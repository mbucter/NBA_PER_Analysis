# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 14:49:36 2017

@author: Matthew
"""

from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd
import numpy as np
import json

def lg_stat_sum(df, stat):
    
    value = 0
    i = 0
    
    while i < len(df):
        value += df[stat][i]
        i += len(df[df.id == df['id'][i]])  ## skipping duplicates
            
    return value

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
    
def return_per_df(min_mp, year):
    df = pd.read_csv(r'D:/nba_per_project/nba_season_data_TOT/'+str(year)+'.csv')
    
    df = df[df['mp'] > min_mp]
    df = df.reset_index(drop=True)
    
    lgFT = lg_stat_sum(df, 'ft')
    lgPF = lg_stat_sum(df, 'pf')
    lgFTA = lg_stat_sum(df, 'fta') 
    lgAST = lg_stat_sum(df, 'ast')
    lgFG = lg_stat_sum(df, 'fg')
    lgPTS = lg_stat_sum(df, 'pts')
    lgFGA = lg_stat_sum(df, 'fga')
    lgORB = lg_stat_sum(df, 'orb')
    lgTO = lg_stat_sum(df, 'tov')
    lgTRB = lg_stat_sum(df, 'trb')
    
    factor = 2/3 - ((.5 * lgAST/lgFG) / (2 * lgFG/lgFT))
    VOP = lgPTS / (lgFGA - lgORB + lgTO + .44 * lgFTA)
    DRBP = (lgTRB - lgORB) / lgTRB
    
    #url = "https://www.basketball-reference.com/leagues/NBA_2017.html"
    
    #team_data structure ->> {team_abbr : [pace, ast, fg]}
    #team_data = pace_data_scrape(url)
    with open('D:/nba_per_project/pace_team_data/pace_data_'+str(year)+'.json') as path:
        team_data = json.load(path)

    lgPace = 0
    for key in team_data:
        lgPace += team_data[key][0]  
    lgPace /= len(team_data)
    
    u_per_array = np.zeros(len(df))

    for i in range(len(df)):
        if df['team_id'][i] != 'TOT':
            tmAST = df['tmAST'][i]
            tmFG = df['tmFG'][i]
           
            uPER = (1/df['mp'][i]) * ( df['fg3'][i] - (df['pf'][i]*lgFT)/lgPF + ((df['ft'][i]/2) * (2 - (tmAST/(3*tmFG)))) + (df['fg'][i] * (2 - (factor*tmAST)/tmFG)) + 2*df['ast'][i]/3 + VOP*(DRBP*(2*df['orb'][i] + df['blk'][i] - .2464*(df['fta'][i] - df['ft'][i]) - (df['fga'][i] - df['fg'][i]) - df['trb'][i]) + (.44*lgFTA*df['pf'][i])/lgPF - (df['tov'][i] + df['orb'][i]) + df['stl'][i] + df['trb'][i] - .1936*(df['fta'][i] - df['ft'][i])) )
            
            u_per_array[i] = uPER
            
        
            
    totPER = 0
    count = 0    
    for i in range(len(df)):
        if df['team_id'][i] != 'TOT':
            totPER += u_per_array[i]
            count += 1
    lguPER = totPER/count
    
    per_array = np.zeros(len(df))
    
    for i in range(len(df)):
        if df['team_id'][i] != 'TOT':
            tmPace = df['tmPace'][i]
            PER = (u_per_array[i]*lgPace/tmPace)*(15/lguPER)
            per_array[i] = PER
            
    df['PER'] = pd.Series(per_array, index=df.index)
        
    return df

if __name__ == "__main__":
    
    for n in range(2017,1980,-1):
        print(n)
        data = return_per_df(300,n)
        data.to_csv('D:/nba_per_project/nba_PER_calculated_seasons/player_per_data_'+str(n)+'.csv')
    
    
    
    