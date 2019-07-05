# A script that helps you get a rendez-vous to ask for French citizenship. 
# It makes a request every N minutes to the Préfecture de la Haute-Garonne 
# Author: alberto (d0t) lumbreras (@t) gmail (d0t) com


# Comments: install geckodriver executable in /usr/local/bin or 
# somewhere else as long as it is included in the PATH variable.
# This is the most painful part for regular users, since the installation 
# is different for Windows, Linux, MacOS.... 
# Here you have some hints:
# https://askubuntu.com/questions/851401/where-to-find-geckodriver-needed-by-selenium-python-package

## Install Selenium, used to control the browser
import subprocess
import sys
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
install('selenium')


import os
import sys
import time 
import random
import numpy as np
import datetime as dt
from subprocess import call
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException


# Adapt this to your case (email, location of sound file...)
# For most regular (Windows) users, you can remove the lines containing SENDMAIL
# it will not send any email, but the song is enough for you to rush over the computer 
# and end the process manually (enter your data and so on)

email = """To: me\n
		   From: me\n
		   Subject: Slot available!\n\n
		   Hurry up!\n
		   http://haute-garonne.gouv.fr/booking/create/7736/2"""

#SENDMAIL    = f"/usr/sbin/ssmtp -v <email@email.net> < {email}"
PLAYSONG    = "aplay ./marseillaise.wav &"
url         = "http://www.haute-garonne.gouv.fr/booking/create/7736/1"
buttons     = ["planning14500", "planning14510", "planning14520", "planning16456", "planning17481"]

# Each minute
TIMEBUTTONS = 120
TIMELOOP = 0
CANDIDATE_MINUTES = range(0,59)
BLOCKED_TIME = 90

# Standard strategy
TIMEBUTTONS = 25
TIMELOOP = 30
CANDIDATE_MINUTES = [0,10,1]
BLOCKED_TIME = 60


# Standard strategy
TIMEBUTTONS = 30
TIMELOOP = 60
CANDIDATE_MINUTES = [10,30,50]
BLOCKED_TIME = 60

while(True):
	call(['pkill', 'firefox'])
	print("Waiting for minute", CANDIDATE_MINUTES)
	while (dt.datetime.now().minute not in CANDIDATE_MINUTES):
		time.sleep(10) 
		continue

	print("*****************************************************")
	print("Openning browser at", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	
	#browser = webdriver.Firefox(proxy=proxy)
	browser = webdriver.Firefox()
	#break
	
	try:
		for i in range(len(buttons)):
			button = buttons[i]
			print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			browser.get(url)
			element = browser.find_element_by_id(button)
			element.click()
			element = browser.find_element_by_name("nextButton")
			element.click()
			print(str(browser.current_url) + "." * np.random.poisson(3,1)[0])

			if(browser.current_url[-1:]=="3"):
				
				# register success
				with open("success.txt", 'a') as f:
					f.write(dt.datetime.now().strftime("yes\t%Y-%m-%d %H:%M:%S") + "\t" + button + "\n")
				
				# send alerts
				os.system(PLAYSONG)
				#os.system(SENDMAIL)		
				break

			# register failure
			with open("success.txt", 'a') as f:
				f.write(dt.datetime.now().strftime("no\t%Y-%m-%d %H:%M:%S") + "\t" + button + "\n")
				
			secs = np.random.poisson(TIMEBUTTONS,1)[0]
			print("- Button", i,  "Next button in", TIMEBUTTONS, "seconds")
			time.sleep(secs) # time between buttons
			
		else:
			# Didn't find a slot in the calendar through any button
			secs = np.random.poisson(TIMELOOP,1)[0]
			print("Next loop in ", TIMELOOP, "seconds")
			time.sleep(secs)
			continue
		
		break

	except Exception as e:
		
		# register success
		with open("success.txt", 'a') as f:
			f.write(dt.datetime.now().strftime("blocked\t%Y-%m-%d %H:%M:%S\n"))
		
		print("Blocked! Close browser and sleep...")
		browser.close()
		
		call(['pkill', 'firefox'])
		time.sleep(BLOCKED_TIME)
		continue

	browser.close()
		
print("End loop because target page has been reached")

