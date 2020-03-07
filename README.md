# url_status_checker
This program checks the status of a list of provided urls, if the url returns anything but a 200 status code, sends a message to defined slack channel(s) and makes an entry on a very simple website hosted through this same program with flask. Once the website starts returning 200 status code, sends another message to slack to notify that website is back up and also updates flask website.


Adding urls and incoming slack webhook:


1)open config.ini


2)paste incoming webhook url into incoming_webhook section, remove the quote


3)add more sites as needed


How to run:


1)pip install -r requirements.txt


2)run main.py



