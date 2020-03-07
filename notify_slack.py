import requests
import pickle 
import datetime
import json 
import time 
import configparser 



config = configparser.ConfigParser()
config.read('config.ini')
slack_webhook = config['slack']['incoming_webhook']

#---Slack Function
def notify_slack(message):
    body = json.dumps({'username': 'Website_Monitor', 'icon_emoji': ':chrislook:', 'text': message})
    payload = requests.post(slack_webhook,data=body, verify=False) #Verify=false was set because CORP and all the janky stuff that happens


#---URL Status
def down(url):
    try:
        current_status_file = pickle.load(open("url_status.p", "rb"))
    except Exception as ex:
        print("The url_status.p file was not found. it will be recreated." + str(ex))
        notify_slack(url + " *is down!* :no_entry:")
        return
    
    if url not in current_status_file:
        notify_slack(url + " *is down!* :no_entry:")
        return
    
    if (url in current_status_file) and (current_status_file[url]['status'] == "up"):
        notify_slack(url + " *is down!* :no_entry:")
    else:
        print("already down, skipping notify")

def back_online(url):
    print("found " + url + " back online.")
    try:
        current_status_file = pickle.load(open("url_status.p", "rb"))
    except Exception as ex:
        print("The url_status.p file was not found. it will be recreated." + str(ex))
        return

    if (url in current_status_file) and (current_status_file[url]['status'] == "down"):
        it_was_down_time = current_status_file[url]['time']
        current_time = datetime.datetime.now()
        notify_slack(url + " *is back online!* :up:, it was down for" + str(current_time - it_was_down_time))
    else:
        print("skipping notifying that the url is online")


#---Execution
def run_checks():
    while True:
        config.read('config.ini')
        url_list = [config['sites'][key] for key in config['sites']]
        #An empty dictionary to store the status of our urls
        url_status = {}
        for url in url_list:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code != 200:
                    print(url + " is down.")
                    down(url)
                    url_status[url] = {'status': "down", 'time': datetime.datetime.now().replace(microsecond=0)}
                else:
                    back_online(url)
                    url_status[url] = {'status': "up", 'time': datetime.datetime.now().replace(microsecond=0)}
                    time.sleep(10)
            except requests.ConnectionError:
                print(url + " is down.")
                down(url)
                url_status[url] = {'status': "down", 'time': datetime.datetime.now().replace(microsecond=0)}

        pickle.dump(url_status, open("url_status.p", "wb"))
