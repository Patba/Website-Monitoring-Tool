import re
import threading as thread
import time
import sched
from sys import argv
from urllib.request import urlopen
from smtplib import SMTP
from writer import log_create

scheduler = sched.scheduler(time.time, time.sleep)


def check_nwk_connection():
    """
    Check the internet connection by getting status of google and yahoo.
    They can't be down at the same time, right?
    """
    g = fetch_status('http://google.com')
    a = fetch_status('http://apple.com')
    if g or a:
        return True
    else:
        return False


def fetch_status(url):
    """
    Open rl and check the response
    If else we conclude that the server is down.
    """
    url = add_https(url)
    url_file = urlopen(url)
    response = url_file.code

    if response in (200, 302):
        return True, response
    else:
        return False, response


def email_alert(status):
    """
    It's purpose is to send an email
    :param status: fetches status if down
    :return:
    """
    sender = 'email@email.email'
    password = 'passwordofemail'
    recipient = 'typehere@recipient.mail'
    server = SMTP('your_domain_here:25')
    server.ehlo()
    server.starttls()
    server.login(sender, password)
    headers = ["from: " + sender,
               "subject: " + status,
               "to: " + recipient,
               "content-type: text/html"]
    headers = "\n".join(headers)
    server.sendmail(sender, recipient, headers + "\n" + status)
    server.quit()


def add_https(url):
    """
    Adding https for security
    """
    if not re.match('^http[s]?://', url):
        url = "https://" + url
    return url


def test(url):
    """
    First check the internet connection if it's on then check the requested url.
    """
    if check_nwk_connection():
        site_is_up, response = fetch_status(url)
        if site_is_up:
            print(f"{url} is up!")
            log_create(url, site_is_up, response)
        else:
            status = '%s is down!' % url
            log_create(url, site_is_up, response)
            email_alert(status)
    else:
        print('Network is down!')


def periodic(schld, intv, action, args):
    """
    Scheduler to check server status in intervals.
    """
    schld.enter(intv, 1, periodic,
                (schld, intv, action, args))
    action(args)


if __name__ == '__main__':
    #If you want to use it as a script then you need to open terminal and do "python main.py google.com 60" [python scriptname url interval]
    # site_url = argv[1]
    # interval = int(argv[2])

    site_url = "github.com"
    interval = 1
    periodic(scheduler, interval, test, site_url)

    thread = thread.Thread(target=scheduler.run)
    thread.start()
