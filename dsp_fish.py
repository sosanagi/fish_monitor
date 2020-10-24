import tkinter as tk
from tkinter import messagebox
from tkinter import font
from time import *
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
import threading
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

import post
import plot
import feed_sql
import temp_sql
import screen_saver

FONT_SIZE=30
IMG_W = 400
IMG_H = 350
PLOT_INTERVAL = 900


HOST = 'localhost'
PORT = 51000
MAX_MESSAGE = 2048
NUM_THREAD = 2


root = tk.Tk()
root.withdraw()


def main_proc():
    global top
    top = tk.Toplevel(root)
    top.deiconify()
    top.attributes("-fullscreen", True)

    set_frame()
    show_time()
    com_start()
    #img_read()
    plot_img()

def set_frame():
    global now_time,feed_time,now_temp,img_canvas,plot_frame
    std_font = font.Font(family='Helvetica', size=FONT_SIZE, weight='bold')

    main_frame = tk.Frame(top)
    main_frame.grid(columnspan=2)
    sub_frame = tk.Frame(main_frame)
    button_frame = tk.Frame(sub_frame)
    plot_frame = tk.Frame(main_frame)

    title = tk.StringVar()
    title.set('魚モニタ')
    feed_time_title = tk.StringVar()
    feed_time_title.set('最終給餌時')
    meas_title = tk.StringVar()
    meas_title.set('水温図')
    feed_time = tk.StringVar()
    feed_time.set('')
    nt_title = tk.StringVar()
    nt_title.set('現在の水温')
    now_temp = tk.StringVar()
    now_temp.set('')
    now_time = tk.StringVar()
    now_time.set('')

    title_label = tk.Label(main_frame,textvariable=title,font=std_font)
    ftitle_label = tk.Label(main_frame,textvariable=feed_time_title,font=std_font)
    mtitle_label = tk.Label(main_frame,textvariable=meas_title,font=std_font)
    ftime_label = tk.Label(sub_frame,textvariable=feed_time,font=std_font)
    nt_title_label = tk.Label(sub_frame,textvariable=nt_title,font=std_font)
    n_temp_label = tk.Label(sub_frame,textvariable=now_temp,font=std_font)
    #img_canvas = tk.Canvas(main_frame, width=IMG_W, height=IMG_H,bg="black")
    feed_button = tk.Button(button_frame, text='給餌', width=15, height=5, command=input_feed_time)
    cansel_button = tk.Button(button_frame, text='取消', width=15, height=5, command=cansel_feed_time)
    time_label = tk.Label(main_frame,textvariable=now_time,font=std_font)
    close_button = tk.Button(main_frame, text='×',command=on_closing)


    title_label.grid(row=0,column=0,ipadx=100)
    time_label.grid(row=0,column=1,ipadx=100)
    ftitle_label.grid(row=1,column=0,sticky=tk.W)
    mtitle_label.grid(row=1,column=1,sticky=tk.W)
    sub_frame.grid(row=2,column=0,sticky=tk.NW)
    plot_frame.grid(row=2, column=1,sticky=tk.W)
    #img_canvas.grid(row=2, column=1)
    #close_button.grid(row=1,column=0,sticky=tk.SE)

    ftime_label.grid(row=0,column=0,sticky=tk.W,padx=20)
    nt_title_label.grid(row=1,column=0,sticky=tk.W)
    n_temp_label.grid(row=2,column=0,sticky=tk.W,padx=20)
    button_frame.grid(row=3,column=0,sticky=tk.NSEW,columnspan=2)

    feed_button.grid(row=0,column=0,sticky=tk.NSEW,padx=20)
    cansel_button.grid(row=0,column=1,sticky=tk.NSEW,padx=20)



def img_read():
    global fish_img
    read_img = Image.open('NeonTetra.png')
    rimg_w = read_img.width
    rimg_h = read_img.height
    read_img = read_img.resize(( int(rimg_w*(IMG_W/rimg_w)),int(rimg_h*(IMG_H/rimg_w)) ))
    ippy = int((IMG_H - int(rimg_h*(IMG_H/rimg_w))) /2)

    fish_img = ImageTk.PhotoImage(image=read_img)
    img_canvas.create_image(0, ippy, image=fish_img, anchor=tk.NW)

def plot_img():
    fig = plot.read_data()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().config(width=IMG_W,height=IMG_H)
    canvas.get_tk_widget().grid(row=0, column=0,sticky=tk.W)

    top.after(PLOT_INTERVAL*1000, plot_img)

def show_time():
    now_time.set(strftime('%m/%d %H:%M:%S '))
    top.after(1000, show_time)

def input_feed_time():
    msg="time="+str(time())+"\n"
    post.com_send(msg)

def cansel_feed_time():
    feed_sql.delete()
    ftime=feed_sql.select_one()

    date_time = datetime.fromtimestamp(ftime).strftime("%m/%d %H:%M:%S")
    feed_time.set(date_time)


def com_receive():
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.bind ((HOST, PORT))
    except:
        print("PORT already in use. plz re-execute command")
        sleep(3)
        root.quit()
        sys.exit()

    sock.listen (NUM_THREAD)
    print ('receiver ready, NUM_THREAD = ' + str(NUM_THREAD))

    while True:
        try:
            conn,addr = sock.accept()
            mess = conn.recv(MAX_MESSAGE).decode('utf-8')
            conn.close()

            if "stop" in mess:
                break

            mess_list = mess.splitlines()

            get_msg(mess_list,"temp")
            get_msg(mess_list,"time")

        except:
            print('Error')
            break

    sock.close()

def get_msg(list,title):
    l_in = [s for s in list if title in s]

    for l_in_split in l_in:
        if "temp" in l_in_split:
            temp=l_in[0].split("=")[1]
            now_temp.set(temp+" ℃")

            temp_sql.insert(float(temp),time())

        elif "time" in l_in_split:
            ut=l_in[0].split("=")[1]
            feed_sql.insert(ut)
            date_time = datetime.fromtimestamp(float(ut)).strftime("%m/%d %H:%M:%S")
            feed_time.set(date_time)

def com_start():
    th=threading.Thread(target=com_receive)
    th.start()
    th2=threading.Thread(target=screen_saver.start)
    th2.start()

def on_closing():
    post.com_send("stop")
    root.quit()


screen_saver.init()
root.after(0, main_proc)
root.mainloop()
