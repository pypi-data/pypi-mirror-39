
import datetime as dt
from json import loads

from sqlalchemy import asc, desc
from urwid import Pile, Text, Columns

from . import Displayer
from ..calculate.impulse import ImpulseStatistics, Response
from ...lib.date import local_date_to_time
from ...lib.schedule import Schedule
from ...lib.utils import label, em, error
from ...squeal.tables.constant import Constant
from ...squeal.tables.statistic import StatisticJournal, StatisticName, TYPE_TO_JOURNAL_CLASS
from ...uweird.tui.decorators import Indent


class ImpulseDiary(Displayer):

    def _build_date(self, s, f, date, fitness=None, fatigue=None):
        yield from self._build_schedule(s, f, date, schedule=Schedule('d'), fitness=fitness, fatigue=fatigue)

    def _build_schedule(self, s, f, date, schedule=None, fitness=None, fatigue=None):
        rows = []

        def append(cols):
            if cols:
                rows.append(Columns(cols))

        append(list(self._single_response(s, f, date, schedule, fitness, schedule.frame_type == 'd')))
        append(list(self._single_response(s, f, date, schedule, fatigue, schedule.frame_type == 'd')))
        if rows:
            yield Pile([Text('SHRIMP'), Indent(Pile(rows))])

    def _single_response(self, s, f, date, schedule, constant_name, display_range):
        start_time = local_date_to_time(schedule.start_of_frame(date))
        finish_time = local_date_to_time(schedule.next_frame(date))
        response = Response(**loads(Constant.get(s, constant_name).at(s, start_time).value))
        start = self._read(s, response.dest_name, start_time, finish_time, asc)
        finish = self._read(s, response.dest_name, start_time, finish_time, desc)
        if start and finish and start.value != finish.value:
            lo, hi = self._range(s, response.dest_name, start, finish_time, dt.timedelta(days=90))
            if display_range:
                style = 'quintile-%d' % min(5, 1 + int(5 * (finish.value - lo.value) / (hi.value - lo.value)))
            else:
                style = 'label'
            yield Text([label('%s/%s: ' % (response.dest_name, schedule.describe())),
                       (style, '%5d - %5d ' % (int(start.value), int(finish.value))),
                       em('+ve') if start.value < finish.value else error('-ve')])
            if display_range:
                yield Text([label('Range over 90 days: %5d - %5d' % (int(lo.value), int(hi.value)))])

    def _read(self, s, name, start_time, finish_time, direcn):
        return s.query(StatisticJournal). \
            join(StatisticName). \
            filter(StatisticName.name == name,
                   StatisticName.owner == ImpulseStatistics,
                   StatisticJournal.time >= start_time,
                   StatisticJournal.time < finish_time). \
            order_by(direcn(StatisticJournal.time)). \
            limit(1).one_or_none()

    def _range(self, s, name, value, finish_time, period):
        jtype = TYPE_TO_JOURNAL_CLASS[type(value.value)]
        start_time = finish_time - period
        q = s.query(jtype). \
            join(StatisticName). \
            filter(StatisticName.name == name,
                   StatisticName.owner == ImpulseStatistics,
                   jtype.time >= start_time,
                   jtype.time < finish_time)
        return (q.order_by(asc(jtype.value)).limit(1).one(),
                q.order_by(desc(jtype.value)).limit(1).one())
