#make a list of dates from 2017 and 2018 in this format 2017-01-01;2017-01-02;
days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
values = []
years = [2017,2018]
for year in years:
    for i in range(0,12):
        for j in range(1,days_in_month[i]+1):
            #if day is less than 10 add a 0 in front
            if j < 10:
                #if month is less than 10 add a 0 in front
                if i < 10:
                    values.append(str(year)+'-0'+str(i+1)+'-0'+str(j)+';')
                else:
                    values.append(str(year)+'-'+str(i+1)+'-0'+str(j)+';')
            else:
                if i < 10:
                    values.append(str(year)+'-0'+str(i+1)+'-'+str(j)+';')
                else:
                    values.append(str(year)+'-'+str(i+1)+'-'+str(j)+';')
import json
#go through each value and append them all into a string
dates = ''
for i in values:
    dates += i
import requests
stuff = []




import pandas as pd
df = pd.DataFrame(columns=['date','maxtemp','mintemp','sunhour','totalsnow'])
for i in range(0, len(values)):
    input = values[i:i+10]
    inputs = ''
    for each in input:
        inputs += each
    #remove the last semicolon
    ind = input
    inputs = inputs[:-1]

    uri = 'https://api.weatherstack.com/historical?access_key=f006e7724397a1b0197ab3707b71c7b6&query=Brescia&historical_date='+ inputs + '&hourly=24'
    content = requests.get(uri).content
    stuff.append(content)
    

    #now let's parse out what we want using json
    jsonData = json.loads(content)

    for j in range(0, len(ind)-1):
        index = ind[j]
        #take off the semicolon
        index = index[:-1]
        try:
            date = jsonData['historical'][index]['date']
            maxtemp = jsonData['historical'][index]['maxtemp']
            mintemp = jsonData['historical'][index]['mintemp']
            sunhour = jsonData['historical'][index]['sunhour']
            totalsnow = jsonData['historical'][index]['totalsnow']
            df = df.append({'date':date,'maxtemp':maxtemp,'mintemp':mintemp,'sunhour':sunhour,'totalsnow':totalsnow},ignore_index=True)
        except:
            print('error' + index)
            continue
    
 
    i = i + 10


print(df.head(10))
#export to csv
df.to_csv('weather.csv',index=False)
