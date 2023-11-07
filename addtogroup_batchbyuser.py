"""
ADD TO GROUP : BATCH
"""
import os
import subprocess
from time import sleep
import keyboard
import pickle
from tqdm import tqdm
from datetime import datetime
import csv
from tqdm import tqdm
import re

#THIRD PARTY
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl import functions
from telethon.tl.functions.contacts import AddContactRequest

#CONFIG
from config.globals import lg, n, r, w, cy, ye, vars_file_path
from config.header import banner

current_path = os.getcwd()

def batchbyuser_addtogroup():
    """BATCH BY USERNAME"""
    while True:
        #CHOOSE FILE
        os.system('clear')
        banner()
        print(w+'=== BATCH BY USERNAME'+n)
        print(f'{n}Choose file with users\n')
        folder_path = "./members"
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        i = 0
        for file in files:
            print(f'{n}[{ye}{i}{n}] {file}{n}')
            i += 1

        try:
            index = input(f'\n{cy}Enter your choice: {ye}')
            if not index:
                return
            index = int(index)
            if index < 0 or index >= len(files):
                raise ValueError("Invalid index")
        except ValueError:
            print(f'{r}Invalid input.')
            return

        usernames = []
        userids = []
        with open(f'./members/{files[index]}', mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                username = row.get('username')
                userid = row.get('user id')
                if username:
                    usernames.append(username)
                    userids.append(userid)

        print(f"\n{w}{len(usernames)}  usernames extracted from the CSV:{n}")
        first_10_usernames = usernames[:10]
        more_usernames_count = len(usernames) - 10
        comma_list = ', '.join(first_10_usernames)
        if more_usernames_count > 0:
            comma_list += f", and {more_usernames_count} more..."
        print(comma_list)

        #CREATE SESSIONS
        print(w+'\n=== CHOOSE PHONE FOR BATCH'+n)
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
            print(f'{n}[{ye}{i}{n}] +{acc[2]}')
            i += 1
        ind = int(input(f'\n{cy}Enter your choice: {ye}'))
        api_id = accs[ind][0]
        api_hash = accs[ind][1]
        phone = accs[ind][2]

        input(f'\n{cy}Press enter to continue{w}')
        c = TelegramClient(f'./sessions/{phone}', api_id, api_hash)
        c.connect()
        if not c.is_user_authorized():
            try:
                c.send_code_request(phone)
                code = input(f'\n{cy}Enter the code for {w}{phone}{cy}: {ye}')
                c.sign_in(phone, code)
            except PhoneNumberBannedError:
                print(f'{r}[!]{w}{phone}{r} is banned!{n}')
                print(f'{r}[!]{lg} Go to {w}acounts.py{lg} to filter them{n}')
                sleep(3)
                break
        print(f'\n{ye}[i]{w} Connected...')

        ##5.CHOOSE GROUP
        # chats = []
        # last_date = None
        # chunk_size = 200
        # groups=[]
        # result = c(GetDialogsRequest(offset_date=last_date,offset_id=0,offset_peer=InputPeerEmpty(),limit=chunk_size,hash = 0))
        # chats.extend(result.chats)
        # for chat in chats:
        #     try:
        #         if chat.megagroup == True:
        #             groups.append(chat)
        #     except:
        #         continue

        # print(w+'\n\n=== CHOOSE GROUP'+n)
        # print(f'{n}Choose group to add users\n')

        # i = 0
        # for g in groups:
        #     print(w+'['+ye+str(i)+w+']'+w+' '+' '+g.title)
        #     i+=1
        # g_index = input(f'\n{cy}Enter your choice: {ye}')
        
        #target_group = groups[int(g_index)]
        group = 't.me/worldoflia'
        target_group = c.get_entity(group)
        print(f'\n{ye}[i]{w} Your choice {target_group.title}')
        sleep(1)
        print(f'\n{ye}[i]{w} Batch with phone +{phone}, file: {files[index]}, group:{group} ')

        user_ids_in_csv = set()
        csv_file_path = 'files/logs.csv'
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  
            for row in csv_reader:
                u_id = row[0]
                user_ids_in_csv.add(u_id)

        
        entity = InputPeerChannel(target_group.id, target_group.access_hash)

        def sleep_with_description(description, duration):
            for i in range(duration, 0, -1):
                print(description.format(i))
                sleep(1)

        cooldown = 60
        with open(csv_file_path, mode='a', newline='') as file:
            k_u = 0
            csv_writer = csv.writer(file)
            for username in usernames:
                description = username
                if len(description) < 10:
                    description = description + '-' * (10 - len(description))
                elif len(description) > 10:
                    description = description[:17] + '...'
                if str(userids[k_u]) in user_ids_in_csv:
                    sleep_with_description(f"{ye}[DU] {w} {datetime.now()} {{}} {description}", 0)
                else:
                    if k_u % 35 == 0:
                        sleep_with_description(f"{ye}[--]{w} {datetime.now()}: {username} - {userids[k_u]} : Wait {{}} seconds to proceed ...", 300)
                    try:
                        user_to_add = c.get_input_entity(username)
                        c(InviteToChannelRequest(entity, [user_to_add]))
                        sleep_with_description(f"{ye}[OK]{w} {datetime.now()}: {username} - {userids[k_u]} : Adding {username} - {userids[k_u]} ...", 5)
                    except PeerFloodError as e:
                        csv_writer.writerow([userids[k_u], 'flood', datetime.now()])
                        sleep_with_description(f"{ye}[FL]{w} {datetime.now()}: {username} - {userids[k_u]} {e}: Wait {{}} seconds to proceed ...", cooldown)
                        cooldown +=60
                        continue
                    except UserPrivacyRestrictedError:
                        csv_writer.writerow([userids[k_u], 'privacy', datetime.now()])
                        sleep_with_description(f"{ye}[PR]{w} {datetime.now()}: {username} - {userids[k_u]} : Wait {{}} seconds to proceed ...", 3)
                        continue
                    except Exception as e:
                        sleep_with_description(f"{r}[ER] {datetime.now()}: {username} - {userids[k_u]} : {e}", 2)
                        error_message = str(e)
                        match = re.search(r'\b(\d+)\s+seconds\b', error_message)
                        csv_writer.writerow([userids[k_u], 'error', datetime.now()])
                        if match:
                            seconds = int(match.group(1))
                            sleep_with_description(f"{ye}[ER1]{w} {datetime.now()}: {username} - {userids[k_u]} : Wait {{}} seconds to proceed ...", seconds)
                        else:
                            sleep_with_description(f"{ye}[ER2]{w} {datetime.now()}: {username} - {userids[k_u]} : {{}} - {e}", 5)
                        continue
                    csv_writer.writerow([userids[k_u], 'OK', datetime.now()])
                    sleep_with_description(f"{cy}[OK{w} {datetime.now()}: {username} - {userids[k_u]} : {cy} {username} - {userids[k_u]} {w}", 5)
                    sleep_with_description(f"{ye}[OK]{w} {datetime.now()}: {username} - {userids[k_u]} : Wait {{}} seconds to proceed ...", 60)
                k_u += 1
                    
        input(f'\n{cy}In development... Press enter to go back to main menu')

if __name__ == "__main__":
    batchbyuser_addtogroup()
