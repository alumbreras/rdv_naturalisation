import os
import time 
import numpy as np
import datetime as dt
from subprocess import call
from selenium import webdriver

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

# Message to log when success, fail, or blocked.
MSG_FREE_SLOT_YES = "free_slot_yes"
MSG_FREE_SLOT_NO = "free_slot_no"
MSG_BLOCKED = "blocked"



# Notification: e-mail
# For Windows, see https://www.howtogeek.com/120011/stupid-geek-tricks-how-to-send-email-from-the-command-line-in-windows-without-extra-software/
EMAIL_ADDRESS = "alberto.lumbreras+spam@gmail.com" # Insert your e-mail
EMAIL_CONTENT = f"""To: me\n
					From: me\n
					Subject: Slot available!\n\n
					Hurry up!\n
					{URL_2nd}"""
SENDMAIL    = f"/usr/sbin/ssmtp -v <{EMAIL_ADDRESS}> < {EMAIL_CONTENT}"

# Notification: play a song
# For Windows, in some cases it has worked with just 
# PLAYSONG    = "./marseillaise.wav"
# and the VLC reproducer is opened and plays the song
PLAYSONG    = "afplay ./marseillaise.wav &"

# Query strategies (times are in seconds)
# TIMEBUTTONS: if multiple buttons available in the website, time to wait to click next button (prevents being blocked)
# TIMELOOP: once all buttons have been tried, time until next round.
# CANDIDATE_MINUTES: on which minutes (of each hour) you want the script to try.
# BLOCKED_TIME: time to wait until next try once you are blocked.

# Accoring to my logs, the system accepts 
# < 15 queries / minute
# maybe the threshold is 15 queries every 15 mins

TIMEBUTTONS = 0
BLOCKED_TIME = 60*30

# Aggresive strategy. Try each minute.
# This was banned in some prefectures, blocking your future requests for some minutes.
# If this is your case you need to use a less aggressive strategy
# TIMELOOP = 0
# CANDIDATE_MINUTES = range(0,59)

# Standard strategy. Candidate minutes are 10, 30, 50, 
# since I have observed this are the moments when the calendar is freed if there has been some cancelation
TIMELOOP = 60
CANDIDATE_MINUTES = [10,30,50]

# Testing strategy
TIMELOOP = 10
CANDIDATE_MINUTES = range(0,59)

call(['pkill', 'chrome'])
driver = webdriver.Chrome()

while(True):	
	print("Waiting for minute", CANDIDATE_MINUTES)
	while (dt.datetime.now().minute not in CANDIDATE_MINUTES):
		time.sleep(10) 
		continue

	print("*****************************************************")
	print("Openning browser at", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	# Monitor the throughput so that in the key minutes we don't query more than 5 times
	MAX_ATTEMPTS_IN_LAST_MINUTE = 5
	attempts_in_last_minute = 0
	last_minute = dt.datetime.now()

	try:
		for i in range(len(BUTTONS)):
			button = BUTTONS[i]
			print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			driver.get(URL_1st)
			
			element = driver.find_element("id", button)
			element.click()
			element = driver.find_element("name", "nextButton")
			element.click()

			print(str(driver.current_url) + "." * np.random.poisson(3,1)[0])

			if(driver.current_url[-1:]=="3"):
				# register success
				with open("success.txt", 'a') as f:
					f.write(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t" + MSG_FREE_SLOT_YES + "\n")
				
				# send alerts
				os.system(PLAYSONG)
				os.system(SENDMAIL) # comment out this line if you are in Windows, since it won't work	
				
				print("End loop because target page has been reached")
				break

			else: 
				# register failure
				with open("success.txt", 'a') as f:
					f.write(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t" + MSG_FREE_SLOT_NO + "\n")

			attempts_in_last_minute += 1
			if attempts_in_last_minute >= MAX_ATTEMPTS_IN_LAST_MINUTE:
				print("Reached MAX_ATTEMPTS_IN_LAST_MINUTE. 1 minute pause to prevent being blocked.")
				time.sleep(60)
			
			# Reset the counter each minute 
			if (dt.datetime.now() - last_minute).total_seconds() >= 60:
				last_minute = dt.datetime.now()

			secs = np.random.poisson(TIMEBUTTONS,1)[0]
			print("- Button", i,  "Next button in", TIMEBUTTONS, "seconds")
			time.sleep(secs) # time between 
			
		else:
			# Didn't find a slot in the calendar through any button
			secs = np.random.poisson(TIMELOOP,1)[0]
			print("Next loop in ", TIMELOOP, "seconds")
			time.sleep(secs)
			continue

	except Exception as e:
		# register success
		print(e)
		with open("success.txt", 'a') as f:
			f.write(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t" + MSG_BLOCKED + "\n")
		
		print(f"Blocked! Waiting {BLOCKED_TIME} seconds until next round")
		time.sleep(BLOCKED_TIME)
		continue	

