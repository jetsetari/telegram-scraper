"""
ADD TO GROUP : BATCH
"""
import os

#CONFIG
from config.globals import lg, n, r, w, cy, ye, vars_file_path
from config.header import banner

current_path = os.getcwd()

def batchbyid_addtogroup():
    """BATCH BY USER ID"""
    while True:
        os.system('clear')
        banner()
        print(w+'=== BATCH BY USER ID'+n)
        input('\nIn development... Press enter to go back to main menu')
        break

if __name__ == "__main__":
    batchbyid_addtogroup()
