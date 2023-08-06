'''*************************************************************************************************
Name: maincolgroup.py                    Author: Brendan Furey                     Date: 09-Dec-2018

Component module in the python timerset package. This package facilitates code timing for
instrumentation and other purposes, with very small footprint in both code and resource usage.

GitHub: https://github.com/BrenPatF/timerset_python

pip: $ pip install timerset

See 'Code Timing and Object Orientation and Zombies' for the original idea implemented in Oracle 
   PL/SQL, Perl and Java
   http://www.scribd.com/doc/43588788/Code-Timing-and-Object-Orientation-and-Zombies
   Brendan Furey, November 2010

There is an example main program showing how to use the timerset package, and a unit test program
====================================================================================================
|  Main/Test     |  Unit Module |  Notes                                                           |
|===================================================================================================
| *maincolgroup* |  colgroup    |  Simple file-reading and group-counting module, with code timing.|
|                |              |  Example showing how to use the timer-et package                 
----------------------------------------------------------------------------------------------------
|  testtimerset  |  timerset    |  Unit testing the timerset package, uses npm trapit package      |
====================================================================================================

Main driver for simple file-reading and group-counting module, with code timing. It is used as an
example showing how to use the timerset package.

To run from root (timerset) folder:

$ python examples\colgroup\maincolgroup

*************************************************************************************************'''
from context import timerset
import colgroup as cg

ts = timerset.TimerSet('Timer_ts')

(input_file, delim, col) = './examples/colgroup/fantasy_premier_league_player_stats.csv', ',', 6

grp = cg.ColGroup(input_file, delim, col)
ts.increment_time ('ColGroup')

grp.pr_list('(as is)', grp.list_as_is())
ts.increment_time ('list_as_is')

grp.pr_list('key', grp.sort_by_key())
ts.increment_time('sort_by_key')

grp.pr_list('value (item_getter)', grp.sort_by_value_IG())
ts.increment_time('sort_by_valueIG')

grp.pr_list('value (lambda)', grp.sort_by_value_lambda())
ts.increment_time('sort_by_value_lambda')

print(ts.format_results())