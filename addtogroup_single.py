"""
ADD TO GROUP : SINGLE
"""
import os
import subprocess
from time import sleep
import keyboard
import pickle
from tqdm import tqdm
from datetime import datetime
import csv

#THIRD PARTY
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl import functions

#CONFIG
from config.globals import lg, n, r, w, cy, ye, vars_file_path
from config.header import banner

current_path = os.getcwd()

def single_addtogroup():
    """TEST SINGLE USER TO ADD GROUP"""
    while True:
        ##1.CHOOSE ACCOUNT
        os.system('clear')
        banner()
        print(w+'=== ADD TO GROUP : TEST USER'+n)
        print(f'{n}Choose phone to test\n')
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
        print(f'{n}Account you selected: {phone}')
        sleep(1)

        ##2.ADD WITH USERNAME OR ID?
        os.system('clear')
        banner()
        print(w+'=== CHOOSE METHOD'+n)
        print(f'{n}Choose how you want to add user to group\n')
        print(n+'['+ye+'1'+n+'] Add user with username'+n)
        print(n+'['+ye+'2'+n+'] Add user with user ID'+n)
        try:
            add_type = input(f'\n{cy}Enter your choice: {ye}')
            if not add_type:
                break
            add_type = int(add_type)
        except ValueError:
            print(f'{r}Invalid input.{n}')
            input(cy+'\nPress enter to goto main menu')
        print(f'{n}Processing...')
        sleep(1)

        ##4.CREATE SESSION
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
        sleep(3)

        ##3.FILL IN USER ID
        os.system('clear')
        banner()
        print(w+'=== FILL IN DETAILS'+n)
        print(f'{n}Fill in details of user\n')
        if add_type == 1:
            user_name = str(input(f'{cy}Enter username: {ye}'))
            user_id = c.get_input_entity(user_name).user_id
            #user_to_add = c.get_input_entity(user_name)
            print(f'{n}User you selected: {user_name}')
        elif add_type == 2:
            user_id = int(input(f'{cy}Enter ID: {ye}'))
            # try:
            #     user_to_add = c.get_input_entity(user_id)
            # except Exception as e:
            #     print(f'{r}[!]{w} {e}{n}')
            #     break
            #user_hash = int(input(f'{cy}Enter hash: {ye}'))
            print(f'{n}User you selected: {user_id}')
        else:
            input(cy+'\nNothing selected. Press enter to goto main menu')
            break
        sleep(1)

        ##5.CHOOSE GROUP
        chats = []
        last_date = None
        chunk_size = 200
        groups=[]
        result = c(GetDialogsRequest(offset_date=last_date,offset_id=0,offset_peer=InputPeerEmpty(),limit=chunk_size,hash = 0))
        chats.extend(result.chats)
        for chat in chats:
            try:
                if chat.megagroup == True:
                    groups.append(chat)
            except:
                continue

        print(w+'\n\n=== CHOOSE GROUP'+n)
        print(f'{n}Choose group to add user\n')

        i = 0
        for g in groups:
            print(w+'['+ye+str(i)+w+']'+w+' '+' '+g.title)
            i+=1
        g_index = input(f'\n{cy}Enter your choice: {ye}')
        # group = 't.me/worldoflia'
        # target_group = c.get_entity(group)
        target_group = groups[int(g_index)]
        print(f'{n}Your choice {target_group.title}')
        sleep(1)

        ##5.ADDING USER
        print(f'{ye}[i]{w} Wait 3 seconds...')
        sleep(1)
        print(f'{ye}[i]{w} Wait 2 seconds...')
        sleep(1)
        print(f'{ye}[i]{w} Wait 1 seconds...')
        sleep(1)

        user_ids_in_csv = set()
        csv_file_path = 'files/logs.csv'
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  
            for row in csv_reader:
                u_id = row[0]
                user_ids_in_csv.add(u_id)

        with open(csv_file_path, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            # if str(user_id) in user_ids_in_csv:
            #     print(f'{r}[!]{w} This user is already tested. See files/logs.csv to see the result{n}')
            #     sleep(3)
            # else:
            try:
                print(f'{ye}[i]{w} Adding user...')
                entity = InputPeerChannel(target_group.id, target_group.access_hash)
                if add_type == 1:
                    user_to_add = c.get_input_entity(user_name)
                elif add_type == 2:
                    user_to_add = c(functions.users.GetFullUserRequest(id=user_id))
                    print(user_to_add.stringify())
                    sleep(5)
                    break
                    #user_to_add = InputPeerUser(user_id, user_hash)
                c(InviteToChannelRequest(entity, [user_to_add]))
                sleep(1)
            except PeerFloodError as e:
                #time.sleep()
                print(f'{r}[!]{w} Aborted. Peer Flood Error {e} {n}')
                csv_writer.writerow([user_id, 'flood', datetime.now()])
                sleep(1)
                break
            except UserPrivacyRestrictedError:
                print(f'{r}[!]{w} User Privacy Restriction{n}')
                csv_writer.writerow([user_id, 'privacy', datetime.now()])
                sleep(1)
                break
            except Exception as e:
                print(f'{r}[!]{w} Some Other error in adding{n}')
                print(f'{r}[!]{w} {e}{n}')
                csv_writer.writerow([user_id, 'error', datetime.now()])
                sleep(1)
                break
            csv_writer.writerow([user_id, 'OK', datetime.now()])
            print(f'{ye}[i]{w} User successfully added')
            sleep(5)

        
if __name__ == "__main__":
    single_addtogroup()
