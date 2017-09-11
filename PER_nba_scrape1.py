# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 15:57:33 2017

@author: Matthew
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def season_scrape(url):
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    html = req.content
    soup = BeautifulSoup(html,'html.parser')
    
    cols = ['id','player','pos','age','team_id','g','gs','mp','fg','fga','fg_pct','fg3','fg3a','fg3_pct','fg2',
            'fg2a','fg2_pct','efg_pct','ft','fta','ft_pct','orb','drb','trb','ast','stl','blk','tov','pf','pts']
    rows = []
    
    tr_list = soup.find_all('tr')
    
    for tr in tr_list:
        if 'fg' in [item['data-stat'] for item in tr.find_all('td')]: ##this line is a quick fix for maxing sure the tr is a row of data
            row = [tr.find('td')['data-append-csv']]   ## gets player id
            for td in tr.find_all('td'):
                row.append(td.string)
        
            rows.append(row)
        
    df = pd.DataFrame(rows,columns=cols)
    
    return df
    

if __name__ == "__main__":
    
    for year in range(2017,1980,-1):
        print(year)
        
        url = "https://www.basketball-reference.com/leagues/NBA_"+str(year)+"_totals.html"
        data = season_scrape(url)
        
        data.to_csv(r'D:/nba_per_project/nba_season_data/'+str(year)+'.csv')
        
        time.sleep(1)
    
    
    
