'''*************************************************************************************************
Name: testtimerset.py                    Author: Brendan Furey                     Date: 02-Dec-2018

Component module in the python timerset package. This package facilitates code timing for
instrumentation and other purposes, with very small footprint in both code and resource usage.

GitHub: https://github.com/BrenPatF/timerset_python

pip: $ pip install timerset

See 'Code Timing and Object Orientation and Zombies' for the original idea implemented in Oracle 
   PL/SQL, Perl and Java
   http://www.scribd.com/doc/43588788/Code-Timing-and-Object-Orientation-and-Zombies
   Brendan Furey, November 2010

There is an example main program showing how to use the timerset package, and a unit test program.

====================================================================================================
|  Main/Test     |  Unit Module |  Notes                                                           |
|===================================================================================================
|  maincolgroup  |  colgroup    |  Simple file-reading and group-counting module, with logging     |
|                |              |  to file. Example of testing impure units, and error display     |
----------------------------------------------------------------------------------------------------
| *testtimerset* |  timerset    |  Unit testing the timer-set package, uses npm trapit package     |
====================================================================================================

This file has the unit test program for the TimerSet class. See also the example in folder examples.

The test program follows 'The Math Function Unit Testing design pattern'.

GitHub: https://github.com/BrenPatF/trapit_nodejs_tester

Note that the unit test program generates an output timerset_out.json file that is processed by a
separate nodejs program, npm package trapit. This can be installed via npm (npm and nodejs required):

$ npm install timer-set

The output json file contains arrays of expected and actual records by group and scenario, in the
format expected by the Javascript program. The Javascript program produces listings of the results
in html and/or text format, and a sample set of listings is included in the folder test\timerset.

*************************************************************************************************'''
from context import timerset
import sys, traceback
import json
import utils

ROOT = './test/'
INPUT_JSON = ROOT + 'timerset.json'
OUTPUT_JSON = ROOT + 'timerset_out.json'
DELIM, INP, OUT, EXP, ACT = '|', 'inp', 'out', 'exp', 'act'
CON,   INC,   INI,   GET,   GETF,   SELF,   SELFF,   RES = \
"CON", "INC", "INI", "GET", "GETF", "SELF", "SELFF", "RES"
EVENT_SEQUENCE, SCALARS = "Event Sequence", "Scalars"
TIMER_SET_1, TIMER_SET_1_F,       TIMER_SET_2, TIMER_SET_2_F = \
"Set 1",     "Set 1 (formatted)", "Set 2",     "Set 2 (formatted)"
SELF_GRP,          SELF_GRP_F,                   RES_GRP,   EXCEPTION = \
"Self (unmocked)", "Self (unmocked, formatted)", "Results", "Exception"

'''*************************************************************************************************

purely_wrap_unit: Unit test wrapper function. This is called within a loop over input scenarios, 
    returning a dictionary which includes the input dictionary and has the actual program outputs
    inserted

*************************************************************************************************'''
def purely_wrap_unit(call_scenario): # json object for a single scenario, with inputs and expected
                                     # outputs

    mock_yn, time_width, dp_totals, dp_per_call, calls_width = \
        map(lambda s: None if s == '' else s, utils.csv_to_lis(call_scenario[INP][SCALARS][0]))
    events = call_scenario[INP][EVENT_SEQUENCE]
    times = list(map(utils.csv_to_lis, events))
    timer_set = {}
    counter_n = 0
    def now():
        nonlocal counter_n
        counter_n += 1
        return float(times[counter_n - 1][3])

    counter_c = 0
    def cpu():
        nonlocal counter_c
        counter_c += 1
        return float(times[counter_c - 1][4])

    out_arr, out_arr_f, exceptions, self_timer, self_timer_f, results = \
    {TIMER_SET_1: [], TIMER_SET_2: []}, {TIMER_SET_1: [], TIMER_SET_2: []}, [], [], [], []

    for e in events:
        e_lis = utils.csv_to_lis(e)
        set_nm, timer_nm, event, sleep_time, cpu_not_used = e_lis
        if mock_yn != 'Y': utils.sleep(float(sleep_time))
        if event == CON:
            timer_set[set_nm] = timerset.TimerSet(set_nm, now, cpu) if mock_yn == 'Y' \
                           else timerset.TimerSet(set_nm)
        elif event == INC:
            timer_set[set_nm].increment_time(timer_nm)
        elif event == INI:
            timer_set[set_nm].init_time()
        elif event == GET:
            out_arr[set_nm] = list(map(lambda l: l[0] + DELIM + "{:.{}f}".format(l[1], 3) + DELIM +
                                                                "{:.{}f}".format(l[2], 3) + DELIM +
                                                                str(l[3]),
                                       timer_set[set_nm].get_timers()))
        elif event == GETF:
            try:
                out_arr_f[set_nm] = timer_set[set_nm].format_timers(time_width, dp_totals, 
                                                                    dp_per_call, calls_width)
            except:
                tt, value, tb = sys.exc_info()
                exceptions = [str(value), ''.join(traceback.format_exception(tt, value, tb))]
        elif event == SELF:
            st = timerset.TimerSet.get_self_timer()
            self_timer = [str(st[0]) + DELIM + str(st[1])]
        elif event == SELFF:
            self_timer_f = [timerset.TimerSet.format_self_timer()]
        elif event == RES:
            results = [timer_set[set_nm].format_results(time_width, dp_totals, 
                                                        dp_per_call, calls_width)]
        else:
            raise ValueError('Error event {} not known'.format(event))
    return {
        INP: call_scenario[INP],
        OUT: {
              TIMER_SET_1 : {
                  EXP: call_scenario[OUT][TIMER_SET_1], 
                  ACT: out_arr[TIMER_SET_1]
              },
              TIMER_SET_1_F : {
                  EXP: call_scenario[OUT][TIMER_SET_1_F],
                  ACT: out_arr_f[TIMER_SET_1]
              },
              TIMER_SET_2 : {
                  EXP: call_scenario[OUT][TIMER_SET_2], 
                  ACT: out_arr[TIMER_SET_2]
              },
              TIMER_SET_2_F : {
                  EXP: call_scenario[OUT][TIMER_SET_2_F],
                  ACT: out_arr_f[TIMER_SET_2]
              },
              SELF_GRP : {
                  EXP: call_scenario[OUT][SELF_GRP],
                  ACT: self_timer
              },
              SELF_GRP_F : {
                  EXP: call_scenario[OUT][SELF_GRP_F],
                  ACT: self_timer_f
              },
              RES_GRP : {
                  EXP: call_scenario[OUT][RES_GRP],
                  ACT: results
              },
              EXCEPTION : {
                  EXP: call_scenario[OUT][EXCEPTION],
                  ACT: exceptions
              }
        }
    }
'''*************************************************************************************************

Testing main section: 
    Read test input data from json file as object with meta and (call) scenarios objects
    Loop over scenarios passing in the calling scenario to the wrapper function, and assigning
        return value to the (augmented) scenarios object element for the current scenario
    Write the full augmented scenarios object to json output file
*************************************************************************************************'''

with open(INPUT_JSON, encoding='utf-8') as data_file:
    testData = json.loads(data_file.read())

meta, call_scenarios = testData['meta'], testData['scenarios']

scenarios = {}
for s in call_scenarios:
    scenarios[s] = purely_wrap_unit(call_scenarios[s])
out_scenarios = {'meta': meta, 'scenarios': scenarios}

with open(OUTPUT_JSON, 'w') as outfile:
    json.dump(out_scenarios, outfile, indent=4)