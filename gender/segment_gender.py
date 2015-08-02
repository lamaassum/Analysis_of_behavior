'''
This script is to segment the keystrokes and the plaintext of the conversations to two groups corresponding to the gender and save them in separate files.
It receives the path of the dataset folder as an argument.
'''
import sys
import os
import csv
############################################################################
path = sys.argv[1]# Get the dataset folder path
dirs = os.listdir(path)
female_files = []
male_files = []
for d in dirs:
    if not d.startswith('.'):#ignoring hidden files/directories
		female_files = female_files + [(path+'/'+d+'/'+f) for f in (os.listdir(path+'/'+d)) if not f.startswith('.') and f.count('-') == 1 and f[f.index('-')+2] == 'F']#retrieve the female log files
		male_files = male_files + [(path+'/'+d+'/'+f) for f in (os.listdir(path+'/'+d)) if not f.startswith('.') and f.count('-') == 1 and f[f.index('-')+2] == 'M']#retrieve the male log files

# Arrays to hold the keystrokes
f_log = []
m_log = []
#Arrays to hold the plaintext
f_pt = []
m_pt = []

id = 1
for f in female_files:
	file = open(f,"rU")
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		f_log.append([id]+[r[0],int(r[1])])
	file.close()
	
	
	file = open(f.replace('.csv','-PT.csv'),"rU")# open the plaintext file that corresponds to the current log file
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		f_pt.append([id]+[r[0],int(r[1])])
	file.close()	
	id = id + 1
	
id = 1	
for f in male_files:
	file = open(f,"rU")
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		m_log.append([id]+[r[0],int(r[1])])
	file.close()
	
	
	file = open(f.replace('.csv','-PT.csv'),"rU")
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		m_pt.append([id]+[r[0],int(r[1])])
	file.close()	
	id = id + 1
csv_file = open('female-log.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in f_log:
	writer.writerow(entry)
csv_file.close()

csv_file = open('male-log.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in m_log:
	writer.writerow(entry)
csv_file.close()

csv_file = open('female-text.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in f_pt:
	writer.writerow(entry)
csv_file.close()

csv_file = open('male-text.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in m_pt:
	writer.writerow(entry)
csv_file.close()