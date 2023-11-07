"""
ACCOUNTS : LIST ACCOUNTS
"""
import os
import pickle

#CONFIG
from config.globals import n, w, cy, vars_file_path
from config.header import banner

def list_accounts():
    """LIST ACCOUNTS"""
    os.system('clear')
    banner()
    print(w+'=== LIST ACCOUNTS'+n)
    display = []
    with open(vars_file_path, 'rb') as j:
        while True:
            try:
                display.append(pickle.load(j))
            except EOFError:
                break
    j.close()
    print('==========================================================')
    i = 0
    for z in display:
        print(f'{z[0]} | {z[1]} | {z[2]}')
        i += 1
    print('==========================================================')
    input(cy+'\nPress enter to goto main menu')

if __name__ == "__main__":
    list_accounts()
