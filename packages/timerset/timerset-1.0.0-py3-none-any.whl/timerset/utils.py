'''*************************************************************************************************
Name: utils.py                         Author: Brendan Furey                       Date: 09-Dec-2018

Component module in the python timerset package. This package facilitates code timing for
instrumentation and other purposes, with very small footprint in both code and resource usage.

GitHub: https://github.com/BrenPatF/timerset_python

pip: $ pip install timerset

See 'Code Timing and Object Orientation and Zombies' for the original idea implemented in Oracle 
   PL/SQL, Perl and Java
   http://www.scribd.com/doc/43588788/Code-Timing-and-Object-Orientation-and-Zombies
   Brendan Furey, November 2010

As well as the entry point timerset module there is a helper module, utils, of functions
====================================================================================================
|  Module    |  Notes                                                                              |
|===================================================================================================
|  timerset  |  Code timing class                                                                  |
----------------------------------------------------------------------------------------------------
| *utils*    |  General utility functions                                                          |
====================================================================================================

This file has general utility functions.

*************************************************************************************************'''
from time import process_time, sleep as t_sleep

DELIM = '|'
'''*************************************************************************************************

rJust, lJust: Right/left-justify a string or number

*************************************************************************************************'''
def r_just(name, width): # string to print, width
    sname = str(name)
    if width < len(sname):
        raise ValueError("rJust passed invalid parameters: " + sname + ", " + str(width))
    return ' '*(width - len(sname)) + sname

def l_just(name, width): # string to print, width
    sname = str(name)
    if width < len(sname):
        raise ValueError("lJust passed invalid parameters: " + sname + ", " + str(width))
    return sname + ' '*(width - len(sname))

'''*************************************************************************************************

heading: Returns a title with "=" underlining to its length, preceded by a blank line

*************************************************************************************************'''
def heading (title): # heading string
    return '\n' + title + '\n' + "="*len(title)

'''*************************************************************************************************

csv_to_lis: Returns array by splitting csv string on DELIM

*************************************************************************************************'''
def csv_to_lis(csv): # string to split
    return csv.split(DELIM)

'''*************************************************************************************************

col_headers: Returns a set of column headers, input as array of value, length/justification tuples

*************************************************************************************************'''
def col_headers (col_names): # array of value, length/justification tuples
    strings = list(map(lambda c: l_just(c[0], -c[1]) if c[1] < 0 else r_just(c[0], c[1]), col_names))
    lines = ['  '.join(strings)]
    unders = list(map(lambda s: '-'*len(s), strings))
    lines.append('  '.join(unders))
    return lines

'''*************************************************************************************************

sleep: Sleep for testing, with CPU content, using time.sleep for the non-CPU part

*************************************************************************************************'''
def sleep (stime, fractionCPU = 0.5): # elapsed time to sleep, with fraction to be CPU
    stop = process_time()
    i = 1
    while process_time() < stop + fractionCPU * stime:
        y = 10.0 ** i
        i = 1 if i > 10 else i + 1
    t_sleep((1.0 - fractionCPU) * stime)