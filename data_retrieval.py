#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 19:16:13 2023

@author: francesc
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
from datetime import timedelta, datetime

def get_dates_between(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return date_list

def get_data(date):
    """
    Parameters
    ----------
    date: string in yyyy-mm-dd format
        date to retreive data from
        
    Returns
    -------
        df with the data corresponding to the date in the list
    """
    date_object = datetime.strptime(date, '%Y-%m-%d')
    yyyy = date_object.year
    mm = date_object.strftime('%m')
    dd = date_object.strftime('%d')

    # Send a request to the URL and get the HTML content
    url = f'https://www.meteosantfeliu.cat/WXDailyHistory.php?ID=ICTSANTF2&month={mm}&day={dd}&year={yyyy}&format=1&graphspan=day'
    response = requests.get(url)
    html_content = response.content
       
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    data=soup.get_text()
    # Convert the data to a list of lists
    rows = [line.split(',') for line in data.strip().split('\n')]
    
    
    # Convert the list of lists to a pandas DataFrame
    df = pd.DataFrame(rows, columns=['Time', 'TemperatureC', 'DewpointC', 'PressurehPa', 'WindDirection', 'WindDirectionDegrees', 'WindSpeedKMH', 'WindSpeedGustKMH', 'Humidity', 'HourlyPrecipMM', 'Conditions', 'Clouds', 'dailyrainMM', 'SolarRadiationWatts/m^2', 'UVIndex', 'SoftwareType', 'DateUTC'])
    
    # Filter out rows with 'DateUTC' in the 'DateUTC' column
    df = df[df['DateUTC'] != 'DateUTC']
    
    # Convert the "DateUTC" column to datetime data type
    df['DateUTC'] = pd.to_datetime(df['DateUTC'], format='%Y-%m-%dT%H:%M:%SZ')
    
    # Convert the "Time" column to datetime data type
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Set the "Time" column as the DataFrame index
    df.set_index('Time', inplace=True)
    
    # Drop the "DateUTC" column as it's no longer needed in the index
    #df.drop(columns='DateUTC', inplace=True)
    
    # Drop rows with 'None' values in the DataFrame
    df = df.dropna()
    
    # Display the DataFrame
    print(df)

    # Convert the "TemperatureC" column to numeric (float) data type
    df['TemperatureC'] = pd.to_numeric(df['TemperatureC'], errors='coerce')
    df['WindDirectionDegrees'] = pd.to_numeric(df['WindDirectionDegrees'], errors='coerce')
    df['Humidity'] = pd.to_numeric(df['Humidity'], errors='coerce')
    return df


import logging
import os
outdir = '/home/francesc/data/meteosantfeliu'
for i in ["09,10,11,12,13,14,15,16,17,18,19,20,21,22"]:    
    # run the stuff
    data=pd.DataFrame()
    string_start_date = '2009-01-01'
    string_end_date = '2009-12-31'
    start_date = datetime.strptime(f'{string_start_date}', '%Y-%m-%d')
    end_date = datetime.strptime(f'{string_end_date}', '%Y-%m-%d')
    date_list = get_dates_between(start_date, end_date)
    
    # Configure the logging
    logging.basicConfig(filename=f'{outdir}_{start_date.strftime("20%y%m%d")}_{end_date.strftime("20%y%m%d")}.log', level=logging.ERROR, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    try:
        data = get_data(date_list[0])
    except Exception as e:
        logging.error(f'Problem with day {date_list[0]}: {e}')
    for date in date_list[1:]:
        try:
            data = pd.concat([data,get_data(date)])
        except Exception as e:
            logging.error(f'Problem with day {date}: {e}')
        s_d = start_date.strftime('20%y%m%d')
        e_d = end_date.strftime('20%y%m%d')
    data.to_csv(f'{outdir}/{s_d}_{e_d}.csv')
    data.to_parquet(f'{outdir}/{s_d}_{e_d}.parquet')

# merge all data in one dataset
pd_i=pd_tmp=pd.DataFrame()
outdir = '/home/francesc/data/meteosantfeliu'
for i in ['09','10','11','12','13','14','15','16','17','18','19','20','21','22']:   
    string_start_date = f'20{i}-01-01'
    string_end_date = f'20{i}-12-31'
    start_date = datetime.strptime(f'{string_start_date}', '%Y-%m-%d')
    end_date = datetime.strptime(f'{string_end_date}', '%Y-%m-%d')
    s_d = start_date.strftime('20%y%m%d')
    e_d = end_date.strftime('20%y%m%d')
    pd_i = pd.read_csv(os.path.join(outdir, f"{s_d}_{e_d}.csv"))
    pd_tmp=pd.concat([pd_tmp, pd_i])
    
