#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:21:47 2023

@author: Frank Baring
"""

# Import packages
import pandas as pd
import os
import re
import requests
import timeout_decorator
from collections import deque

# FUNCTIONS--------------------------------------------------------------------
# Collecting URL content with routine time capped to 3 seconds
@timeout_decorator.timeout(3, timeout_exception=StopIteration)    
def timed_req(my_URL):
    r = requests.get(my_URL)
    if r:
        return r
    else:
        return 0

# Searching for emails in URL content with routine time capped to 10 seconds
@timeout_decorator.timeout(5, timeout_exception=StopIteration)        
def timed_scrape(my_text):
    email = re.findall(r"[a-z\.\-+_]+@[a-z\.\-+_]+\.com", my_text, re.I)
    email = [e for e in email if "wixpress" not in e]
    if email:
        return my_lower(email)
    else:
        return 0 
    
# Remove postfixes
def my_trunc(my_name):
    remove_str = [' LTD',' LTD',' LLC', ' L.L.C', 'INC',' INC',' DDS',' CORP',
                  ' PC', ' PLLC',' P.C',' PLC',' D.D.S.',' O.D',',', '.']
    for string in remove_str:
        try:
            my_name = my_name.replace(string,"")
        except:
            pass
    return my_name

# Clean the company names, removing punctuation
def my_clean(my_name):
    try:
        my_name = re.sub('[^A-Za-z0-9]+','', my_trunc(my_name)).strip().lower()
        return my_name
    except:
        pass
    
# Makes new list of lower case strings
def my_lower(ls):
    new_ls = list()
    for i in ls:
        new_ls.append(i.lower())
    return new_ls

# Remove spaces and rewrite as url
def my_strip(my_list):
    # deque of urls to be returned as [1. business name, 2. url]
    urls = deque()
    for name in my_list:
        try:
            urls.insert(0,[name,'https://www.' +
                                      my_clean(name).replace(" ","") + '.com'])
        except:
            pass
    return urls
    

# Rejoin scraped emails to parent df
def my_export(parent_df, child_list, my_path):
    # Local varaible flag_list for checking dud emails
    flag_list = ['@mail','@email','demo','you','test','example','info','donotreply',
                 'catch','spam','name','support']
    
    # Merge and clean into a final data frame
    email_df = pd.DataFrame(child_list, columns = ['BorrowerName', 'email'])
    df_final = pd.merge(email_df, parent_df, how='inner', on = 'BorrowerName') # Merge
    df_final = df_final.drop_duplicates(subset = ['email'])# Eliminate duplicates
    df_final = df_final.reset_index()# Reset index numbers
    df_final = df_final.drop(['index'], axis=1) # Remove extra index column
    
    # New sheet
    new_sheet = list()
    for element in child_list:
        for email in element[1]:
            check = any(flag in email for flag in flag_list)
            if not check:
                new_sheet.append([element[0],email])
    
    # Edit columns
    email_list = pd.DataFrame(new_sheet, columns = ['Business Name','Email'])
    email_list = email_list.drop_duplicates(subset = ['Email'])# Eliminate duplicates
    # Clean email list names
    for i in range(0,len(email_list)):
        email_list.iloc[i,0] = my_trunc(email_list.iloc[i,0])
    # Export
    if(len(email_list) > 0):
        with pd.ExcelWriter((my_path + 'all_real_estate' + '.xlsx'),mode = "a",
                            engine = "openpyxl", if_sheet_exists="overlay") as writer:  
            df_final.to_excel(writer, sheet_name='Data', index = False)
            email_list.to_excel(writer, sheet_name='Email List', index = False)
        
# Loop for email scraping
def scrape_routine(my_names,my_state,url_num):
    # Declare function-specific variables
    scraped = list()
    i = 1
    hit_count = 0
    # Loop over my_names and scrape emails from URL when possible
    for name in my_names:
        print(str(i) + " state: [" + my_state + "] url_num: " + str(url_num))
        i += 1
        try:
            URL = name[1]
            r = timed_req(URL)
            if r.status_code == 200:
                email = timed_scrape(r.text)
                if email:
                   hit_count += len(set(email))
                   print(name[0] + " [" + my_state + "] "+ str(hit_count))
                   scraped.append([name[0],set(email)])
                else:
                    continue
            else:
                continue
        except:
            continue
    
    return scraped # Return

# ENVIRONMENT SETUP------------------------------------------------------------
# Set directory
root = '/Users/frankbaring/documents/penelope/data/'
os.chdir(root)

# SCRAPE EMAILS----------------------------------------------------------------
# URLs and states to be iterated over
urls = ['https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/dd54d47b-63e9-41c4-ae13-8e12c8ca4ea1/download/public_up_to_150k_12_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/262eb7fc-e074-45ca-a977-f6d8d223e1b3/download/public_up_to_150k_11_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/d2a0b6cd-414a-44af-9c0d-55259e5ebf20/download/public_up_to_150k_10_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/2f6e4ccd-0311-43dc-b721-8bc07f586fa2/download/public_up_to_150k_9_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/35375b26-8bd5-4868-b89d-ab02ccbf2b43/download/public_up_to_150k_8_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/2cea4fbe-2fb5-4307-8d00-5c7203d333f7/download/public_up_to_150k_7_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/03bab509-ad0f-4dbd-88f1-99599dbd3dfc/download/public_up_to_150k_6_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/f4f85ef0-6279-4e81-baac-eefbbc3ebc2d/download/public_up_to_150k_5_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/a100fcb3-7708-4683-aa63-e5a594264e21/download/public_up_to_150k_4_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/6899d4ff-7f2a-4455-a18f-592118e8e052/download/public_up_to_150k_3_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/b785dfac-7d99-4bc0-9ab2-e87fe855174e/download/public_up_to_150k_2_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/5f700a26-02f9-4d97-94a3-e3c2c43871eb/download/public_up_to_150k_1_230101.csv',
        'https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/2b55e11d-7e75-4bbb-b526-69a06c0c4731/download/public_150k_plus_230101.csv']
# States
my_states = ['CA','CT','IL','NJ','NY','VA']
# Set NAICSCode
my_code = '531' # Real estate

# EXECUTE----------------------------------------------------------------------
# Import data
for i in range(7,len(urls)):
    try:
        my_database = pd.read_csv(urls[i])
    except:
        print("PROBLEM GATHERING DATA FROM URL")
        pass
    for state in my_states:
        # Copy subset of data according to state, industry and number of employees
        df = my_database.copy()
        df = df.astype({'NAICSCode':'string'}) # Change NAICS code column to string
        # Set path
        path = root + state + '/real_estate/'
        # Filter
        df = df[df['BorrowerState'] == state]
        df = df[df['NAICSCode'].str.contains(my_code)]
        # Split main data frame for searching
        names = df.iloc[:,df.columns.get_loc('BorrowerName')]
        # Strip company names and collect URLs
        names = list(my_strip(names))
        scraped_final = scrape_routine(names,state,i)
        # Clean and export
        my_export(my_database,scraped_final,path)


