# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:28:10 2020

@author: hp
"""
import luigi
import luigi.contrib.postgres
from luigi.contrib.postgres import CopyToTable
import requests
import json
from time import strptime
import calendar
class GetCovid(luigi.Task):
    def output(self):
        return luigi.LocalTarget("data/cases.tsv")
    def requires(self):
        return None
    def run(self):
        url = 'https://api.covid19india.org/data.json'
        data = requests.get(url).json()
        with self.output().open('w') as outfile:
            for i in data['cases_time_series']:
                mn = i['date'].strip().split(' ')
                dys = strptime(mn[1], '%B').tm_mon
                if str(calendar.monthrange(2020, dys)[1]) == mn[0]:
                    outfile.write('{casemonth}\t{cases}\t{totaldeceased}\t{totalrecovered}\n'.format(casemonth=mn[1],
                                  cases=i['totalconfirmed'],totaldeceased=i['totaldeceased'],totalrecovered=i['totalrecovered']))
class CasesToDB(CopyToTable):
    host = "localhost"
    database = "corona"
    user = "postgres"
    password = "1234"
    table = "COVIDDATA"
    columns = [("casemonth", "TEXT"),("cases", "TEXT"),("totaldeceased", "TEXT"),("totalrecovered", "TEXT")]
    def requires(self):
        return GetCovid()
if __name__ == '__main__':
    luigi.run(['CasesToDB', '--workers', '1', '--local-scheduler'])
    #luigi.run()
    
    
 
    
