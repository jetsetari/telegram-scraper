"""
ADD TO GROUP
"""
import os
import subprocess
import sys

#CONFIG
from config.globals import lg, n, r, w, cy, ye
from config.header import banner

api_id = str(sys.argv[1])
api_hash = str(sys.argv[2])
phone = str(sys.argv[3])
file = str(sys.argv[4])
group = str(sys.argv[5])

while True:
	os.system('clear')
	banner()
	print(os.listdir('./members'))
	print(w+f'=== ADDING PEOPLE {api_id}-{api_hash}-{phone}-{file}-{group}'+n)
	input('\nYAYAYYAYA')