# coding=utf-8
#!/usr/bin/env python3

""" 
Before changing the program and publishing it somewhere, please
Please note that this program is under GPLv3 license.
More information:
https://tr.wikipedia.org/wiki/gnu_genel_kamu_lisans%c4%b1
https://www.gnu.org/licenses/quick-guide-gplv3.html
"""

__author__ = "Marwan 007 : @mrwn.007"
__license__ = "GPLv3"
__version__ = "0.1"
__status__ = "being developed"



from time import time, sleep
from random import choice
from multiprocessing import Process

from libs.utils import CheckPublicIP, IsProxyWorking
from libs.utils import PrintStatus, PrintSuccess, PrintError
from libs.utils import PrintBanner, GetInput, PrintFatalError
from libs.utils import LoadUsers, LoadProxies, PrintChoices

from libs.instaclient import InstaClient

USERS = []
PROXIES = []

def MultiThread(username, userid, loginuser, loginpass, proxy, reasonid):
    client = None
    if (proxy != None):
        PrintStatus("[" + loginuser + "]", "Logging into the Account!")
        client = InstaClient(
            loginuser,
            loginpass,
            proxy["ip"],
            proxy["port"]
        )
    else:
        PrintStatus("[" + loginuser + "]", "Logging into the Account!")
        client = InstaClient(
            loginuser,
            loginpass,
            None,
            None
        )
        
    client.Connect()
    client.Login()
    client.Spam(userid, username, reasonid)
    print("")

def NoMultiThread():
    for user in USERS:
        client = None
        if (useproxy):
            proxy = choice(PROXIES)
            PrintStatus("[" + user["user"] + "]", "Logging into the Account!")
            client = InstaClient(
                user["user"],
                user["password"],
                proxy["ip"],
                proxy["port"]
            )
        else:
            proxy = choice(PROXIES)
            PrintStatus("[" + user["user"] + "]", "Logging into the Account!")
            client = InstaClient(
                user["user"],
                user["password"],
                None,
                None
            )
        
        client.Connect()
        client.Login()
        client.Spam(userid, username, reasonid)
        print("")


if __name__ == "__main__":
    PrintBanner()
    PrintStatus("Loading users!")
    USERS = LoadUsers("./users.txt")
    PrintStatus("Loading Proxes!")
    PROXIES = LoadProxies("./proxy.txt")
    print("")

    username = GetInput("The account username you want to complain about:")
    userid = GetInput("The account number you want to complain about:")
    useproxy = GetInput("Do you want to use proxy? [Yes No]:")
    if (useproxy == "Yes"):
        useproxy = True
    elif (useproxy == "No"):
        useproxy = False
    else:
        PrintFatalError("Please just enter 'Yes' or 'No'!")
        exit(0)
    usemultithread = GetInput("Do you want to use multithreading? [Yes / No] (Do not use this feature if you have too many users or if your computer is slow!):")
    
    if (usemultithread == "Yes"):
        usemultithread = True
    elif (usemultithread == "No"):
        usemultithread = False
    else:
        PrintFatalError("Please just enter 'Yes' or 'No'!")
        exit(0)
    
    PrintChoices()
    reasonid = GetInput("Please select one of the reasons for the above complaint (ex: 1 for spam):")

    
    
    
    print("")
    PrintStatus("Starting!")
    print("")

    if (usemultithread == False):
        NoMultiThread()
    else:
        for user in USERS:
            p = Process(target=MultiThread,
                args=(username,
                    userid,
                    user["user"],
                    user["password"],
                    None if useproxy == False else choice(PROXIES),
                    reasonid
                )
            )
            p.start() 
    

    
