# A script that helps you get a rendez-vous to ask for French citizenship. 
# It makes a request every N minutes to the Préfecture 
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

# List of some known urls from the different préfectures
URL_93_1st = "https://www.seine-saint-denis.gouv.fr/booking/create/13303/1"
URL_93_2nd = "https://www.seine-saint-denis.gouv.fr/booking/create/13303/2"
URL_31_1st = "http://www.haute-garonne.gouv.fr/booking/create/7736/1"
URL_31_2nd = "http://haute-garonne.gouv.fr/booking/create/7736/2"

# We need to click a button whose html id is different in each préfecture.
# We need its id so that our scripts knows where to click.
BUTTONS_31 = ["planning39592"]
BUTTONS_93 = ["planning16622"]

# Select the variables according to your prefecture
URL_1st = URL_93_1st
URL_2nd = URL_93_2nd 
BUTTONS = BUTTONS_93

# Notification variables
EMAIL_ADDRESS = "alberto.lumbreras+spam@gmail.com" # Insert your e-mail
EMAIL_CONTENT = f"""To: me\n
					From: me\n
					Subject: Slot available!\n\n
					Hurry up!\n
					{URL_2nd}"""
SENDMAIL    = f"/usr/sbin/ssmtp -v <{EMAIL_ADDRESS}> < {EMAIL_CONTENT}"
PLAYSONG    = "aplay ./marseillaise.wav &"

# Query strategies (times are in seconds)
# TIMEBUTTONS: if multiple buttons available in the website, time to wait to click next button (prevents being blocked)
# TIMELOOP: once all buttons have been tried, time until next round.
# CANDIDATE_MINUTES: on which minutes (of each hour) you want the script to try.
# BLOCKED_TIME: time to wait until next try once you are blocked.

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

# Aggresive strategy. Try each minute.
# This was banned in some prefectures, blocking your future requests for some minutes.
# If this is your case you need to use a less aggressive strategy
TIMEBUTTONS = 120
TIMELOOP = 0
CANDIDATE_MINUTES = range(0,59)
BLOCKED_TIME = 90 


while(True):
	call(['pkill', 'firefox'])
	print("Waiting for minute", CANDIDATE_MINUTES)
	while (dt.datetime.now().minute not in CANDIDATE_MINUTES):
		time.sleep(10) 
		continue

	print("*****************************************************")
	print("Openning browser at", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	driver = webdriver.Chrome()
	
	try:
		for i in range(len(BUTTONS)):
			button = BUTTONS[i]
			print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			driver.get(URL_1st)

			# New
			element = driver.find_element("id", button)
			element.click()
			element = driver.find_element("name", "nextButton")
			element.click()
			
			# Old
			# element = driver.find_element_by_id(button)
			# element.click()
			# element = driver.find_element_by_name("nextButton")
			# element.click()
			
			print(str(driver.current_url) + "." * np.random.poisson(3,1)[0])

			if(driver.current_url[-1:]=="3"):
				
				# register success
				with open("success.txt", 'a') as f:
					f.write(dt.datetime.now().strftime("yes\t%Y-%m-%d %H:%M:%S") + "\t" + button + "\n")
				
				# send alerts
				os.system(PLAYSONG)
				os.system(SENDMAIL) # comment out this line if you are in Windows, since it won't work	
				break

			# register failure
			with open("success.txt", 'a') as f:
				f.write(dt.datetime.now().strftime("no\t%Y-%m-%d %H:%M:%S") + "\t" + button + "\n")
				
			secs = np.random.poisson(TIMEBUTTONS,1)[0]
			print("- Button", i,  "Next button in", TIMEBUTTONS, "seconds")
			time.sleep(secs) # time between 
			
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

