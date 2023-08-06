
from sqlalchemy.sql.functions import count

from . import WaypointCalculator
from ..names import SEGMENT_TIME, LATITUDE, LONGITUDE, DISTANCE, S, summaries, MIN, MSR, CNT, HEART_RATE, \
    SEGMENT_HEART_RATE, BPM, MAX
from ..waypoint import filter_none
from ...squeal.tables.activity import ActivityJournal
from ...squeal.tables.segment import SegmentJournal, Segment
from ...squeal.tables.statistic import StatisticName, StatisticJournal, StatisticJournalType


class SegmentStatistics(WaypointCalculator):

    def run(self, force=False, after=None):
        with self._db.session_context() as s:
            if 0 == s.query(count(Segment.id)).scalar():
                self._log.warn('No segments defined in database')
                return
        super().run(force=force, after=after)

    def _filter_statistic_journals(self, q):
        return q.filter(StatisticName.name == SEGMENT_TIME)

    def _filter_activity_journals(self, q):
        return q.join(SegmentJournal, SegmentJournal.activity_journal_id == ActivityJournal.id)

    def _names(self):
        return {LATITUDE: 'lat',
                LONGITUDE: 'lon',
                DISTANCE: 'distance',
                HEART_RATE: 'hr'}

    def _add_stats_from_waypoints(self, s, ajournal, waypoints):
        for sjournal in s.query(SegmentJournal). \
                filter(SegmentJournal.activity_journal == ajournal).all():
            StatisticJournal.add(self._log, s, SEGMENT_TIME, S, summaries(MIN, CNT, MSR), self,
                                 ajournal.activity_group, sjournal,
                                 (sjournal.finish - sjournal.start).total_seconds(),
                                 sjournal.start, StatisticJournalType.FLOAT)
            waypoints = [w for w in filter_none(self._names().values(), waypoints)
                         if sjournal.start <= w.time <= sjournal.finish]
            # weight by time gap so we don't bias towards more sampled times
            gaps = [(w1.time - w0.time, 0.5 * (w0.hr + w1.hr))
                    for w0, w1 in zip(waypoints, waypoints[1:])]
            if gaps:
                weighted = sum(dt.total_seconds() * hr for dt, hr in gaps)
                average = weighted / sum(dt.total_seconds() for dt, _ in gaps)
                StatisticJournal.add(self._log, s, SEGMENT_HEART_RATE, BPM, summaries(MAX, CNT, MSR), self,
                                     ajournal.activity_group, sjournal, average,
                                     sjournal.start, StatisticJournalType.FLOAT)
            else:
                self._log.warn('No Heart Rate data')
