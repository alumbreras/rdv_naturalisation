# A script that notifies you when there is a free slot for the naturalisation

A script that periodically queries the website of the prefecture until there is a free slot for a naturalisation rendez-vous. Once the website shows a calendar instead of the typical message prompting you to re-try later, the Marselleise is played so that you can hurry up and complete the process (the script cannot do that for you)  


## Configuration
Install the Python packages required to run the script:
```
pip install -r requirements.txt
```

Install geckodriver, a driver for Selenium (or anyone) to communicate with Gecko, the Firefox engine. We need to place the geckodriver executable in /usr/local/bin or somewhere else as long as it is included in the PATH variable. This is the most painful part for regular users, since the installation is different for Windows, Linux, MacOS.... Here you have some hints:
https://askubuntu.com/questions/851401/where-to-find-geckodriver-needed-by-selenium-python-package

For Mac, you can do:
```
brew install geckodriver
```
The installation folder is `/opt/homebrew/Cellar/geckodriver/0.32.0`


## Run the script
From the command line, go to the folder where you downloaded the project and write
```
python script.py
```