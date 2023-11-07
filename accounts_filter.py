"""
ACCOUNTS : FILTER ACCOUNTS
"""
from time import sleep
import os
import pickle

#THIRD PARTY
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError

#CONFIG
from config.globals import lg, n, r, w, cy, ye, vars_file_path
from config.header import banner


def filter_banned_accounts():
    """FILTER ACCOUNTS"""
    os.system('clear')
    banner()
    print(w+'=== FILTER BANNED ACCOUNTS'+n)
    print(f'\n{ye}[i]{lg} Scanning accounts ...')
    accounts = []
    banned_accs = []
    with open(vars_file_path, 'rb') as h:
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
    h.close()
    if len(accounts) == 0:
        print(r+'[!] There are no accounts! Please add some and retry')
        sleep(3)
        return
    for account in accounts:
        api_id = int(account[0])
        api_hash = str(account[1])
        phone = str(account[2])
        client = TelegramClient(f'sessions/{phone}', api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
                client.sign_in(phone, input('[+] Enter the code: '))
            except PhoneNumberBannedError:
                print(r+str(phone) + ' is banned!'+n)
                session_file = phone + '.session'
                os.system(f'rm sessions/{session_file}')
                banned_accs.append(account)
    if len(banned_accs) == 0:
        print(f'{ye}[i]{w} Congrats! No banned accounts')
        input(cy+'\nPress enter to goto main menu')
    else:
        for m in banned_accs:
            accounts.remove(m)
        with open(vars_file_path, 'wb') as k:
            for a in accounts:
                _id = a[0]
                _hash = a[1]
                _phone = a[2]
                pickle.dump([_id, _hash, _phone], k)
        k.close()
        print(f'{ye}[i]{w} All banned accounts removed')
        input(cy+'\nPress enter to goto main menu')

if __name__ == "__main__":
    filter_banned_accounts()
