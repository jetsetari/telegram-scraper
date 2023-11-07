"""
ACCOUNTS : ADD ACCOUNTS
"""
from time import sleep
import os
import pickle

#THIRD PARTY
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from colorama import init

#CONFIG
from config.globals import n, r, w, cy, ye, vars_file_path
from config.header import banner

init()

def add_new_accounts():
    """ADD NEW ACCOUNTS"""
    os.system('clear')
    banner()
    print(w+'=== ADD NEW ACCOUNTS'+n)
    with open(vars_file_path, 'ab') as g:
        newly_added = []
        while True:
            a = int(input(f'\n{cy}Enter API ID: {ye}'))
            b = str(input(f'{cy}Enter API Hash: {ye}'))
            c = str(input(f'{cy}Enter Phone Number: {ye}'))
            p = ''.join(c.split())
            pickle.dump([a, b, p], g)
            newly_added.append([a, b, p])
            ab = input(f'{cy}\nDo you want to add more accounts? [{ye}y{cy}/{ye}n{cy}]: {ye}')
            if 'y' in ab:
                pass
            else:
                print(f'{ye}[i]{w} Saved all accounts in vars.txt')
                g.close()
                sleep(3)
                os.system('clear')
                banner()
                print(f'{ye}[i]{w} Logging in from new accounts...\n')
                print(f'{n}==========================================================')
                for added in newly_added:
                    c = TelegramClient(f'sessions/{added[2]}', added[0], added[1])
                    try:
                        print(f'{ye}[i]{w} Creating session for {added[2]}{n}')
                        c.start()
                        print(f'n\n{ye}[+] {w} Logged in - {added[2]}')
                        c.disconnect()
                    except PhoneNumberBannedError:
                        print(f'{r}[!] {added[2]} is banned! Filter it using option 2')
                        continue
                    print('\n')
                print(f'{n}==========================================================')
                input(cy+'\nPress enter to goto main menu')
                break
    g.close()

if __name__ == "__main__":
    add_new_accounts()
