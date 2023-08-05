
import datetime as dt
from collections import deque, Counter, namedtuple
from itertools import chain

from sqlalchemy import inspect, select, and_
from sqlalchemy.sql.functions import coalesce

from ..names import ACTIVE_DISTANCE, MAX, M, ACTIVE_TIME, S, ACTIVE_SPEED, KMH, round_km, MEDIAN_KM_TIME, \
    PERCENT_IN_Z, PC, TIME_IN_Z, HR_MINUTES, MAX_MED_HR_M, BPM, MIN, CNT, SUM, AVG, HEART_RATE, DISTANCE, MSR, summaries
from ...squeal.tables.statistic import StatisticJournalFloat, StatisticJournal, StatisticName, StatisticJournalInteger
from ...stoats.calculate import ActivityCalculator
from ...stoats.calculate.heart_rate import hr_zones_from_database
from ...stoats.read.activity import ActivityImporter


class ActivityStatistics(ActivityCalculator):

    def _filter_journals(self, q):
        return q.filter(StatisticName.name == ACTIVE_TIME)

    def _add_stats(self, s, ajournal):
        waypoints = list(self._waypoints(s, ajournal))
        if not waypoints:
            self._log.warn('No statistcs for %s' % ajournal)
            return
        totals = Totals(self._log, waypoints)
        self._add_float_stat(s, ajournal,  ACTIVE_DISTANCE, summaries(MAX, CNT, SUM, MSR), totals.distance, M)
        self._add_float_stat(s, ajournal, ACTIVE_TIME, summaries(MAX, SUM, MSR), totals.time, S)
        self._add_float_stat(s, ajournal, ACTIVE_SPEED, summaries(MAX, AVG, MSR), totals.distance * 3.6 / totals.time, KMH)
        for target in round_km():
            times = list(sorted(TimeForDistance(self._log, waypoints, target * 1000).times()))
            if not times:
                break
            median = len(times) // 2
            self._add_float_stat(s, ajournal, MEDIAN_KM_TIME % target, summaries(MIN, MSR), times[median], S)
        zones = hr_zones_from_database(self._log, s, ajournal.activity_group, ajournal.start)
        if zones:
            for (zone, frac) in Zones(self._log, waypoints, zones).zones:
                self._add_float_stat(s, ajournal, PERCENT_IN_Z % zone, None, 100 * frac, PC)
            for (zone, frac) in Zones(self._log, waypoints, zones).zones:
                self._add_float_stat(s, ajournal, TIME_IN_Z % zone, None, frac * totals.time, S)
            for target in HR_MINUTES:
                heart_rates = sorted(MedianHRForTime(self._log, waypoints, target * 60).heart_rates(), reverse=True)
                if heart_rates:
                    self._add_float_stat(s, ajournal, MAX_MED_HR_M % target, summaries(MAX, MSR), heart_rates[0], BPM)
        else:
            self._log.warn('No HR zones defined for %s or before' % ajournal.start)

    def _waypoints(self, s, ajournal):

        sn = inspect(StatisticName).local_table
        sj = inspect(StatisticJournal).local_table
        sji = inspect(StatisticJournalInteger).local_table
        sjf = inspect(StatisticJournalFloat).local_table

        id_map = self._id_map(s, ajournal)
        ids = list(id_map.keys())

        for timespan in ajournal.timespans:
            self._log.debug('%s' % timespan)
            kargs = {'timespan': timespan}
            stmt = select([sn.c.id, sj.c.time, coalesce(sjf.c.value, sji.c.value)]) \
                .select_from(sj.join(sn).outerjoin(sjf).outerjoin(sji)) \
                .where(and_(sj.c.source_id == ajournal.id,
                            sn.c.id.in_(ids),
                            sj.c.time >= timespan.start,
                            sj.c.time <= timespan.finish)) \
                .order_by(sj.c.time)
            self._log.debug(stmt)
            for id, time, value in s.connection().execute(stmt):
                if 'time' not in kargs:
                    kargs['time'] = time
                elif kargs['time'] != time:
                    yield Waypoint(**kargs)
                    kargs = {'timespan': timespan}
                kargs[id_map[id]] = value
        self._log.debug('Waypoints generated')

    def _id_map(self, s, ajournal):
        # need to convert from statistic_name_id to attribute name
        return {self._id(s, ajournal, HEART_RATE): 'heart_rate',
                self._id(s, ajournal, DISTANCE): 'distance'}

    def _id(self, s, ajournal, name):
        return s.query(StatisticName.id). \
            filter(StatisticName.name == name,
                   StatisticName.owner == ActivityImporter,
                   StatisticName.constraint == ajournal.activity_group).scalar()


Waypoint = namedtuple('Waypoint', 'timespan, time, heart_rate, distance')
'''
This no longer appears as an explicit structure in the database.
It corresponds to a record in the FIT file and is a collection of values from the activity
at a particular time.
'''


class Chunk:
    '''
    A collection of data points in time order, associated with a single timespan.

    In most of the uses below the contents are slowly incremented over time (and
    values popped off the front) as various statistics are calculated.
    '''

    def __init__(self, waypoint):
        self.__timespan = waypoint.timespan
        self.__waypoints = deque([waypoint])

    def append(self, waypoint):
        self.__waypoints.append(waypoint)

    def popleft(self):
        return self.__waypoints.popleft()

    def __diff(self, index, attr, zero=0):
        if len(self.__waypoints) > 1:
            return attr(self.__waypoints[index]) - attr(self.__waypoints[0])
        else:
            return zero

    def distance(self):
        return self.__diff(-1, lambda w: w.distance)

    def distance_delta(self):
        return self.__diff(1, lambda w: w.distance)

    def time(self):
        return self.__diff(-1, lambda w: w.time, dt.timedelta(0)).total_seconds()

    def time_delta(self):
        return self.__diff(1, lambda w: w.time, dt.timedelta(0)).total_seconds()

    def heart_rates(self):
        return (waypoint.heart_rate for waypoint in self.__waypoints if waypoint.heart_rate is not None)

    def __len__(self):
        return len(self.__waypoints)

    def __getitem__(self, item):
        return self.__waypoints[item]

    def __bool__(self):
        return self.distance_delta() > 0


class Chunks:

    def __init__(self, log, waypoints):
        self._log = log
        self._waypoints = waypoints

    def chunks(self):
        chunks, chunk_index = deque(), {}
        for waypoint in self._waypoints:
            timespan = waypoint.timespan
            if timespan in chunk_index:
                chunk_index[timespan].append(waypoint)
            else:
                chunk = Chunk(waypoint)
                chunk_index[timespan] = chunk
                chunks.append(chunk)
            yield chunks


class TimeForDistance(Chunks):

    def __init__(self, log, waypoints, distance):
        super().__init__(log, waypoints)
        self.__distance = distance

    def times(self):
        for chunks in self.chunks():
            distance = sum(chunk.distance() for chunk in chunks)
            if distance > self.__distance:
                while chunks and distance - chunks[0].distance_delta() > self.__distance:
                    distance -= chunks[0].distance_delta()
                    chunks[0].popleft()
                    if not chunks[0]:
                        chunks.popleft()
                time = sum(chunk.time() for chunk in chunks)
                yield time * self.__distance / distance


class MedianHRForTime(Chunks):

    def __init__(self, log, waypoints, time, max_gap=None):
        super().__init__(log, waypoints)
        self.__time = time
        self.__max_gap = 0.01 * time if max_gap is None else max_gap
        log.debug('Will reject gaps > %ds' % int(self.__max_gap))

    def _max_gap(self, chunks):
        return max(c1[0].timespan.start - c2[0].timespan.finish
                   for c1, c2 in zip(list(chunks)[1:], chunks)).total_seconds()

    def heart_rates(self):
        for chunks in self.chunks():
            while len(chunks) > 1 and self._max_gap(chunks) > self.__max_gap:
                self._log.debug('Rejecting chunk because of gap (%ds)' % int(self._max_gap(chunks)))
                chunks.popleft()
            time = sum(chunk.time() for chunk in chunks)
            if time > self.__time:
                while chunks and time - chunks[0].time_delta() > self.__time:
                    time -= chunks[0].time_delta()
                    chunks[0].popleft()
                    while chunks and not chunks[0]:
                        chunks.popleft()
                heart_rates = list(sorted(chain(*(chunk.heart_rates() for chunk in chunks))))
                if heart_rates:
                    median = len(heart_rates) // 2
                    yield heart_rates[median]


class Totals(Chunks):

    def __init__(self, log, waypoints):
        super().__init__(log, waypoints)
        chunks = list(self.chunks())[-1]
        self.distance = sum(chunk.distance() for chunk in chunks)
        self.time = sum(chunk.time() for chunk in chunks)


class Zones(Chunks):

    def __init__(self, log, waypoints, zones):
        super().__init__(log, waypoints)
        # this assumes record data are evenly distributed
        self.zones = []
        chunks = list(self.chunks())[-1]
        counts = Counter()
        lower_limit = 0
        for zone, upper_limit in enumerate(zones):
            for chunk in chunks:
                for heart_rate in chunk.heart_rates():
                    if heart_rate is not None:
                        if lower_limit <= heart_rate < upper_limit:
                            counts[zone] += 1  # zero-based (incremented below)
            lower_limit = upper_limit
        total = sum(counts.values())
        if total:
            for zone in range(len(zones)):
                self.zones.append((zone + 1, counts[zone] / total))


