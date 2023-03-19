import re 
import requests

content = requests.get('https://www.wunderground.com/history/daily/it/brescia/LIPO/date/2017/1/1').content
print(content)
#write to a text file
#look for an int after this class="ng-star-inserted"> number <

pattern = re.compile(r'.*class="ng-star-inserted>(\d+).*')

#find all the matches in the table
MaxT = pattern.findall(str(content))
print('MaxT: ', MaxT)

key =  '45da8e9749b589b7be27c13e3a9061b'
#url = 'http://api.weatherstack.com/historical?access_key=f006e7724397a1b0197ab3707b71c7b6&query=NewYork&historical_date=2017-01-01;2018-12-31&hourly=24'

http://api.weatherstack.com/autocomplete?access_key=45da8e9749b589b7be27c13e3a9061b&query=brescia