import requests
import uuid
import re
from time import sleep
from threading import Thread
import json
import os
from tkinter import messagebox
clear = lambda: os.system('cls') #on Windows System
qq = requests.session()
def close():
    input('Press Enter To close The Programm ... ')
    exit(0)


try:
    open('Account.txt',"r").read().splitlines()
except:
    print('Username\nPassword',file=open('Account.txt',"a"))
uid = str(uuid.uuid4())
count = 0
thrdrun = 0
save = True
mode = ''
email = ''
cok =''
nump = ''
ful_name =''
userACC = ''
passACC = ''
run = False
hd_login = {
    'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US",
    "X-IG-Capabilities": "3brTvw==",
    "X-IG-Connection-Type": "WIFI",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    'Host': 'i.instagram.com'
    }

def get_challenge_choices(last_json):
        choices = []

        if last_json.get("step_name", "") == "select_verify_method":
            choices.append("Challenge received")
            if "phone_number" in last_json["step_data"]:
                choices.append("0 - Phone")
            if "email" in last_json["step_data"]:
                choices.append("1 - Email")

        if last_json.get("step_name", "") == "delta_login_review":
            choices.append("Login attempt challenge received")
            choices.append("0 - It was me")
            choices.append("0 - It wasn't me")

        if not choices:
            choices.append(
                '"{}" challenge received'.format(last_json.get("step_name", "Unknown"))
            )
            choices.append("0 - Default")

        return choices

def challange(login_json):
    global cok
    challenge_url = 'https://i.instagram.com/api/v1/' + login_json["challenge"]["api_path"][1:]
    try:
            b = requests.get(challenge_url ,headers = hd_login ,  cookies=cok)
    except Exception as e:
            print("solve_challenge; {}".format(e))
            return False
    choiccc = get_challenge_choices(b.json())
    for choice in choiccc:
            print(choice)
    code = input("Insert choice : ")
    data_c = {
        'choice' : code,
        '_uuid' : uid ,
        '_uid' : uid , 
        '_csrftoken' : 'missing'
    }
    send_c = requests.post(challenge_url, data=data_c , headers=hd_login,  cookies=cok)
    print("A code has been sent to {}, please check.".format(send_c.json()['step_data']['contact_point']))
    code = input("Insert code: ").strip()
    data_co = {
        'security_code' : code,
        '_uuid' : uid ,
        '_uid' : uid , 
        '_csrftoken' : 'missing'
    }
    send_o = requests.post(challenge_url, data=data_co , headers=hd_login,  cookies=cok)
    send_coj = send_o.json()
    if ('logged_in_user') in send_coj:
        'Logged in :)'
        cok = send_o.cookies
        return True
    return False


def get_info():
    global email , ful_name , nump , hd_login,cok
    try:
        txt = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true" , headers= hd_login , cookies=cok).json()
        email = txt['user']['email']
        nump = txt['user']['phone_number']
        ful_name = txt['user']['full_name']
    except:
        pass

def login_api(username,password):
    global hd_login , cok
    login_url = "https://i.instagram.com/api/v1/accounts/login/"
    data_login = {'uuid': uid,
        'password': password,
        'username': username,
        'device_id': uid,
        'from_reg': 'false',
        '_csrftoken': 'missing',
        'login_attempt_count': '0'}
    loginc = requests.post(login_url,data=data_login, headers=hd_login)
    login1 = loginc.text
    if ('"logged_in_user"') in login1:
        print (f"Logged in as @{username}")
        cok = loginc.cookies
        return True
    elif("Incorrect Username") in login1:
        print("The username you entered doesn't appear to belong to an account. Please check your username and try again.")
        close()
        exit()
    elif('Incorrect password') in login1:
        print("The password you entered is incorrect. Please try again.")
        close()
        exit()
    elif ('"inactive user"') in login1:
        print('Your account has been disabled for violating our terms. Learn how you may be able to restore your account.')
        close()
        exit()
    elif ('checkpoint_challenge_required') in login1:
        cok = loginc.cookies
        return challange(loginc.json())
    else:
        print(login1)
        close()
        exit()

def cheakspamblock():
    global email , userACC ,ful_name ,nump , hd_login , cok
    edit_url = 'https://i.instagram.com/api/v1/accounts/edit_profile/'
    d2 = {
        '_uuid': uid,
        '_uid': uid,
        '_csrftoken' : 'missing',
        'first_name' : ful_name,
        'is_private' : 'false',
        'phone_number' : nump,
        'biography' : '' ,
        'username' : userACC +'.cr1py' ,
        'gender' : '3',
        'email' : email,
        'external_url' : ''
    }
    do = requests.post(edit_url,data=d2,headers=hd_login, cookies=cok).status_code
    if do == 200 :
        return True
    elif do == 429 :
        print("""Spammed block""")
        input('Press Enter To Close The Programm')
        exit(0)





def save(user):
    global passACC , email ,save
    sleep(0.5)
    if save:
        save = False
        try:
            os.mkdir('Swaps')
            print(f'New user : {user}\nPassword : {passACC}\nEmail : {email}',file=open(f'swaps/{user}.txt',"a"))
        except:
            print(f'New user : {user}\nPassword : {passACC}\nEmail : {email}',file=open(f'swaps/{user}.txt',"a"))
        senddic()
    else:
        pass


def edit():
    global run , count , hd_login , d2 , cok
    while True:
        edit_url = 'https://i.instagram.com/api/v1/accounts/edit_profile/'
        while run:
            go = requests.post(edit_url,data=d2,headers=hd_login, cookies=cok).status_code
            if go == 200 :
                run = False
                claimed(d2['username'])
            elif go == 429 :
                print('Spam Block Stop !')
                input('Press Enter To Close Programm .')
                exit(0)
            elif go == 400 :
                count +=1
                print('Waiting For @{} To swap [{}]'.format(d2['username'] , count) , end ="\r")


def claimed(user):
    global passACC , email ,mode
    save(user)
    for x in range(2):
        clear()
        print('Swapped successfully @{}'.format(user))
    if mode == '2':
        input('Press Enter To Show Information .')
        print(f'New user : {user}\nPassword : {passACC}\nEmail : {email}')
        close()
    else:
        close()


def swapapple(user):
    global hd_login , d2 , cok
    edit_url = 'https://i.instagram.com/api/v1/accounts/edit_profile/'
    c = requests.post(edit_url,data=d2,headers=hd_login ,  cookies=cok).text
    if('''"This username isn't available. Please try another."''') in c:
         return True
    elif("This username isn't available."):
        return False



def go():
    global run , d2 , thrd
    threads = []
    for _ in range(int(thrd)):
        t = Thread(target=edit)
        t.start()
        threads.append(t)
    messagebox.showinfo( "Are You Ready ?",f"Swapping @{d2['username']} \n Threads : {thrd}")
    run = True

def ver_n(name):
    clear()
    q = requests.get(f'http://artii.herokuapp.com/make?text={name}')
    print(q.text)

def ak2():
    global userACC ,passACC
    ask = input('[+] Mods : \n[1]  From Account.txt  \n[2]  I will write  \n  [+] :')
    if ask == '1' :
        try:
            listacc = open('Account.txt',"r").read().splitlines()
            userACC = listacc[0]
            passACC = listacc[1]
        except:
                print('Error in info.txt')
                close()
    elif ask == '2':
        userACC = input('Username : ')
        passACC =input('Password : ')
    else:
        clear()
        print('Not recoizable mode !!')
        ak2()




def urres():
    ask = input('[+] Choose : \n[y]  Continue I am responsible  \n[n]  I DO NOT wanna swap  \n  [+] :')
    if ask == 'y' :
        clear()
        return True
    elif ask == 'n':
        clear()
        close()
        return False
    else:
        print('Not recoizable choice !!')
        urres()

clear()

try:
    ver_n(lislog[2])
except:
    q = input('What is The turbo Name : ')
    print(f'{q}',file=open('C:\\info.txt',"a"))
    ver_n(q)

ak2()
clear()

if login_api(userACC , passACC):
    get_info()
    if cheakspamblock() :
        print('''Yor are ready''')
        sleep(2)
    else:
        print('Spammed Block')
        close()
    clear()
    d2 = {
        '_uuid': uid,
        '_uid': uid,
        '_csrftoken' : 'missing',
        'first_name' : ful_name,
        'is_private' : 'false',
        'phone_number' : nump,
        'biography' : '' ,
        'username' :  input('Target : ') ,
        'gender' : '3',
        'email' : email,
        'external_url' : ''
    }
    if swapapple(d2['username']):
        thrd = input('Thread : ')
        go()
    else:
        print('You Cant Swap 14 Day >:')
        if urres():
            thrd = input('Thread : ')
            go()
        else:
            print('Faild To login')
            close()
        

