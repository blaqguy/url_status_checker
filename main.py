import requests
import configparser
from flask import Flask, render_template
from threading import Thread
import time
import notify_slack

config = configparser.ConfigParser()
config.read('config.ini')
urls = [config['sites'][key] for key in config['sites']]
bad_sites = [] #empty list used to store the bad sites.
good_sites = []


def site_status():
    while True:
        for url in urls:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code != 200 and url in bad_sites:
                    print(f"{url}, is already down, no action")
                elif r.status_code != 200:
                    print(f"{url}, is down, adding to bad_sites")
                    bad_sites.append(url)
                    good_sites.remove(url)
                elif r.status_code == 200 and url in bad_sites:
                    print(f"{url}, is back up")
                    bad_sites.remove(url)
                    good_sites.append(url)
                elif r.status_code == 200 and url in good_sites:
                    print(f"{url}, is good, no action")
                else:
                    print(f"{url}, is good, adding to good_sites")
                    good_sites.append(url)
                    #time.sleep(10)
            except requests.ConnectionError:
                if url in bad_sites:
                    print(url + "already added to bad sites list, skipping")
                else:
                    bad_sites.append(url)
                    good_sites.remove(url)



app = Flask(__name__)

@app.route("/")
def statuspage():
    return render_template('layout.html', good_sites=good_sites, bad_sites=bad_sites)

#@app.route('/admin')
#def content():
#	text = open('config.ini', 'r+')
#	content = text.read()
#	text.close()
#	return render_template('contents.html', text=content)    



if __name__ == '__main__':
    Thread(target=app.run).start()

t1 = Thread(target = site_status)
t1.start()
t2 = Thread(target = notify_slack.run_checks())
t2.start()
