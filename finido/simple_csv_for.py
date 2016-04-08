# -*- coding: utf-8 -*-



#csvfile = open(csv_file, 'r')

import csv

output_file = open('COMBINED.csv','w')
writer =  csv.writer(output_file)
import os
import glob
files = os.path.dirname(os.path.abspath(__file__))
links = dict()

for fil in glob.glob(os.path.join(files, '*.csv')):
    reader = csv.reader(open(fil))
    for row in reader:
            print(row[11])
            if links.get(row[11],0)==0:
                print(row[11])
                links[row[11]]=1
                
                writer.writerow(row) 
#ne = os.path.join(files, 'Untitled Folder')
#for fil in glob.glob(os.path.join(ne, '*.csv')):
#    reader = csv.reader(open(fil))
#    for row in reader:
#            if links.get(row[1],0)==0:
#                links[row[1]]=1 
#                writer.writerow(row)            
        
 
            
    
    
