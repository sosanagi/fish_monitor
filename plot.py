#import psycopg2 as pg
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, timedelta
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import tkinter as tk
import time

import temp_sql
import feed_sql

#plt.rcParams.update({'figure.max_open_warning': 0})

def read_data():
    data=temp_sql.select()

    r_data = [ (x,datetime.fromtimestamp(y)) for (x,y) in data[:]]
    df = pd.DataFrame(r_data, columns=['temp','date'])

    df['date'] = pd.to_datetime(df['date'])

    df = df.set_index('date')

    temp_plot(df)

def temp_plot(df):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df)

    xmin = datetime.now() - timedelta(days=1)
    xmax = datetime.now() + timedelta(minutes=15)
    temp_min = df["temp"].min()
    temp_max = df["temp"].max()
    ymin = temp_min - (5 - (int(temp_min) % 5) + (temp_min - int(temp_min)) )
    ymax = temp_max + (5 - (temp_max % 5))
    plt.xlim([xmin,xmax])
    plt.ylim([ymin,ymax])


    ftime_data=feed_sql.select()

    for ftime in ftime_data:
        feed_dt = datetime.fromtimestamp(ftime)
        plt.vlines(feed_dt, ymin, ymax, "red", linestyles='dashed')


    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    plt.grid(which="major",axis='both',color='#999999',linestyle='--')

    daysFmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(daysFmt)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3), tz=None))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 1), tz=None))
    fig.autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Temp (℃)')

    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=60)

    sns.set()

    #plt.grid(which="both")
    #plt.vlines(linestyle=":")
    #plt.xticks(rotation=270)
    #plt.plot(df)
    plt.savefig('canvas.png')
    plt.close()


if __name__ == "__main__":
    while True:
        read_data()
        time.sleep(900)
