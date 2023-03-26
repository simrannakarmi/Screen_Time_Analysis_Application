import datetime as dt
import json
import pandas as pd
class Time:
    f = open('activities.json')
    data =json.load(f)
    # print(act)
    act={'name':[],
         'total_time':[]}
    def total_time(self):
        for i in self.data['activities']:
            # print(i['name'])
            self.act['name'].append(i['name'])
            new_data=dt.timedelta(0,0,0,0,0,0)
            for j in i['time_entries']:
                days = j['days']
                hours = j['hours']
                minutes = j['minutes']
                # print(minutes)
                seconds = j['seconds']
                delta = dt.timedelta(days=days, hours=hours, minutes=minutes,seconds=seconds)
                new_data+=delta
            # print(new_data)
            self.act['total_time'].append(new_data) 
            
        # print(self.act) 
        return self.act
    f.close()

