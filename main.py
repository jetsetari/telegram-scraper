"""
ACCOUNTS : FILTER ACCOUNTS
"""
import os
from colorama import init
from config.globals import lg, n, ye, w, cy, r
from config.header import banner

init()

while True:
    os.system('clear')
    banner()
    print(w+'=== MENU'+n)
    print(n+'['+ye+'1'+n+'] Accounts'+n)
    print(n+'['+ye+'2'+n+'] Scraper'+n)
    print(n+'['+ye+'3'+n+'] Add to group'+n)
    print(n+'['+ye+'4'+n+'] Send Message'+n)
    print(lg+'[0] Quit'+n)
    try:
        A = input(f'\n{cy}Enter your choice: {ye}')
        if not A:
            break
        A = int(A)
    except ValueError:
        print(f'{r}Invalid input.{n}')
        A = 0
    if A == 1:
        os.system('python3 accounts.py')
    elif A == 2:
        os.system('python3 scraper.py')
    elif A == 3:
        os.system('python3 addtogroup.py')
    elif A == 4:
        os.system('python3 sendmessage.py')
    elif A == 0:
        break
    else:
        input(cy+'\nNothing selected. Press enter to goto main menu')
