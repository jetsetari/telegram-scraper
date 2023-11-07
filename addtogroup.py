"""
ADD TO GROUP : MAIN
"""
import os

#CONFIG
from config.globals import lg, n, r, w, cy, ye
from config.header import banner

#DEFS
from addtogroup_single import single_addtogroup
from addtogroup_batch import batch_addtogroup
from addtogroup_batchbyuser import batchbyuser_addtogroup
from addtogroup_batchbyid import batchbyid_addtogroup

while True:
    os.system('clear')
    banner()
    print(w+'=== ADD TO GROUP'+n)
    print(n+'['+ye+'1'+n+'] Test single user'+n)
    print(n+'['+ye+'2'+n+'] Batch by username'+n)
    print(n+'['+ye+'3'+n+'] Batch by user id'+n)
    print(lg+'[0] --Back'+n)
    try:
        a = input(f'\n{cy}Enter your choice: {ye}')
        if not a:
            break
        a = int(a)
    except ValueError:
        print(f'{r}Invalid input.{n}')
        input(cy+'\nPress enter to goto main menu')
    if a == 1:
        single_addtogroup()
    elif a == 2:
        batchbyuser_addtogroup()
    elif a == 3:
        batchbyid_addtogroup()
    elif a == 0:
        break
    else:
        input(cy+'\nNothing selected. Press enter to goto main menu')
