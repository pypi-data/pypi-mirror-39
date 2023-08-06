'''*************************************************************************************************
Name: timerset.py                      Author: Brendan Furey                       Date: 09-Dec-2018

Component module in the python timerset package. This package facilitates code timing for
instrumentation and other purposes, with very small footprint in both code and resource usage.

GitHub: https://github.com/BrenPatF/timerset_python

pip: $ pip install timerset

See 'Code Timing and Object Orientation and Zombies' for the original idea implemented in Oracle 
   PL/SQL, Perl and Java
   http://www.scribd.com/doc/43588788/Code-Timing-and-Object-Orientation-and-Zombies
   Brendan Furey, November 2010

As well as the entry point timerset module there is a helper module, utils, of utility functions
====================================================================================================
|  Module    |  Notes                                                                              |
|===================================================================================================
| *timerset* |  Code timing class                                                                  |
----------------------------------------------------------------------------------------------------
|  utils     |  General utility functions                                                          |
====================================================================================================

This file has the entry point TimerSet class. See the example in folder examples, and unit test in
folder test.

*************************************************************************************************'''
from time import process_time, perf_counter
from functools import reduce
import utils
from datetime import datetime

# Constants are display lengths, decimal places and labels, plus number of times to call self-timer
#  and s->ms factor
CALLS_WIDTH, TIME_WIDTH, TIME_DP, TIME_RATIO_DP, TOT_TIMER, OTH_TIMER, SELF_TIME, TIME_FACTOR = \
10,          8,          2,       5,             'Total',   '(Other)', 0.1,       1000
timer_times = []

'''*************************************************************************************************

_getTimes: Gets elapsed and CPU times using system calls (or mocks) and returns as tuple

*************************************************************************************************'''
def _get_times(now, cpu): # elapsed, CPU time functions (may be from time, or mocks)
    return now(), cpu()

'''*************************************************************************************************

_val_widths: Handle parameter defaulting, and validate width parameters, int() where necessary
    Parameters: time width and decimal places, time ratio dp, calls width

*************************************************************************************************'''
def _val_widths(time_width, time_dp, time_ratio_dp, calls_width):
    def default_prm(val, default): # parameter value, default value
        return default if val is None else int(val)
    time_width = default_prm(time_width, TIME_WIDTH)
    time_dp = default_prm(time_dp, TIME_DP)
    time_ratio_dp = default_prm(time_ratio_dp, TIME_RATIO_DP)
    calls_width = default_prm(calls_width, CALLS_WIDTH)

    if calls_width < 5:
        raise ValueError(('Error, calls_width must be > 4, actual: {calls_width}').
            format(calls_width=str(calls_width)))
    elif time_width < 0 or time_dp < 0 or time_ratio_dp < 0:
        raise ValueError(('Error, time_width, time_dp, time_ratio_dp must be > 0, actual: {actual}').
            format(actual=str(time_width) + ', ' + str(time_dp) + ', ' + str(time_ratio_dp)))
    elif time_width + time_dp < 6:
        raise ValueError(('Error, time_width + time_dp must be > 6, actual: {actual}').
            format(actual=str(time_width) + ' + ' + str(time_dp)))
    elif time_width + time_ratio_dp < 8:
        raise ValueError(('Error, time_width + time_ratio_dp must be > 7, actual: {actual}').
            format(actual=str(time_width) + ' + ' + str(time_ratio_dp)))
    return time_width, time_dp, time_ratio_dp, calls_width
'''*************************************************************************************************

_form*: Formatting methods that return formatted times and other values as strings

*************************************************************************************************'''
def _form_name(name, max_name): # timer name, column length as maximum timer name length
    return ('{0:'+str(max_name)+'s}').format(name)
def _form_time(t, dp, time_width): # time, decimal places to print
    return ('{0:'+str(time_width + dp)+'.'+ str(dp)+'f}').format(t)
def _form_time_trim (t, dp, time_width): # time, decimal places to print
    return _form_time(t, dp, time_width).lstrip()
def _form_calls(calls, calls_width): # number of calls to timer
    return ('{0:'+str(calls_width)+'d}').format(calls)
def _form_dt_time(t = datetime.now()): # datetime, defaulting to now
    return datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
'''*************************************************************************************************

_timer_line: Returns a formatted timing line
    Parameters: timer name, maximum timer name length, elapsed, cpu times, number of calls to timer,
                time width and decimal places, time ratio dp, calls width

*************************************************************************************************'''
def _timer_line(timer, max_name, ela, cpu, calls, time_width, time_dp, time_ratio_dp, calls_width):
    return '  '.join([_form_name(timer, max_name),
                      _form_time(ela, time_dp, time_width),
                      _form_time(cpu, time_dp, time_width),
                      _form_calls(calls, calls_width),
                      _form_time(ela/calls, time_ratio_dp, time_width),
                      _form_time(cpu/calls, time_ratio_dp, time_width)])

class TimerSet:

    '''*********************************************************************************************

    __init__: Constructor function, which sets the timer set name and initialises the instance
              timing variables. Saves the timing functions passed, or defaulted, to object instance
        Parameters: timer set name, elapsed, CPU time functions defaulting to 'from time' functions

    *********************************************************************************************'''
    def __init__(self, timer_set_name, p_now = perf_counter, p_cpu = process_time):
        self.now = p_now
        self.cpu = p_cpu
        self.timer_set_name = timer_set_name
        self.n_times = -1
        self.timer_hash = {}
        self.ela_time_start, self.cpu_time_start = _get_times(self.now, self.cpu)
        self.ela_time_prior, self.cpu_time_prior = self.ela_time_start, self.cpu_time_start
        self.stime = datetime.now()
        self.results = []

    '''*********************************************************************************************

    init_time: Initialises (or resets) the instance timing array

    *********************************************************************************************'''
    def init_time(self):
        self.ela_time_prior, self.cpu_time_prior = _get_times(self.now, self.cpu)

    '''*********************************************************************************************

    increment_time: Increments the timing accumulators for a timer

    ************************************************************************************************'''
    def increment_time(self, timer_name): # timer name

        ela_dif, cpu_dif = _get_times(self.now, self.cpu)

        cur_hash = self.timer_hash.get(timer_name, [0, 0, 0])
        self.timer_hash[timer_name] = [cur_hash[0] + ela_dif - self.ela_time_prior, 
                                       cur_hash[1] + cpu_dif - self.cpu_time_prior, cur_hash[2] + 1]
        self.ela_time_prior, self.cpu_time_prior = ela_dif, cpu_dif
    '''*********************************************************************************************

    get_timers: Returns the results for timer set in an array of objects

    *********************************************************************************************'''
    def get_timers(self):
        if len(self.results) == 0:
            ela_dif, cpu_dif = _get_times(self.now, self.cpu)
            tot_tim = [ela_dif - self.ela_time_start, cpu_dif - self.cpu_time_start]
            sum_tim = reduce((lambda s, t: [s[0]+t[0],s[1]+t[1],s[2]+t[2]]), self.timer_hash.values())
            self.results = [(k, v[0], v[1], v[2]) for k, v in self.timer_hash.items()]
            self.results.append([OTH_TIMER, tot_tim[0] - sum_tim[0], tot_tim[1] - sum_tim[1], 1])
            self.results.append([TOT_TIMER, tot_tim[0], tot_tim[1], sum_tim[2] + 1])
        return self.results
    '''*********************************************************************************************

    format_timers: Writes the timers to an array of formatted strings for the timer set
        Parameters: time width and decimal places, time ratio dp, calls width

    *********************************************************************************************'''
    def format_timers(self, time_width = None, time_dp = None, time_ratio_dp = None, 
                      calls_width = None):
        time_width, time_dp, time_ratio_dp, calls_width = _val_widths(
        time_width, time_dp, time_ratio_dp, calls_width)

        timer_arr = self.get_timers()
        max_name = max(len(max(self.timer_hash.keys(),key=len)), len(OTH_TIMER))
        lenTime, lenTimeRatio = time_width + time_dp, time_width + time_ratio_dp
        fmt_arr = utils.col_headers([
                        ['Timer',    -max_name],
                        ['Elapsed',  time_width+time_dp],
                        ['CPU',      time_width+time_dp],
                        ['Calls',    calls_width],
                        ['Ela/Call', time_width+time_ratio_dp],
                        ['CPU/Call', time_width+time_ratio_dp]
                  ])
        for i, t in enumerate(timer_arr):
            fmt_arr.append(_timer_line(t[0], max_name, t[1], t[2], t[3], time_width, time_dp, 
                                      time_ratio_dp, calls_width))
            if i > len(timer_arr) - 3: fmt_arr.append(fmt_arr[1])

        return fmt_arr

    '''*********************************************************************************************

    get_self_timer: Static function returns 2-tuple with timings per call for calling increment_time

    *********************************************************************************************'''
    def get_self_timer():
        timer_timer = TimerSet('timer')
        t, i = 0, 0
        while t < SELF_TIME:
            timer_timer.increment_time('x')
            i += 1
            if i % 100 == 0: t = timer_timer.timer_hash.get('x')[0]

        timer_times = timer_timer.timer_hash.get('x')
        return timer_times[0]/i, timer_times[1]/i

    '''*********************************************************************************************

    format_self_timer: Static function returns formatted string with the results of get_self_timer
        Parameters: time width and decimal places, time ratio dp

    *********************************************************************************************'''
    def format_self_timer(time_width = None, time_dp = None, time_ratio_dp = None):
        time_width, time_dp, time_ratio_dp, calls_width = _val_widths(
        time_width, time_dp, time_ratio_dp, None)

        t = TimerSet.get_self_timer()
        return '[Timer timed (per call in ms): Elapsed: ' + _form_time_trim(TIME_FACTOR*t[0], 
            time_ratio_dp, time_width) + ', CPU: ' + _form_time_trim(TIME_FACTOR*t[1], time_ratio_dp, 
            time_width) + ']'
        
    '''*********************************************************************************************

    format_results: Returns formatted string with the complete results, using format_timers;
                    includes self timing results
        Parameters: time width and decimal places, time ratio dp, calls width

    *********************************************************************************************'''
    def format_results(self, time_width = None, time_dp = None, time_ratio_dp = None,
                       calls_width = None):
        time_width, time_dp, time_ratio_dp, calls_width = _val_widths(
        time_width, time_dp, time_ratio_dp, calls_width)

        return utils.heading("Timer set: " + self.timer_set_name + ", constructed at " +
                    _form_dt_time(self.stime) + ", written at " + _form_dt_time()) + '\n' + \
                    reduce(lambda s, l: s + '\n' + l, self.format_timers(
                        time_width, time_dp, time_ratio_dp, calls_width)) + '\n' + \
                    TimerSet.format_self_timer(time_width, time_dp, time_ratio_dp)