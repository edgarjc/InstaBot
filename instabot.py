from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep, strftime
from random import randint
from datetime import datetime
from time import sleep
import pandas as pd
import logging
import sys
import os.path

## USER VARIABLES 
MAC_CHROME_PROFILE = "/Users/edgar/Library/Application Support/Google/Chrome/Default" #Ex. userpath/Library/Application Support/Google/Chrome/Default}
chromedriver_path = '/Users/edgar/Documents/Development Projects/SimpleInstaBot/chromedriver'
USERNAME = ""
PASSWORD = ""
##############


start_time = datetime.now()

likesLogFile = 'likes_count.log';
total = 0;

# MACOS Only
# Gets cookies from your current chrome profile so you dont have to login everytime
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=" + MAC_CHROME_PROFILE)
options.add_argument('lang=pt-br')

# Change this to your own selenium chromedriver path!
chromeService = Service(chromedriver_path)
webdriver = webdriver.Chrome(service=chromeService, options=options)


sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

""" #TODO: Check if user is logged in, if not
##### UNCOMMENT THE FIRST TIME YOU RUN IT SO IT LOGS IN  
username = webdriver.find_element("name",'username')
# Change with your username
username.send_keys(USERNAME)
password = webdriver.find_element("name",'password')
# Change with your password
password.send_keys(PASSWORD)


try:
    button_login = webdriver.find_element("css selector",'#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button')
except:
    button_login = webdriver.find_element("css selector",'.sqdOP > .qF0y9')
button_login.click()
sleep(60)
##### UNCOMMENT THE FIRST TIME YOU RUN IT SO IT LOGS IN  
 """
 
try:
    savebt = webdriver.find_element("css selector",'#react-root > section > main > div > div > div > div > button')
    savebt.click()
except:
    pass

try:
    notnow = webdriver.find_element("css selector",'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow.click()
except:
	pass

# Change with hashtags you want to use
hashtag_list = ['travel']

prev_user_list = []

d_users = []
tag = -1
likes = 0

for hashtag in hashtag_list:
    print('Currently on ' + '#' + hashtag);
    tag += 1
    # Opens hashtag
    #TODO: If hashtag is like4like do something else
    webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
    sleep(8)

    element = webdriver.find_element("css selector", 'div:nth-child(2) > div > .\_ac7v:nth-child(1) > .\_aabd:nth-child(1) .\_aagw')

    hover = ActionChains(webdriver).move_to_element(element)
    hover.perform()

    # It clicks on first photo to open photo window
    #first_thumbnail = webdriver.find_element("css selector",'.\_abpo')
    first_thumbnail = webdriver.find_element("css selector",'.\_aabd')

    first_thumbnail.click()
    sleep(randint(2,3))    
    
    try:        
        for x in range(1,300):
            # Copies username of user
            """ username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/div/a').text
            print(username)
            d_users.append(username) """
            try:
            # Clicks on like button
                button_like = webdriver.find_element("css selector",'.\_aamw > .\_abl-')
                button_like.click()
                likes += 1
                print(format(likes) + " " + "likes on #" + hashtag)
            except:
                print("Like error");
            # Increaments likes array
            
            sleep(3)
          
            try:
                # Next picture
                webdriver.find_element("css selector",'.\_aaqg .\_ab6-').click()
                sleep(randint(2,4))
            except:
                print("Next picture error");
    except:
        # If error occurres, skip to next hashtag
        print("Oops!", sys.exc_info()[0], "occurred.")
        continue

for n in range(0,len(d_users)):
    prev_user_list.append(d_users[n])
    
""" updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_list.csv'.format(strftime("%Y%m%d-%H%M%S"))) """
#Creates file if not there
if not (os.path.isfile(likesLogFile)): 
    with open(likesLogFile,'a') as f:
        f.write(str(0))

with open(likesLogFile, 'r') as inp:
    content = inp.read()
    total = int(content) + int(likes)
    print(total);

with open(likesLogFile, 'w') as outp:
    outp.write(str(total))
print('Liked {} photos.'.format(likes))

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))