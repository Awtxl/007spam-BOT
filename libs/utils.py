from requests import Session

def CheckPublicIP():
    try:
        with Session() as ses:
            res = ses.get("https://api.ipify.org/?format=json")
            if (res.status_code == 200):
                return res.json()["ip"]
            return None
    except:
        return None
    pass
    
def IsProxyWorking(proxy):
    try:
        with Session() as ses:
            ses.proxies.update(proxy)
            res = ses.get("https://api.ipify.org/?format=json")
            if (res.status_code == 200):
                if(res.json()["ip"] != CheckPublicIP() and CheckPublicIP != None):
                    return True
            return False
    except:
        return False
    pass

def PrintSuccess(message, username, *argv):
    print("[ OK ] ", end="")
    print("[", end="")
    print(username, end="")
    print("] ", end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")
    pass

# Spam 1
# Do not hurt yourself 2
# Drug 3
# Nudity 4
# Severity 5
# Hate Speech 6
# Harassment and Bullying 7
# Identity Imitation 8
# Age-Free Child 11

def PrintChoices():
    print("""    
    +----------------------------+--------+
    |        Reason              | Numara |
    +----------------------------+--------+
    | Spam                       |      1 |
    | Do not hurt yourself       |      2 |
    | Drug                       |      3 |
    | Nudity                     |      4 |
    | Severity                   |      5 |
    | Hate Speech                |      6 |
    | Harassment and Bullying    |      7 |
    | Identity Imitation         |      8 |
    | Age-Free Child             |     11 |
    +----------------------------+--------+
    """)

def GetInput(message, *argv):
    print("[ ? ] ", end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    return input()

def PrintFatalError(message, *argv):
    print("[ X ] ", end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")
    pass

def PrintError(message, username, *argv):
    print("[ X ] ", end="")
    print("[", end="")
    print(username, end="")
    print("] ", end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")
    pass

def PrintStatus(message, *argv):
    print("[ * ] ", end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")
    pass

def PrintBanner():
    banner = """
  ──▄█████████████████████████▄──
  ▄█▀░█░█░█░░░░░░░░░░░░░░░░░░░▀█▄
  █░░░█░█░█░░░░░░░░░░░░░░█████░░█
  █░░░█░█░█░░░░░░░░░░░░░░█████░░█
  █░░░█░█░█░░░░░░░░░░░░░░█████░░█
  █░░░░░░░░░▄▄▄█████▄▄▄░░░░░░░░░█
  ███████████▀▀░░░░░▀▀███████████
  █░░░░░░░██░░▄█████▄░░██░░░░░░░█
  █░░░░░░░██░██▀░░░▀██░██░░░░░░░█
  █░░░░░░░██░██░░░░░██░██░░░░░░░█
  █░░░░░░░██░██▄░░░▄██░██░░░░░░░█
  █░░░░░░░██▄░▀█████▀░▄██░░░░░░░█
  █░░░░░░░░▀██▄▄░░░▄▄██▀░░░░░░░░█
  █░░░░░░░░░░▀▀█████▀▀░░░░░░░░░░█
  █░░░░007spam BOT░░░░░░░░░░░░░░█
  █░░░░C0d3d By Marwan 007░░░░░░█
  █░░░░Insta :@mrwn.007░░░░░░░░░█
  ▀█▄░░░░░░░░░░░░░░░░░░░░░░░░░▄█▀
  ──▀█████████████████████████▀──
 
    """
    print(banner)
    pass

def LoadUsers(path):
    ret = []
    try:
        with open(path, 'r') as file:
            for line in file.readlines():
                line = line.replace("\n", "").replace("\r","")
                user = line.split(" ")[0]
                password = line.split(" ")[1]
                ret.append({
                    "user": user,
                    "password": password
                })
                pass
            pass
        return ret
    except:
        PrintFatalError("'users.txt' File not found!")
        exit(0)
    pass

def LoadProxies(path):
    ret = []
    try:
        with open(path, 'r') as file:
            for line in file.readlines():
                line = line.replace("\n", "").replace("\r","")
                ip = line.split(":")[0]
                port = line.split(":")[1]
                ret.append({
                    "ip": ip,
                    "port": port
                })
                pass
            pass
        return ret
    except:
        PrintFatalError("'proxy.txt' File not found!")
        exit(0)
    pass
