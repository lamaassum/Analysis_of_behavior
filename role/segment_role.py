'''
This script is to segment the keystrokes and the plaintext of the conversations to two groups corresponding to the role (caller or receiver) and save them in separate files.
It receives the path of the dataset folder as an argument.
'''
import sys
import os
import csv
############################################################################
path = sys.argv[1]
dirs = os.listdir(path)
caller_files = []
receiver_files = []
for d in dirs:
    if not d.startswith('.'):#ignoring hidden files/directories
		caller_files = caller_files + [(path+'/'+d+'/'+f) for f in (os.listdir(path+'/'+d)) if not f.startswith('.') and f.count('-') == 1 and f[f.index('-')+1] == 'C']#retrieve the caller log files
		receiver_files = receiver_files + [(path+'/'+d+'/'+f) for f in (os.listdir(path+'/'+d)) if not f.startswith('.') and f.count('-') == 1 and f[f.index('-')+1] == 'R']#retrieve the receiver log files

# Arrays to hold the keystrokes
c_log = []
r_log = []
#Arrays to hold the plaintext
c_pt =[]
r_pt =[]

id = 1
for f in caller_files:
	file = open(f,"rU")
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		c_log.append([id]+[r[0],int(r[1])])
	file.close()
	
	file = open(f.replace('.csv','-PT.csv'),"rU")# open the plaintext file that corresponds to the current log file
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		c_pt.append([id]+[r[0],int(r[1])])
	file.close()
		
	id = id + 1
	
	

id = 1	
for f in receiver_files:
	file = open(f,"rU")
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		r_log.append([id]+[r[0],int(r[1])])
	file.close()
	
	file = open(f.replace('.csv','-PT.csv'),"rU")
	reader = csv.reader((line.replace('\0','') for line in file), delimiter=",")
	for r in reader:
		r_pt.append([id]+[r[0],int(r[1])])
	file.close()	
	
	id = id + 1
	
csv_file = open('caller-log.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in c_log:
	writer.writerow(entry)
csv_file.close()

csv_file = open('receiver-log.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in r_log:
	writer.writerow(entry)
csv_file.close()

csv_file = open('caller-text.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in c_pt:
	writer.writerow(entry)
csv_file.close()

csv_file = open('receiver-text.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in r_pt:
	writer.writerow(entry)
csv_file.close()