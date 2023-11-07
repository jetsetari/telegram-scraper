"""
ACCOUNTS : MAIN
"""
import os

#CONFIG
from config.globals import lg, n, r, w, cy, ye
from config.header import banner

#DEFS
from accounts_add import add_new_accounts
from accounts_filter import filter_banned_accounts
from accounts_list import list_accounts
from accounts_delete import delete_account

while True:
    os.system('clear')
    banner()
    print(w+'=== ACCOUNTS'+n)
    print(n+'['+ye+'1'+n+'] Add new accounts'+n)
    print(n+'['+ye+'2'+n+'] Filter banned accounts'+n)
    print(n+'['+ye+'3'+n+'] List accounts'+n)
    print(n+'['+ye+'4'+n+'] Delete accounts'+n)
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
        add_new_accounts()
    elif a == 2:
        filter_banned_accounts()
    elif a == 3:
        list_accounts()
    elif a == 4:
        delete_account()
    elif a == 0:
        break
    else:
        input(cy+'\nNothing selected. Press enter to goto main menu')
