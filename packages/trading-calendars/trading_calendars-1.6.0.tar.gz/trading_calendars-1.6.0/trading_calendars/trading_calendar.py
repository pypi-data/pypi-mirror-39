#
# Copyright 2018 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from abc import ABCMeta, abstractproperty
from lru import LRU
import warnings

from operator import attrgetter
from pandas.tseries.holiday import AbstractHolidayCalendar
from six import with_metaclass
import numpy as np
from numpy import searchsorted
import pandas as pd
from pandas import (
    DataFrame,
    date_range,
    DatetimeIndex,
)
from pandas.tseries.offsets import CustomBusinessDay
import toolz

from .calendar_helpers import (
    compute_all_minutes,
    is_open,
    next_divider_idx,
    previous_divider_idx,
)
from .utils.memoize import lazyval
from .utils.pandas_utils import days_at_time
from .utils.preprocess import preprocess, coerce


start_default = pd.Timestamp('1990-01-01', tz='UTC')
end_base = pd.Timestamp('today', tz='UTC')
# Give an aggressive buffer for logic that needs to use the next trading
# day or minute.
end_default = end_base + pd.Timedelta(days=365)

NANOS_IN_MINUTE = 60000000000
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)
WEEKDAYS = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY)
WEEKENDS = (SATURDAY, SUNDAY)


def selection(arr, start, end):
    predicates = []
    if start is not None:
        predicates.append(start.tz_localize('UTC') <= arr)
    if end is not None:
        predicates.append(arr < end.tz_localize('UTC'))

    if not predicates:
        return arr

    return arr[np.all(predicates, axis=0)]


def _group_times(all_days, times, tz, offset):
    elements = [
        days_at_time(
            selection(all_days, start, end),
            time,
            tz,
            offset
        )
        for (start, time), (end, _) in toolz.sliding_window(
            2,
            toolz.concatv(times, [(None, None)])
        )
    ]
    return elements[0].append(elements[1:])


class TradingCalendar(with_metaclass(ABCMeta)):
    """
    An TradingCalendar represents the timing information of a single market
    exchange.

    The timing information is made up of two parts: sessions, and opens/closes.

    A session represents a contiguous set of minutes, and has a label that is
    midnight UTC. It is important to note that a session label should not be
    considered a specific point in time, and that midnight UTC is just being
    used for convenience.

    For each session, we store the open and close time in UTC time.
    """
    def __init__(self, start=start_default, end=end_default):
        # Midnight in UTC for each trading day.

        # In pandas 0.18.1, pandas calls into its own code here in a way that
        # fires a warning. The calling code in pandas tries to suppress the
        # warning, but does so incorrectly, causing it to bubble out here.
        # Actually catch and suppress the warning here:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            _all_days = date_range(start, end, freq=self.day, tz='UTC')

        # `DatetimeIndex`s of standard opens/closes for each day.
        self._opens = _group_times(
            _all_days,
            self.open_times,
            self.tz,
            self.open_offset,
        )
        self._closes = _group_times(
            _all_days,
            self.close_times,
            self.tz,
            self.close_offset,
        )

        # `Series`s mapping sessions with nonstandard opens/closes to
        # the open/close time.
        _special_opens = self._calculate_special_opens(start, end)
        _special_closes = self._calculate_special_closes(start, end)

        # Overwrite the special opens and closes on top of the standard ones.
        _overwrite_special_dates(_all_days, self._opens, _special_opens)
        _overwrite_special_dates(_all_days, self._closes, _special_closes)

        # In pandas 0.16.1 _opens and _closes will lose their timezone
        # information. This looks like it has been resolved in 0.17.1.
        # http://pandas.pydata.org/pandas-docs/stable/whatsnew.html#datetime-with-tz  # noqa
        self.schedule = DataFrame(
            index=_all_days,
            columns=['market_open', 'market_close'],
            data={
                'market_open': self._opens,
                'market_close': self._closes,
            },
            dtype='datetime64[ns]',
        )

        # Simple cache to avoid recalculating the same minute -> session in
        # "next" mode. Analysis of current zipline code paths show that
        # `minute_to_session_label` is often called consecutively with the same
        # inputs.
        self._minute_to_session_label_cache = LRU(1)

        self.market_opens_nanos = self.schedule.market_open.values.\
            astype(np.int64)

        self.market_closes_nanos = self.schedule.market_close.values.\
            astype(np.int64)

        self._trading_minutes_nanos = self.all_minutes.values.\
            astype(np.int64)

        self.first_trading_session = _all_days[0]
        self.last_trading_session = _all_days[-1]

        self._late_opens = pd.DatetimeIndex(
            _special_opens.map(self.minute_to_session_label)
        )

        self._early_closes = pd.DatetimeIndex(
            _special_closes.map(self.minute_to_session_label)
        )

    @lazyval
    def day(self):
        return CustomBusinessDay(
            holidays=self.adhoc_holidays,
            calendar=self.regular_holidays,
            weekmask=self.weekmask,
        )

    @abstractproperty
    def name(self):
        raise NotImplementedError()

    @abstractproperty
    def tz(self):
        raise NotImplementedError()

    @abstractproperty
    def open_times(self):
        """
        Returns a list of tuples of (start_date, open_time).  If the open
        time is constant throughout the calendar, use None for the start_date.
        """
        raise NotImplementedError()

    @abstractproperty
    def close_times(self):
        """
        Returns a list of tuples of (start_date, close_time).  If the close
        time is constant throughout the calendar, use None for the start_date.
        """
        raise NotImplementedError()

    @property
    def weekmask(self):
        """
        String indicating the days of the week on which the market is open.

        Default is '1111100' (i.e., Monday-Friday).

        See Also
        --------
        numpy.busdaycalendar
        """
        return '1111100'

    @property
    def open_offset(self):
        return 0

    @property
    def close_offset(self):
        return 0

    @lazyval
    def _minutes_per_session(self):
        diff = self.schedule.market_close - self.schedule.market_open
        diff = diff.astype('timedelta64[m]')
        return diff + 1

    def minutes_count_for_sessions_in_range(self, start_session, end_session):
        """
        Parameters
        ----------
        start_session: pd.Timestamp
            The first session.

        end_session: pd.Timestamp
            The last session.

        Returns
        -------
        int: The total number of minutes for the contiguous chunk of sessions.
             between start_session and end_session, inclusive.
        """
        return int(self._minutes_per_session[start_session:end_session].sum())

    @property
    def regular_holidays(self):
        """
        Returns
        -------
        pd.AbstractHolidayCalendar: a calendar containing the regular holidays
        for this calendar
        """
        return None

    @property
    def adhoc_holidays(self):
        return []

    @property
    def special_opens(self):
        """
        A list of special open times and corresponding HolidayCalendars.

        Returns
        -------
        list: List of (time, AbstractHolidayCalendar) tuples
        """
        return []

    @property
    def special_opens_adhoc(self):
        """
        Returns
        -------
        list: List of (time, DatetimeIndex) tuples that represent special
         closes that cannot be codified into rules.
        """
        return []

    @property
    def special_closes(self):
        """
        A list of special close times and corresponding HolidayCalendars.

        Returns
        -------
        list: List of (time, AbstractHolidayCalendar) tuples
        """
        return []

    @property
    def special_closes_adhoc(self):
        """
        Returns
        -------
        list: List of (time, DatetimeIndex) tuples that represent special
         closes that cannot be codified into rules.
        """
        return []

    # -----

    @property
    def opens(self):
        return self.schedule.market_open

    @property
    def closes(self):
        return self.schedule.market_close

    @property
    def late_opens(self):
        return self._late_opens

    @property
    def early_closes(self):
        return self._early_closes

    def is_session(self, dt):
        """
        Given a dt, returns whether it's a valid session label.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt that is being tested.

        Returns
        -------
        bool
            Whether the given dt is a valid session label.
        """
        return dt in self.schedule.index

    def is_open_on_minute(self, dt):
        """
        Given a dt, return whether this exchange is open at the given dt.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to check if this exchange is open.

        Returns
        -------
        bool
            Whether the exchange is open on this dt.
        """
        return is_open(self.market_opens_nanos, self.market_closes_nanos,
                       dt.value)

    def next_open(self, dt):
        """
        Given a dt, returns the next open.

        If the given dt happens to be a session open, the next session's open
        will be returned.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to get the next open.

        Returns
        -------
        pd.Timestamp
            The UTC timestamp of the next open.
        """
        idx = next_divider_idx(self.market_opens_nanos, dt.value)
        return pd.Timestamp(self.market_opens_nanos[idx], tz='UTC')

    def next_close(self, dt):
        """
        Given a dt, returns the next close.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to get the next close.

        Returns
        -------
        pd.Timestamp
            The UTC timestamp of the next close.
        """
        idx = next_divider_idx(self.market_closes_nanos, dt.value)
        return pd.Timestamp(self.market_closes_nanos[idx], tz='UTC')

    def previous_open(self, dt):
        """
        Given a dt, returns the previous open.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to get the previous open.

        Returns
        -------
        pd.Timestamp
            The UTC imestamp of the previous open.
        """
        idx = previous_divider_idx(self.market_opens_nanos, dt.value)
        return pd.Timestamp(self.market_opens_nanos[idx], tz='UTC')

    def previous_close(self, dt):
        """
        Given a dt, returns the previous close.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to get the previous close.

        Returns
        -------
        pd.Timestamp
            The UTC timestamp of the previous close.
        """
        idx = previous_divider_idx(self.market_closes_nanos, dt.value)
        return pd.Timestamp(self.market_closes_nanos[idx], tz='UTC')

    def next_minute(self, dt):
        """
        Given a dt, return the next exchange minute.  If the given dt is not
        an exchange minute, returns the next exchange open.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to get the next exchange minute.

        Returns
        -------
        pd.Timestamp
            The next exchange minute.
        """
        idx = next_divider_idx(self._trading_minutes_nanos, dt.value)
        return self.all_minutes[idx]

    def previous_minute(self, dt):
        """
        Given a dt, return the previous exchange minute.

        Raises KeyError if the given timestamp is not an exchange minute.

        Parameters
        ----------
        dt: pd.Timestamp
            The dt for which to get the previous exchange minute.

        Returns
        -------
        pd.Timestamp
            The previous exchange minute.
        """

        idx = previous_divider_idx(self._trading_minutes_nanos, dt.value)
        return self.all_minutes[idx]

    def next_session_label(self, session_label):
        """
        Given a session label, returns the label of the next session.

        Parameters
        ----------
        session_label: pd.Timestamp
            A session whose next session is desired.

        Returns
        -------
        pd.Timestamp
            The next session label (midnight UTC).

        Notes
        -----
        Raises ValueError if the given session is the last session in this
        calendar.
        """
        idx = self.schedule.index.get_loc(session_label)
        try:
            return self.schedule.index[idx + 1]
        except IndexError:
            if idx == len(self.schedule.index) - 1:
                raise ValueError("There is no next session as this is the end"
                                 " of the exchange calendar.")
            else:
                raise

    def previous_session_label(self, session_label):
        """
        Given a session label, returns the label of the previous session.

        Parameters
        ----------
        session_label: pd.Timestamp
            A session whose previous session is desired.

        Returns
        -------
        pd.Timestamp
            The previous session label (midnight UTC).

        Notes
        -----
        Raises ValueError if the given session is the first session in this
        calendar.
        """
        idx = self.schedule.index.get_loc(session_label)
        if idx == 0:
            raise ValueError("There is no previous session as this is the"
                             " beginning of the exchange calendar.")

        return self.schedule.index[idx - 1]

    def minutes_for_session(self, session_label):
        """
        Given a session label, return the minutes for that session.

        Parameters
        ----------
        session_label: pd.Timestamp (midnight UTC)
            A session label whose session's minutes are desired.

        Returns
        -------
        pd.DateTimeIndex
            All the minutes for the given session.
        """
        return self.minutes_in_range(
            start_minute=self.schedule.at[session_label, 'market_open'],
            end_minute=self.schedule.at[session_label, 'market_close'],
        )

    def execution_minutes_for_session(self, session_label):
        """
        Given a session label, return the execution minutes for that session.

        Parameters
        ----------
        session_label: pd.Timestamp (midnight UTC)
            A session label whose session's minutes are desired.

        Returns
        -------
        pd.DateTimeIndex
            All the execution minutes for the given session.
        """
        return self.minutes_in_range(
            start_minute=self.execution_time_from_open(
                self.schedule.at[session_label, 'market_open'],
            ),
            end_minute=self.execution_time_from_close(
                self.schedule.at[session_label, 'market_close'],
            ),
        )

    def execution_minutes_for_sessions_in_range(self, start, stop):
        minutes = self.execution_minutes_for_session
        return pd.DatetimeIndex(
            np.concatenate([
                minutes(session)
                for session in self.sessions_in_range(start, stop)
            ]),
            tz='UTC',
        )

    def minutes_window(self, start_dt, count):
        start_dt_nanos = start_dt.value
        all_minutes_nanos = self._trading_minutes_nanos
        start_idx = all_minutes_nanos.searchsorted(start_dt_nanos)

        # searchsorted finds the index of the minute **on or after** start_dt.
        # If the latter, push back to the prior minute.
        if all_minutes_nanos[start_idx] != start_dt_nanos:
            start_idx -= 1

        if start_idx < 0 or start_idx >= len(all_minutes_nanos):
            raise KeyError("Can't start minute window at {}".format(start_dt))

        end_idx = start_idx + count

        if start_idx > end_idx:
            return self.all_minutes[(end_idx + 1):(start_idx + 1)]
        else:
            return self.all_minutes[start_idx:end_idx]

    def sessions_in_range(self, start_session_label, end_session_label):
        """
        Given start and end session labels, return all the sessions in that
        range, inclusive.

        Parameters
        ----------
        start_session_label: pd.Timestamp (midnight UTC)
            The label representing the first session of the desired range.

        end_session_label: pd.Timestamp (midnight UTC)
            The label representing the last session of the desired range.

        Returns
        -------
        pd.DatetimeIndex
            The desired sessions.
        """
        return self.all_sessions[
            self.all_sessions.slice_indexer(
                start_session_label,
                end_session_label
            )
        ]

    def sessions_window(self, session_label, count):
        """
        Given a session label and a window size, returns a list of sessions
        of size `count` + 1, that either starts with the given session
        (if `count` is positive) or ends with the given session (if `count` is
        negative).

        Parameters
        ----------
        session_label: pd.Timestamp
            The label of the initial session.

        count: int
            Defines the length and the direction of the window.

        Returns
        -------
        pd.DatetimeIndex
            The desired sessions.
        """
        start_idx = self.schedule.index.get_loc(session_label)
        end_idx = start_idx + count

        return self.all_sessions[
            min(start_idx, end_idx):max(start_idx, end_idx) + 1
        ]

    def session_distance(self, start_session_label, end_session_label):
        """
        Given a start and end session label, returns the distance between them.
        For example, for three consecutive sessions Mon., Tues., and Wed,
        ``session_distance(Mon, Wed)`` returns 3. If ``start_session`` is after
        ``end_session``, the value will be negated.

        Parameters
        ----------
        start_session_label: pd.Timestamp
            The label of the start session.
        end_session_label: pd.Timestamp
            The label of the ending session inclusive.

        Returns
        -------
        int
            The distance between the two sessions.
        """
        negate = end_session_label < start_session_label
        if negate:
            start_session_label, end_session_label = (
                end_session_label,
                start_session_label,
            )
        start_idx = self.all_sessions.searchsorted(start_session_label)
        end_idx = self.all_sessions.searchsorted(
            end_session_label,
            side='right',
        )

        out = end_idx - start_idx
        if negate:
            out = -out

        return out

    def minutes_in_range(self, start_minute, end_minute):
        """
        Given start and end minutes, return all the calendar minutes
        in that range, inclusive.

        Given minutes don't need to be calendar minutes.

        Parameters
        ----------
        start_minute: pd.Timestamp
            The minute representing the start of the desired range.

        end_minute: pd.Timestamp
            The minute representing the end of the desired range.

        Returns
        -------
        pd.DatetimeIndex
            The minutes in the desired range.
        """
        start_idx = searchsorted(self._trading_minutes_nanos,
                                 start_minute.value)

        end_idx = searchsorted(self._trading_minutes_nanos,
                               end_minute.value)

        if end_minute.value == self._trading_minutes_nanos[end_idx]:
            # if the end minute is a market minute, increase by 1
            end_idx += 1

        return self.all_minutes[start_idx:end_idx]

    def minutes_for_sessions_in_range(self,
                                      start_session_label,
                                      end_session_label):
        """
        Returns all the minutes for all the sessions from the given start
        session label to the given end session label, inclusive.

        Parameters
        ----------
        start_session_label: pd.Timestamp
            The label of the first session in the range.

        end_session_label: pd.Timestamp
            The label of the last session in the range.

        Returns
        -------
        pd.DatetimeIndex
            The minutes in the desired range.

        """
        first_minute, _ = self.open_and_close_for_session(start_session_label)
        _, last_minute = self.open_and_close_for_session(end_session_label)

        return self.minutes_in_range(first_minute, last_minute)

    def open_and_close_for_session(self, session_label):
        """
        Returns a tuple of timestamps of the open and close of the session
        represented by the given label.

        Parameters
        ----------
        session_label: pd.Timestamp
            The session whose open and close are desired.

        Returns
        -------
        (Timestamp, Timestamp)
            The open and close for the given session.
        """
        sched = self.schedule

        # `market_open` and `market_close` should be timezone aware, but pandas
        # 0.16.1 does not appear to support this:
        # http://pandas.pydata.org/pandas-docs/stable/whatsnew.html#datetime-with-tz  # noqa
        return (
            sched.at[session_label, 'market_open'].tz_localize('UTC'),
            sched.at[session_label, 'market_close'].tz_localize('UTC'),
        )

    def session_open(self, session_label):
        return self.schedule.at[
            session_label,
            'market_open'
        ].tz_localize('UTC')

    def session_close(self, session_label):
        return self.schedule.at[
            session_label,
            'market_close'
        ].tz_localize('UTC')

    def session_opens_in_range(self, start_session_label, end_session_label):
        return self.schedule.loc[
            start_session_label:end_session_label,
            'market_open',
        ].dt.tz_localize('UTC')

    def session_closes_in_range(self, start_session_label, end_session_label):
        return self.schedule.loc[
            start_session_label:end_session_label,
            'market_close',
        ].dt.tz_localize('UTC')

    @property
    def all_sessions(self):
        return self.schedule.index

    @property
    def first_session(self):
        return self.all_sessions[0]

    @property
    def last_session(self):
        return self.all_sessions[-1]

    def execution_time_from_open(self, open_dates):
        return open_dates

    def execution_time_from_close(self, close_dates):
        return close_dates

    @lazyval
    def all_minutes(self):
        """
        Returns a DatetimeIndex representing all the minutes in this calendar.
        """
        opens_in_ns = self._opens.values.astype(
            'datetime64[ns]',
        ).view('int64')

        closes_in_ns = self._closes.values.astype(
            'datetime64[ns]',
        ).view('int64')

        return DatetimeIndex(
            compute_all_minutes(opens_in_ns, closes_in_ns),
            tz='utc',
        )

    @preprocess(dt=coerce(pd.Timestamp, attrgetter('value')))
    def minute_to_session_label(self, dt, direction="next"):
        """
        Given a minute, get the label of its containing session.

        Parameters
        ----------
        dt : pd.Timestamp or nanosecond offset
            The dt for which to get the containing session.

        direction: str
            "next" (default) means that if the given dt is not part of a
            session, return the label of the next session.

            "previous" means that if the given dt is not part of a session,
            return the label of the previous session.

            "none" means that a KeyError will be raised if the given
            dt is not part of a session.

        Returns
        -------
        pd.Timestamp (midnight UTC)
            The label of the containing session.
        """
        if direction == "next":
            try:
                return self._minute_to_session_label_cache[dt]
            except KeyError:
                pass

        idx = searchsorted(self.market_closes_nanos, dt)
        current_or_next_session = self.schedule.index[idx]
        self._minute_to_session_label_cache[dt] = current_or_next_session

        if direction == "next":
            return current_or_next_session
        elif direction == "previous":
            if not is_open(self.market_opens_nanos, self.market_closes_nanos,
                           dt):
                # if the exchange is closed, use the previous session
                return self.schedule.index[idx - 1]
        elif direction == "none":
            if not is_open(self.market_opens_nanos, self.market_closes_nanos,
                           dt):
                # if the exchange is closed, blow up
                raise ValueError("The given dt is not an exchange minute!")
        else:
            # invalid direction
            raise ValueError("Invalid direction parameter: "
                             "{0}".format(direction))

        return current_or_next_session

    def minute_index_to_session_labels(self, index):
        """
        Given a sorted DatetimeIndex of market minutes, return a
        DatetimeIndex of the corresponding session labels.

        Parameters
        ----------
        index: pd.DatetimeIndex or pd.Series
            The ordered list of market minutes we want session labels for.

        Returns
        -------
        pd.DatetimeIndex (UTC)
            The list of session labels corresponding to the given minutes.
        """
        if not index.is_monotonic_increasing:
            raise ValueError(
                "Non-ordered index passed to minute_index_to_session_labels."
            )

        # Find the indices of the previous open and the next close for each
        # minute.
        prev_opens = (
            self._opens.values.searchsorted(index.values, side='right') - 1
        )
        next_closes = (
            self._closes.values.searchsorted(index.values, side='left')
        )

        # If they don't match, the minute is outside the trading day. Barf.
        mismatches = (prev_opens != next_closes)
        if mismatches.any():
            # Show the first bad minute in the error message.
            bad_ix = np.flatnonzero(mismatches)[0]
            example = index[bad_ix]

            prev_day = prev_opens[bad_ix]
            prev_open, prev_close = self.schedule.iloc[prev_day]
            next_open, next_close = self.schedule.iloc[prev_day + 1]

            raise ValueError(
                "{num} non-market minutes in minute_index_to_session_labels:\n"
                "First Bad Minute: {first_bad}\n"
                "Previous Session: {prev_open} -> {prev_close}"
                "Next Session: {next_open} -> {next_close}"
                .format(
                    num=mismatches.sum(),
                    first_bad=example,
                    prev_open=prev_open, prev_close=prev_close,
                    next_open=next_open, next_close=next_close)
            )

        return self.schedule.index[prev_opens]

    def _special_dates(self, calendars, ad_hoc_dates, start_date, end_date):
        """
        Compute a Series of times associated with special dates.

        Parameters
        ----------
        holiday_calendars : list[(datetime.time, HolidayCalendar)]
            Pairs of time and calendar describing when that time occurs. These
            are used to describe regularly-scheduled late opens or early
            closes.
        ad_hoc_dates : list[(datetime.time, list[pd.Timestamp])]
            Pairs of time and list of dates associated with the given times.
            These are used to describe late opens or early closes that occurred
            for unscheduled or otherwise irregular reasons.
        start_date : pd.Timestamp
            Start of the range for which we should calculate special dates.
        end_date : pd.Timestamp
            End of the range for which we should calculate special dates.

        Returns
        -------
        special_dates : pd.Series
            Series mapping trading sessions with special opens/closes to the
            special open/close for that session.
        """
        # List of Series for regularly-scheduled times.
        regular = [
            scheduled_special_times(
                calendar,
                start_date,
                end_date,
                time_,
                self.tz,
            )
            for time_, calendar in calendars
        ]

        # List of Series for ad-hoc times.
        ad_hoc = [
            pd.Series(
                index=pd.to_datetime(datetimes, utc=True),
                data=days_at_time(datetimes, time_, self.tz),
            )
            for time_, datetimes in ad_hoc_dates
        ]

        merged = regular + ad_hoc
        if not merged:
            # Concat barfs if the input has length 0.
            return pd.Series([])

        result = pd.concat(merged).sort_index()
        return result.loc[(result >= start_date) & (result <= end_date)]

    def _calculate_special_opens(self, start, end):
        return self._special_dates(
            self.special_opens,
            self.special_opens_adhoc,
            start,
            end,
        )

    def _calculate_special_closes(self, start, end):
        return self._special_dates(
            self.special_closes,
            self.special_closes_adhoc,
            start,
            end,
        )


def scheduled_special_times(calendar, start, end, time, tz):
    """
    Returns a Series mapping each holiday (as a UTC midnight Timestamp)
    in ``calendar`` between ``start`` and ``end`` to that session at
    ``time`` (as a UTC Timestamp).
    """
    days = calendar.holidays(start, end)
    return pd.Series(
        index=pd.DatetimeIndex(days, tz='UTC'),
        data=days_at_time(days, time, tz=tz),
    )


def _overwrite_special_dates(midnight_utcs,
                             opens_or_closes,
                             special_opens_or_closes):
    """
    Overwrite dates in open_or_closes with corresponding dates in
    special_opens_or_closes, using midnight_utcs for alignment.
    """
    # Short circuit when nothing to apply.
    if not len(special_opens_or_closes):
        return

    len_m, len_oc = len(midnight_utcs), len(opens_or_closes)
    if len_m != len_oc:
        raise ValueError(
            "Found misaligned dates while building calendar.\n"
            "Expected midnight_utcs to be the same length as open_or_closes,\n"
            "but len(midnight_utcs)=%d, len(open_or_closes)=%d" % len_m, len_oc
        )

    # Find the array indices corresponding to each special date.
    indexer = midnight_utcs.get_indexer(special_opens_or_closes.index)

    # -1 indicates that no corresponding entry was found.  If any -1s are
    # present, then we have special dates that doesn't correspond to any
    # trading day.
    if -1 in indexer:
        bad_dates = list(special_opens_or_closes[indexer == -1])
        raise ValueError("Special dates %s are not trading days." % bad_dates)

    # NOTE: This is a slightly dirty hack.  We're in-place overwriting the
    # internal data of an Index, which is conceptually immutable.  Since we're
    # maintaining sorting, this should be ok, but this is a good place to
    # sanity check if things start going haywire with calendar computations.
    opens_or_closes.values[indexer] = special_opens_or_closes.values


class HolidayCalendar(AbstractHolidayCalendar):
    def __init__(self, rules):
        super(HolidayCalendar, self).__init__(rules=rules)
