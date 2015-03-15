
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import requests


# In[2]:

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)


# In[3]:

soup = BeautifulSoup(r.content)


# In[4]:

for row in soup('table'):
    print row


# In[5]:

soup('table')[6]


# In[6]:

print soup('table')[6].find_all('tr')


# In[7]:

for tr in soup('table')[6].find_all('tr',{ "class" : "tcont" }):
    try:
        tds = tr.find_all('td')
        country = str(tds[0])
        boys = str(tds[7])
        girls = str(tds[10])
        country = country[country.find('>')+1:country.find('</')]
        boys_years = int(boys[boys.find('>')+1:boys.find('</')])
        girls_years = int(girls[girls.find('>')+1:girls.find('</')])
        print country, boys_years, girls_years
    except:
        pass
    


# In[8]:

import pandas as pd


# In[9]:

columns = ['Country','Boys_Years','Girls_years']


# In[10]:

df = pd.DataFrame(columns=columns)


# In[11]:

df


# In[12]:

df_list = []
for tr in soup('table')[6].find_all('tr',{ "class" : "tcont" }):
    try:
        tds = tr.find_all('td')
        country = str(tds[0])
        boys = str(tds[7])
        girls = str(tds[10])
        country = country[country.find('>')+1:country.find('</')]
        boys_years = int(boys[boys.find('>')+1:boys.find('</')])
        girls_years = int(girls[girls.find('>')+1:girls.find('</')])
        df_list.append([country, boys_years, girls_years])
    except:
        pass
print df_list


# In[13]:

df = pd.DataFrame(df_list, columns=columns)


# In[14]:

df.mean(), df.min(), df.max()


# In[15]:

df


# In[16]:

df.plot()


# In[17]:

(df['Boys_Years']-df['Girls_years']).plot()


# In[35]:

import csv

df_gdp_list = []

with open('ny.gdp.mktp.cd_Indicator_en_csv_v2/ny.gdp.mktp.cd_Indicator_en_csv_v2.csv','rU') as inputFile:
    next(inputFile) # skip the first two lines
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        #print line[0] + '","'.join(line[42:-5])
        #print line[0] + line[50]
        try:
            country = line[0]
            gdp = float(line[50])
            df_gdp_list.append([country,gdp])
        except:
            pass
            
print df_gdp_list


# In[154]:

df_gdp = pd.DataFrame(df_gdp_list, columns=["Country","GDP"])
log(df_gdp['GDP'])


# In[156]:

df_gdp['Log_GDP']=0.0
df_gdp['Log_GDP'] = log(df_gdp['GDP'])
df['GDP']=0.0
df['Log_GDP']=0.0
df


# In[157]:

for i in range(len(df['Country'])):
    for j in range(len(df_gdp['Country'])):
        if (df['Country'][i] == df_gdp['Country'][j]):
            print df['Country'][i], df_gdp['Country'][j] 
            df['GDP'][i]=df_gdp['GDP'][j]
            df['Log_GDP'][i]=df_gdp['Log_GDP'][j]


# In[158]:

df


# In[159]:

for i in range(len(df['Country'])):
    for j in range(len(df_gdp['Country'])):
        if ((df['Country'][i] in df_gdp['Country'][j]) or (df_gdp['Country'][j] in df['Country'][i])) and (df['Country'][i] != df_gdp['Country'][j]):
            if df['Country'][i] in ['Congo','Dominica','Dominican Republic','Guinea','Guinea-Bissau','Niger','Nigeria']:
                pass
            elif df_gdp['Country'][j]=='Ireland':
                pass
            else:
                print df['Country'][i], df_gdp['Country'][j] 
            df['GDP'][i]=df_gdp['GDP'][j]
            df['Log_GDP'][i]=df_gdp['Log_GDP'][j]


# In[160]:

df


# In[161]:

df_clean=df


# In[162]:

df_clean=df_clean[df_clean['GDP']>0]


# In[163]:

df_clean


# In[164]:

df_clean.plot()


# In[166]:

a = pd.scatter_matrix(df_clean, alpha=0.05, figsize=(10,10))


# In[170]:

import statsmodels.formula.api as sm
X = df_clean['Log_GDP']

Y = df_clean.Boys_Years

result = sm.OLS( Y, X ).fit()
result.summary()


# In[171]:

res = sm.ols(formula='Boys_Years ~ Log_GDP', data=df_clean).fit()
print res.params
print res.summary()


# In[173]:

res = sm.ols(formula='Girls_years ~ Log_GDP', data=df_clean).fit()
print res.params
print res.summary()


# In[ ]:



