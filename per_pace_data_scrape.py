# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 13:11:18 2017

@author: Matthew
"""

from per_team_data_scrape import pace_data_scrape
import json
from bs4 import BeautifulSoup
import time

for year in range(2017,1980,-1):
    print(year)
    
    url = 'https://www.basketball-reference.com/leagues/NBA_'+str(year)+'.html'
    
    team_data = pace_data_scrape(url)
    
    with open('D:/nba_per_project/pace_team_data/pace_data_'+str(year)+'.json', 'w') as path:
        json.dump(team_data, path)
        
    time.sleep(1)
    
    