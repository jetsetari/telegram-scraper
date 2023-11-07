import os
import time

wh = "\033[1;37m"
re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
ye = "\033[1;33m"  # Yellow color
reset = "\033[0m"  # Reset color


os.system('clear')
print(f"""{wh}
     _   _  _   _   _ 
    | | | \\| | | | | |
    | | | .  | | |_| |
    |_| |_|\\_| |_____|

    Version: 1.1 | Author: 4RI
    {reset}
""")


try:
    import pip
except ImportError:
    print("pip is not installed. Please install pip first.")
    exit(1)

print(wh + '[+] This may take some time ...'+gr)
os.system("""
    pip3 install cython numpy pandas
    python3 -m pip install cython numpy pandas
""")
print(wh + '\n[+] Installing requirements ...'+gr)

os.system("""
    pip3 install telethon requests configparser colorama
    python3 -m pip install telethon requests configparser
    mkdir files
    mkdir members
    touch ./files/config.data
""")
from colorama import init
init(autoreset=True)
print(wh + '\n[+] Succesfully installed ...'+wh)
time.sleep(1)
os.system('clear')

from config.header import banner
banner()
print(reset + "[+] Requirements installed.")
print(reset + "[+] Setting up config.data.\n")
if os.path.getsize('./files/config.data') == 0:
    import configparser
    print(wh + "Fill in credentials from your main account.\n")
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input(wh+"[+] enter api ID : "+re)
    cpass.set('cred', 'id', xid)
    xhash = input(wh+"[+] enter hash ID : "+re)
    cpass.set('cred', 'hash', xhash)
    xphone = input(wh+"[+] enter phone number : "+re)
    cpass.set('cred', 'phone', xphone)
    setup = open('./files/config.data', 'w')
    cpass.write(setup)
    setup.close()
    print(wh+"[+] setup complete !")
else:
    print(wh + "[+] config.data is already set up.\n")

time.sleep(3)
init()
os.system('python3 main.py')