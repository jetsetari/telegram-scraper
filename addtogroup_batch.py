"""
ADD TO GROUP
"""
import os
import subprocess
import time
import keyboard

#CONFIG
from config.globals import lg, n, r, w, cy, ye
from config.header import banner

script_path = 'addtogroup_session.py'
current_path = os.getcwd()

def batch_addtogroup():
    while True:
        os.system('clear')
        banner()
        print(w+'=== ADD TO GROUP : BATCH'+n)
        
        print(f'{r}[!]{w} Don\'t click anywhere during the process...')
        tqdm.monitor_interval = 0
        pbar = tqdm(["a", "b", "c", "d"], position=0, leave=True)
        for char in pbar:
            sleep(0.25)
            pbar.set_description("Processing %s" % char, refresh=False)
        os.system(f'open -a Terminal')
        os.system(f'open -a Terminal')
        time.sleep(1.5)
        keyboard.write(f'cd {current_path}')
        keyboard.press_and_release('Enter')
        keyboard.write(f'python3 {script_path} api_id api_hash phone file group scraped_gr')
        #keyboard.write('python' + ' ' + program + ' ' + api_id + ' ' + api_hash + ' ' + phone + ' ' + file + ' ' + group + ' ' + str(scraped_grp))
        keyboard.press_and_release('Enter')
        print(f'{ye}[i]{w} Account xxx launched and going')
        break

if __name__ == "__main__":
    batch_addtogroup()
