import pyautogui
import subprocess
from subprocess import PIPE
import json
import time

f = open("module.json", 'r')
module = json.load(f)
shell_list = module["shell"]

def shell_exc(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    res = proc.stdout

    return res
    #print('{}'.format(res))

def click_position_check():
    try:
        while True:
            x,y = pyautogui.position()
            position = 'X:'+str(x).rjust(4) + ' Y:'+str(y).rjust(4)
            print(position,end='')
            print('\b' * len(position),end='',flush=True)
            pyautogui.sleep(1)

    except KeyboardInterrupt:
        print('\n終了')

def screen_saver():
    res=shell_exc(shell_list["monitor_off"])

    x,y = pyautogui.position()
    tmp_x,tmp_y = x,y

    while True:
        x,y = pyautogui.position()
        if(tmp_x!=x or tmp_y!=y):
            res=shell_exc(shell_list["monitor_on"])
            break

def init():
    res=shell_exc(shell_list["dsp_set"])
    res=shell_exc(shell_list["screensaver_off"])

def start():
    while True:
        res=shell_exc(shell_list["monitor_check"])
        time.sleep(10)
        if res.split("=")[1].splitlines()[0]:
            #print("検知")
            time.sleep(300)
            screen_saver()

def main():
    init()
    shell_exc(shell_list['monitor_on'])

if __name__ == "__main__":
    main()
