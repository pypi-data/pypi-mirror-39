# Copyright 2009-2019 INRIA Rhone-Alpes, Service Experimentation et
# Developpement
#
# This file is part of Execo.
#
# Execo is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Execo is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Execo.  If not, see <http://www.gnu.org/licenses/>

from .log import style
from .time_utils import format_date, format_duration
import sys
if sys.version_info >= (3,):
    _BIGNUM = sys.maxsize
else:
    _BIGNUM = sys.maxint

#def sort_reports(reports):
#    reports.sort(key = lambda report: report.stats().get('start_date') or _BIGNUM)

class Report(object):

    """Summary of one or more `execo.action.Action`.

    A Report gathers the results of actions or (recursively) of other
    reports.
    """

    def __init__(self, stats_objects = None):
        """
        :param stats_objects:
        """
        self.__name = "%s" % (self.__class__.__name__,)
        self._stats = Report.empty_stats()
        self._stats['name'] = self.__name
        if stats_objects:
            self.add(stats_objects)

    @property
    def name(self):
        """Name given to this report. If None, a default
        name will be given."""
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self._stats['name'] = self.__name

    def add(self, stats_objects):
        """Add some sub-`execo.report.Report` or `execo.action.Action` to this report.

        :param stats_objects:
        """
        self._stats['sub_stats'].extend([o.stats() for o in stats_objects])

    @staticmethod
    def empty_stats():
        """Return a stats initialized to zero."""
        return {
            'name': None,
            'start_date': None,
            'end_date': None,
            'num_processes': 0,
            'num_started': 0,
            'num_ended': 0,
            'num_errors': 0,
            'num_timeouts': 0,
            'num_forced_kills': 0,
            'num_non_zero_exit_codes': 0,
            'num_expect_fail': 0,
            'num_write_error': 0,
            'num_ok': 0,
            'num_finished_ok': 0,
            'sub_stats': [],
            }

    @staticmethod
    def aggregate_stats(stats):
        aggstats = stats.copy()
        no_end_date = False
        for substats in stats['sub_stats']:
            for k in substats:
                if k == 'start_date':
                    if (substats[k] != None
                        and (aggstats[k] == None or substats[k] < aggstats[k])):
                        aggstats[k] = substats[k]
                elif k == 'end_date':
                    if substats[k] == None:
                        no_end_date = True
                    elif aggstats[k] == None or substats[k] > aggstats[k]:
                        aggstats[k] = substats[k]
                elif k in [
                    'num_processes',
                    'num_started',
                    'num_ended',
                    'num_errors',
                    'num_timeouts',
                    'num_forced_kills',
                    'num_non_zero_exit_codes',
                    'num_expect_fail',
                    'num_write_error',
                    'num_ok',
                    'num_finished_ok'
                    ]:
                    aggstats[k] += substats[k]
        if no_end_date:
            aggstats['end_date'] = None
        return aggstats

    def stats(self):
        """Return a dict summarizing the statistics of all `execo.action.Action` and sub-`execo.report.Report` registered to this report.

        This stats dict contains the following metrics:

        - ``start_date``: earliest start date (unix timestamp) of all
          `Action` or None if none have started yet.

        - ``end_date``: latest end date (unix timestamp) of all
          `Action` or None if not available (not all started, not all
          ended).

        - ``num_processes``: number of processes in all `Action`.

        - ``num_started``: number of processes that have started.

        - ``num_ended``: number of processes that have ended.

        - ``num_errors``: number of processes that went in error
          when started.

        - ``num_timeouts``: number of processes that had to be killed
          (SIGTERM) after reaching their timeout.

        - ``num_forced_kills``: number of processes that had to be
          forcibly killed (SIGKILL) after not responding for some
          time.

        - ``num_non_zero_exit_codes``: number of processes that ran
          correctly but whose return code was != 0.

        - ``num_expect_fail``: number of processes on which there was
          an expect failure, i.e. the expect search did not find a
          match before reaching the expect timeout or the stream
          eof/error.

        - ``num_write_error``: number of processes on which there was
          a write error.

        - ``num_ok``: number of processes which:

          - did not started

          - started and not yet ended

          - started and ended and did not went in error (or where
            launched with flag ignore_error) , did not timeout (or
            where launched with flag ignore_timeout), and had an exit
            code == 0 (or where launched with flag ignore_exit_code).

        - ``num_finished_ok``: number of processes which started,
          ended, and are ok.
        """
        return Report.aggregate_stats(self._stats)

    def __repr__(self):
        return "<Report(<%i entries>, name=%r)>" % (len(self._stats['sub_stats']), self._stats['name'])

    def __str__(self):
        stats = self.stats()
        return "<Report(<%i entries>, name=%r, start_date=%r, end_date=%r, num_processes=%r, num_started=%r, num_ended=%r, num_timeouts=%r, num_errors=%r, num_forced_kills=%r, num_expect_fail=%r, num_write_error=%r, num_non_zero_exit_codes=%r, num_ok=%r, num_finished_ok=%r)>" % (
            len(stats['sub_stats']),
            stats['name'],
            format_date(stats['start_date']),
            format_date(stats['end_date']),
            stats['num_processes'],
            stats['num_started'],
            stats['num_ended'],
            stats['num_timeouts'],
            stats['num_errors'],
            stats['num_forced_kills'],
            stats['num_expect_fail'],
            stats['num_write_error'],
            stats['num_non_zero_exit_codes'],
            stats['num_ok'],
            stats['num_finished_ok'])

    def to_string(self, wide = False, brief = False):
        """Returns a formatted string with a human-readable stats of all `Action` results.

        :param wide: if False (default), report format is designed for
          80 columns display. If True, output a (175 characters) wide
          report.

        :param brief: when True, only the Total stats is output, not
          each `Action` or `Report` stats. Default is False.
        """
        output = ""
        if wide:
            output += "Name                            start               end                 length         startd ended  error  timout fkilld expfld wrterr ret!=0 ok     total  \n"
            output += "-------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        else:
            output += "Name                            start               end                 total  \n"
            output += " length         startd ended  error  timout fkilld expfld wrterr ret!=0 ok     \n"
            output += "-------------------------------------------------------------------------------\n"
        def format_line(stats, indent):
            result = ""
            indented_name = " " * indent + "%s" % (stats.get('name'),)
            length = ""
            if stats.get('start_date') and stats.get('end_date'):
                length = format_duration(stats['end_date'] - stats['start_date'])
            else:
                length = ""
            if wide:
                tmpline = "%-31.31s %-19.19s %-19.19s %-15.15s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s\n" % (
                    indented_name,
                    format_date(stats['start_date']),
                    format_date(stats['end_date']),
                    length,
                    stats['num_started'],
                    stats['num_ended'],
                    stats['num_errors'],
                    stats['num_timeouts'],
                    stats['num_forced_kills'],
                    stats['num_expect_fail'],
                    stats['num_write_error'],
                    stats['num_non_zero_exit_codes'],
                    stats['num_ok'],
                    stats['num_processes'])
            else:
                tmpline = "%-31.31s %-19.19s %-19.19s %-7.7s\n" % (
                    indented_name,
                    format_date(stats['start_date']),
                    format_date(stats['end_date']),
                    stats['num_processes'],)
                tmpline += " %-15.15s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s%-7.7s\n" % (
                    length,
                    stats['num_started'],
                    stats['num_ended'],
                    stats['num_errors'],
                    stats['num_timeouts'],
                    stats['num_forced_kills'],
                    stats['num_expect_fail'],
                    stats['num_write_error'],
                    stats['num_non_zero_exit_codes'],
                    stats['num_ok'],)
            if stats['num_ok'] < stats['num_processes']:
                if stats['num_ok'] == stats['num_ended'] and (stats['num_expect_fail'] == 0 and stats['num_write_error'] == 0):
                    tmpline = style.report_warn(tmpline)
                else:
                    tmpline = style.report_error(tmpline)
            result += tmpline
            return result

        def recurse_stats(stats, indent):
            result = ""
            result += format_line(stats, indent)
            for sub_stats in stats['sub_stats']:
                result += recurse_stats(sub_stats, indent+2)
            return result

        stats = self.stats()
        if not brief and len(stats['sub_stats']) > 0:
            for sub_stats in sorted(stats['sub_stats'],
                                    key = lambda stats: stats.get('start_date') or _BIGNUM):
                output += recurse_stats(sub_stats, 0)
            if wide:
                output += "--------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            else:
                output += "-------------------------------------------------------------------------------\n"

        output += format_line(stats, 0)
        return output
