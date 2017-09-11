# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:10:11 2017

@author: Matthew
"""

from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd
import numpy as np

def pace_data_scrape(url):
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    html = req.content
    soup = BeautifulSoup(html,'html.parser')
    
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    
    for comment in comments:
        if '<div class="overthrow table_container" id="div_misc_stats">' in comment:
            pace_soup = BeautifulSoup(comment, "lxml")
        if '<div class="overthrow table_container" id="div_team-stats-base">' in comment:
            stats_soup = BeautifulSoup(comment, "lxml")
    
    tr_list1 = pace_soup.find_all('tr')

    team_dict = {}
    
    for tr in tr_list1:
        if tr.find('a') != None:
            if '/teams/' in tr.find('a')['href']:
                team = tr.find('a')['href'].split('/')[2]
                pace = tr.find('td', {'data-stat':'pace'}).string
                team_dict[team] = [float(pace)]
        
    tr_list2 = stats_soup.find_all('tr')    
    for tr in tr_list2:
        if tr.find('a') != None:
            if '/teams/' in tr.find('a')['href']:
                team = tr.find('a')['href'].split('/')[2]
                ast = tr.find('td', {'data-stat':'ast'}).string
                fg = tr.find('td', {'data-stat':'fg'}).string
                team_dict[team].append(float(ast))
                team_dict[team].append(float(fg))
        
    return team_dict

def scrape_team_data(url):
    
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    html = req.content
    soup = BeautifulSoup(html,'html.parser')
    
    cols = ['team', 'wins', 'losses', 'win_loss_pct', 'pts_per_g', 'opp_pts_per_g', 'srs']
    rows = []
    
    tbody_list = soup.find_all('tbody')
    
    for tbody in tbody_list:
        tr_list = tbody.find_all('tr')
        for tr in tr_list:
            if 'srs' in [item['data-stat'] for item in tr.find_all('td')]: ##this line is a quick fix for maxing sure the tr is a row of data
                row = [tr.find('a')['href'].split('/')[2]]  ## gets team id
                for stat in cols:
                    if tr.find('td', {'data-stat': stat}) != None:
                        row.append(float(tr.find('td', {'data-stat': stat}).string))
                
                rows.append(row)
            
    df = pd.DataFrame(rows,columns=cols)
    
    return df

if __name__ == "__main__":
    
    for year in range(2017,1980,-1):
        print(year)
        
        url = "https://www.basketball-reference.com/leagues/NBA_"+str(year)+".html"
        
        #pace_data = pace_data_scrape(url)
        
        team_df = scrape_team_data(url)
        team_df = team_df.drop_duplicates()
        player_df = pd.read_csv('D:/nba_per_project/nba_PER_calculated_seasons/player_per_data_'+str(year)+'.csv')
        
        team_per_col = []
        weighted_per_col = []
        
        for i in range(len(team_df)):
            team_per_col.append(np.mean(player_df[player_df['team_id'].str.contains(team_df['team'][i])]['PER']))
            weighted_per_col.append(np.mean(player_df[player_df['team_id'].str.contains(team_df['team'][i])]['PER']*player_df[player_df['team_id'].str.contains(team_df['team'][i])]['mp']/sum(player_df[player_df['team_id'].str.contains(team_df['team'][i])]['mp'])))
            
        team_df['mean_PER'] = pd.Series(team_per_col, index=team_df.index)
        team_df['mean_PER_weighted'] = pd.Series(weighted_per_col, index=team_df.index)
        
        team_df.to_csv('D:/nba_per_project/team_data/team_data_'+str(year)+'.csv')
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    