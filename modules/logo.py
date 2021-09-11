import os
from .check_version import check_version

def logo():
	if os.name == 'nt':
		os.system ('cls')
	else:
		os.system ('clear')
	print(rf"""
    /\                     |  __ \             
   /  \   _ __   ___  _ __ | |__) |_ _ ___ ___ 
  / /\ \ | '_ \ / _ \| '_ \|  ___/ _` / __/ __|
 / ____ \| | | | (_) | | | | |  | (_| \__ \__ \
/_/    \_\_| |_|\___/|_| |_|_|   \__,_|___/___/


				version:{'.'.join(check_version())}
""")