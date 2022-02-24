import sqlite3
import requests
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import zipfile
import wget
import os

def getPL94(database, Exists='drop', Table='PL94', Vintage=2020, State=None, Directory=None):
    if Directory:
        os.chwd(Directory)
    headers='https://www2.census.gov/programs-surveys/decennial/rdo/about/2020-census-program/Phase3/SupportMaterials/2020_PLSummaryFile_FieldNames.xlsx'
    wget.download(headers)
    if State:
        if len(State) == 2:
            stateList = pd.read_csv('https://gist.github.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53', dtype=str)
            State = stateList[stateList['stname'] == State.upper()]
        State = State.replace(' ', '_')
        url = f'https://www2.census.gov/programs-surveys/decennial/{vintage}/data/01-Redistricting_File--PL_94-171/{State}/'
    else:
        url = f'https://www2.census.gov/programs-surveys/decennial/{vintage}/data/01-Redistricting_File--PL_94-171/National/'
    r = requests.get(url)
    res = r.content
    for link in BeautifulSoup(res, parse_only=SoupStrainer('a')):
        if 'zip' in link.contents[0]:
            f = link.contents[0]
    file = f'{url}{f}'
    wget.download(file)
    df_header1 = pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name='2020 P.L. Segment 1 Definitions').dropna(axis=0, how='all').reset_index(drop=True)
    df_header2 = pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name='2020 P.L. Segment 2 Definitions').dropna(axis=0, how='all').reset_index(drop=True)
    df_header3 = pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name='2020 P.L. Segment 3 Definitions').dropna(axis=0, how='all').reset_index(drop=True)
    df_headergeo = pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name='2020 P.L. Geoheader Definitions').dropna(axis=0, how='all').reset_index(drop=True)
    header_replace_1 = {i :None for i in range(0,len(df_header1.index)) }
    header_replace_2 = {i :None for i in range(0,len(df_header2.index)) }
    header_replace_3 = {i :None for i in range(0,len(df_header3.index)) }
    header_replace_geo = {i :None for i in range(0,len(df_headergeo.index)) }
    array = [[df_header1,header_replace_1, '1'],[df_header2,header_replace_2,'2'],[df_header3,header_replace_3,'3'],[df_headergeo,header_replace_geo,'o']]
    for i in array:
        json = i[1]
        header = i[0]
        for key in json.keys():
            json[key] = header.iloc[key][1]
    archive = zipfile.ZipFile(f, 'r')
    csv = []
    for i in archive.infolist():
        temp = archive.open(i)
        fileName = temp.name.split('.')[0]
        fileNum = fileName[-5:][0]
        df = pd.read_csv(temp, sep="|", header=None, low_memory=False ,encoding = "ISO-8859-1")
        for j in array:
            if fileNum == j[2] :
                df = df.rename(columns=j[1])
        df.to_csv(f'{fileName}.csv', index=False)
        csv.append(fileName)
    join_on = ['STUSAB','LOGRECNO']
    df_out = None
    for i in csv:
        if df_out is None:
            df_out = pd.read_csv(f'{i}.csv', low_memory=False, dtype={'FILEID':'str','STUSAB':'str','CHARITER':'str','CIFSN':'str','LOGRECNO':'str'})
            continue
        else:
            df = pd.read_csv(f'{i}.csv', low_memory=False, dtype={'FILEID':'str','STUSAB':'str','CHARITER':'str','CIFSN':'str','LOGRECNO':'str'})
            df_out = df_out.merge(df, on=join_on, suffixes=('', '_y'))
            delt = []
            for k in df_out.columns:
                if '_y' in k:

                    delt.append(k)
            df_out = df_out.drop(columns=delt)
    con = sqlite3.connect(f'{database}.db')
    df_out.to_sql(f'{Table}',con, if_exists=Exists , index=False)
    for i in csv:
        os.remove(f'{i}.csv')