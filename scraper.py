"""
SCRAPER
"""
import os
import pickle
import configparser
from time import sleep
import csv

#THIRD PARTY
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.types import UserStatusOffline, InputPeerEmpty
from telethon.tl.functions.channels import GetFullChannelRequest

#CONFIG
from config.globals import lg, n, r, w, cy, ye, vars_file_path
from config.header import banner

while True:
    ##1.LOGIN WITH MAIN ACCOUNT
    os.system('clear')
    banner()
    print(w+'=== SCRAPER'+n)
    print(f'{n}Connecting with main account....\n')

    cpass = configparser.RawConfigParser()
    cpass.read('./files/config.data')

    try:
        main_api_id = cpass['cred']['id']
        main_api_hash = cpass['cred']['hash']
        main_phone = cpass['cred']['phone']
        client = TelegramClient(f'./sessions/{main_phone}', main_api_id, main_api_hash)
    except KeyError:
        os.system('clear')
        banner()
        print(r+"[!] setup config.data file first\n")
        break

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(main_phone)
        os.system('clear')
        banner()
        client.sign_in(main_phone, input(cy+'\nEnter the code from your main account: '+ye))

    ##2.GET GROUPS FROM MAIN ACCOUNT
    chats = []
    LAST_DATE = None
    CHUNK_SIZE = 200
    groups=[]
    result = client(GetDialogsRequest(
                offset_date=LAST_DATE,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=CHUNK_SIZE,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    os.system('clear')
    banner()
    print(w+'=== CHOOSE GROUP'+n)
    print(f'{n}Choose a group to scrape members\n')
    i=0
    username = r+'[main]'
    scraped_files = os.listdir('./members')
    for g in groups:
        f_name = str(g.id)+'.csv'
        p_add = '▢'
        if hasattr(g, 'username') and g.username is not None :
            username = n+'- @'+g.username
            f_name = g.username+'.csv'
        else:
            username = r+'[main]'+n+'- @'+str(g.id)

        if f_name in scraped_files:
            p_add = '▣'
        
        print(w+'['+ye+str(i)+w+']'+w+' '+p_add+' '+g.title+' '+username)
        i+=1

    g_index = input(f'\n{cy}Enter your choice: {ye}')
    target_group=groups[int(g_index)]
    print(f'{n}Your choice {target_group.title}')
    sleep(3)

    ##3.CHOOSE ACCOUNT TO SCRAPE
    if target_group.username is not None :
        os.system('clear')
        banner()
        print(w+'=== SCRAPER'+n)
        print(f'{n}Choose an account to scrape members\n')
        accs = []
        with open(vars_file_path, "rb") as f:
            while True:
                try:
                    accs.append(pickle.load(f))
                except EOFError:
                    f.close()
                    break
        f.close()
        i = 0
        for acc in accs:
            print(f'{n}[{ye}{i}{n}] {acc[2]}')
            i += 1
        ind = int(input(f'\n{cy}Enter your choice: {ye}'))
        api_id = accs[ind][0]
        api_hash = accs[ind][1]
        phone = accs[ind][2]
        print(f'{n}Your choice {phone}')
    else:
        os.system('clear')
        banner()
        print(w+'=== SCRAPER'+n)
        print(f'{r}Attention: {n}Your main account will be used to scrape\n')
        phone = main_phone

    ##4.CREATE SESSION OF SLAVE ACCOUNT
    if target_group.username is not None :
        c = TelegramClient(f'./sessions/{phone}', api_id, api_hash)
        c.connect()
        if not c.is_user_authorized():
            try:
                c.send_code_request(phone)
                code = input(f'\n{cy}Enter the code for {w}{phone}{cy}: {ye}')
                c.sign_in(phone, code)
            except PhoneNumberBannedError:
                print(f'{r}[!]{w}{phone}{r} is banned!{n}')
                print(f'{r}[!]{lg} Run {w}acounts.py{lg} to filter them{n}')
                break
    else:
        c = client


    ##5. FETCH MEMBERS
    print(lg+'\nFetching Members...')
    group = target_group
    file_name = str(target_group.id)
    if target_group.username is not None :
        group = c.get_entity(target_group.username)
        file_name = target_group.username

    members = []
    members = c.iter_participants(group, aggressive=True)
    channel_full_info = c(GetFullChannelRequest(group))
    cont = len(list(enumerate(members)))
    csv_members = []

    print(f'members (max 10k): {len(list(enumerate(members)))}')

    def write(_group,_member):
        """WRITE CSV"""
        if _member.username:
            _username = _member.username
        else:
            _username = ''
        if isinstance(_member.status,UserStatusOffline):
            writer.writerow([_username, _member.id, _member.access_hash, _group.title, _group.id,_member.status.was_online]) # pylint: disable=line-too-long
        else:
            writer.writerow([_username, _member.id, _member.access_hash, _group.title, _group.id,type(_member.status).__name__]) # pylint: disable=line-too-long

    with open(f'members/{target_group.username}.csv', "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id','status'])
        try:
            for index,member in enumerate(members):
                if index%100 == 0:
                    print(lg+'Wait 3 seconds...')
                    sleep(3)
                if not member.bot:
                    print(f'{n}[{ye}{index+1}/{cont}{n}] {n} {member.id} - {member.username}')
                    write(group,member)
                    if member.username is not None and isinstance(member.username, str):
                        csv_members.append(member.username)
        except: # pylint: disable=bare-except
            print(f'{ye}[i]{w} {cont} FloodWaitError, check {target_group.username}.csv')

    f.close()
    os.system('clear')
    banner()
    print(w+'=== DONE'+n)
    print(f'{ye}[i]{w} {cont} users saved in {target_group.username}.csv')
    COMMA_LIST = ', '.join(csv_members)
    print(f'{n}{COMMA_LIST}')

    sleep(5)
    break
