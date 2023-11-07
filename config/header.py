from colorama import init, Fore
import os, random
import time
import sys

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
rs = Fore.RESET
colors = [lg, r, w, cy, ye]
error = lg + '(' + r + '!' + lg + ')' + rs

def banner():
    print(f"""
{ye} _  {ye} _  _  {ye} _   _ 
{ye}| | {ye}| \\| |{ye} | | | |
{ye}| | {ye}| .  |{ye} | |_| |
{ye}|_| {ye}|_|\\_|{ye} |_____| 

Version: 1.1 | Author: 4RI\n
    """)

if not os.name == 'posix':
    print(f"""
{ye} _  {ye} _  _  {ye} _   _ 
{ye}| | {ye}| \\| |{ye} | | | |
{ye}| | {ye}| .  |{ye} | |_| |
{ye}|_| {ye}|_|\\_|{ye} |_____| 

Version: 1.1 | Author: 4RI\n
{error}{r} Automation supports only Mac systems
    """)
    time.sleep(1)
    sys.exit()