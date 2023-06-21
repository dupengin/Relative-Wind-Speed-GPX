#d = [{"a" : 1, "b" : 2, "c":3}, {"a" : 1, "b" : 2 ,"c":3}, {"a" : 1, "b" : 2 ,"c":3}] 

#print(int(len(d)/2))

import csv

fileName = 'test_data_0.csv'

with open (fileName) as f:
    reader = csv.reader(f)
    for row in range(1,len(reader)):
        print( row)