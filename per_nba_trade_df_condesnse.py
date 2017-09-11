# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:24:32 2017

@author: Matthew
"""

import pandas as pd
import json

with open('D:/team_data.json') as path:
        team_data = json.load(path)
        
for year in range(2017,1980,-1):
    print(year)
    
    with open('D:/nba_per_project/pace_team_data/pace_data_'+str(year)+'.json') as path:
        team_data = json.load(path)     

    df = pd.read_csv('D:/nba_per_project/nba_season_data/'+str(year)+'.csv')
    
    tmPace = []
    tmAST = []
    tmFG = []
    
    drop_rows = []
    
    i = 0
    while i < len(df):
        if df['team_id'][i] == 'TOT':
            mp_total = df['mp'][i]
            pace = 0
            tmast = 0
            tmfg = 0
            tmId = ''
            for j in range(i+1,i+len(df[df.id == df['id'][i]])):
                pace += team_data[df['team_id'][j]][0]*df['mp'][j]/mp_total
                tmast += team_data[df['team_id'][j]][1]*df['mp'][j]/mp_total
                tmfg += team_data[df['team_id'][j]][2]*df['mp'][j]/mp_total
                tmId += df['team_id'][j]
                if j != i+len(df[df.id == df['id'][i]])-1:
                    tmId += '/'
                
                drop_rows.append(j)
                
            tmPace.append(pace)
            tmAST.append(tmast)
            tmFG.append(tmfg)
                
            df['team_id'][i] = tmId
            
            i += len(df[df.id == df['id'][i]])
        
        else:
            tmPace.append(team_data[df['team_id'][i]][0])
            tmAST.append(team_data[df['team_id'][i]][1])
            tmFG.append(team_data[df['team_id'][i]][2])
            
            i += 1
            
    df = df.drop(df.index[drop_rows])
        
    df['tmPace'] = pd.Series(tmPace, index=df.index)
    df['tmAST'] = pd.Series(tmAST, index=df.index)
    df['tmFG'] = pd.Series(tmFG, index=df.index)
    
    
    df.to_csv('D:/nba_per_project/nba_season_data_TOT/'+str(year)+'.csv',index=False)

