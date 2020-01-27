from requests import Session
from random import choice

from libs.utils import CheckPublicIP, IsProxyWorking
from libs.utils import PrintStatus, PrintSuccess, PrintError

USER_AGENTS = ["Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0",
"Mozilla/5.0 (Android 4.4; Tablet; rv:41.0) Gecko/41.0 Firefox/41.0",
"Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"]

class InstaClient:
    def __init__(self, user, password, ip, port):
        self.isproxyok = True
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.user_agent = choice(USER_AGENTS)

        self.rur = None
        self.mid = None
        self.csrftoken = None

        self.ses = Session()

        if (self.ip != None and self.port != None):
            self.isproxyok = IsProxyWorking({
                "http": "http://" + self.ip + ":" + self.port,
                "https": "https://" + self.ip + ":" + self.port
            })

            self.ses.proxies.update({
                "http": "http://" + self.ip + ":" + self.port,
                "https": "https://" + self.ip + ":" + self.port
            })

        pass

    def SetDefaultHeaders(self, referer):
        if (referer != None):
            self.ses.headers.update({
                "Referer": referer
            })
        self.ses.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "www.instagram.com",
            "TE": "Trailers",
            "User-Agent": self.user_agent,
            "X-CSRFToken": self.csrftoken,
            "X-IG-App-ID": "1",
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        })
    
    def IsCookiesOK(self):
        if (self.rur == None):
            return False
        if (self.mid == None):
            return False
        if (self.csrftoken == None):
            return False
        
        return True

    def GetAndUpdate(self, url):
        res = self.ses.get(url)
        if (res.status_code == 200):
            self.ses.cookies.update(res.cookies)
            if "rur" in res.cookies.get_dict():
                self.rur = res.cookies.get_dict()["rur"]
            if "mid" in res.cookies.get_dict():
                self.mid = res.cookies.get_dict()["mid"]
            if "csrftoken" in res.cookies.get_dict():
                self.csrftoken = res.cookies.get_dict()["csrftoken"]
        return res

    def PostAndUpdate(self, url, data):
        res = self.ses.post(url, data=data)
        if (res.status_code == 200):
            self.ses.cookies.update(res.cookies)
            if "rur" in res.cookies.get_dict():
                self.rur = res.cookies.get_dict()["rur"]
            if "mid" in res.cookies.get_dict():
                self.mid = res.cookies.get_dict()["mid"]
            if "csrftoken" in res.cookies.get_dict():
                self.csrftoken = res.cookies.get_dict()["csrftoken"]
        return res

    def Connect(self):
        if (self.isproxyok != True):
            PrintError("Proxy does not work! (Proxy:", self.user, self.ip, ":" ,self.port, ")")
            return

        if (self.ip != None and self.port != None):
            PrintSuccess("Proxy working! (Proxy:", self.user ,self.ip, ":" ,self.port, ")")
        self.GetAndUpdate("https://www.instagram.com/accounts/login/")
        if (self.IsCookiesOK() != True):
            PrintError("Cookies could not be received! Try another proxy! (Proxy:", self.user, self.ip, ":", self.port, ")")
            self.isproxyok = False
            return
        pass

    def Login(self):
        if (self.isproxyok != True):
            return

        self.SetDefaultHeaders("https://www.instagram.com/accounts/login/")
        res = self.PostAndUpdate("https://www.instagram.com/accounts/login/ajax/",{
            "username": self.user,
            "password": self.password,
            "queryParams": "{}",
            "optIntoOneTap": "false"
        })
        
        if (res.status_code == 200):
            try:
                obj = res.json()
                if ("message" in obj and obj["message"] == "checkpoint_required"):
                    PrintError("Requires account verification! (URL:", obj["checkpoint_url"], ")")
                    self.isproxyok = False
                    return
                if ("authenticated" in obj and obj["authenticated"] == True and
                "user" in obj and obj["user"] == True):
                    PrintSuccess("Login successful!", self.user)
                    self.isproxyok = True
                    return
                if ("errors" in obj and "error" in obj["errors"]):
                    PrintError("Login failed! Proxy may not be working. (Proxy:", self.user, self.ip, ":", self.port, ")")
                    self.isproxyok = False
                    return
                self.isproxyok = False
            except:
                PrintError("Login failed!", self.user)

        pass
    
    def Spam(self,userid, username, reasonid):
        if (self.isproxyok != True):
            return

        profileURL = "https://www.instagram.com/" + username + "/"
        reportURL = "https://www.instagram.com/users/" + userid + "/report/"

        self.SetDefaultHeaders(profileURL)
        self.GetAndUpdate(profileURL)

        res = self.PostAndUpdate(reportURL, {
            "source_name": "profile",
            "reason": reasonid 
        })

        try:
            obj = res.json()
            if ("description" in obj and "status" in obj):
                if (obj["status"] == "ok" and obj["description"] == "Your reports help keep our community free of spam."):
                    PrintSuccess("Complaint was successfully sent!", self.user)
                    return
            PrintError("Our request to submit a complaint was rejected!", self.user)
        except:
            PrintError("An error occurred while submitting a complaint!", self.user)

        pass
