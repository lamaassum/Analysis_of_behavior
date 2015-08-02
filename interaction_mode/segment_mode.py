'''
This script is to segment the keystrokes and the plaintext of the conversations to two groups corresponding to the interaction mode (agreement/disagreement) and save them in separate files.
It receives the path of the dataset folder as an argument.
'''
import sys
import os
import csv
############################################################################
path = sys.argv[1]# Get the dataset folder path
dirs = os.listdir(path)
#Arrays to hold the segmentation files (which segment the conversation to agreement/disagreement sections)
c_sg_files = []
r_sg_files = []
for d in dirs:
    if not d.startswith('.'):#ignoring hidden files/directories
		c_sg_files = c_sg_files + [(path+'/'+d+'/'+f) for f in (os.listdir(path+'/'+d)) if not f.startswith('.') and f[f.index('-')+1] == 'C' and f.endswith('SG.csv')]#retrieve the caller segmentation files
		r_sg_files = r_sg_files + [(path+'/'+d+'/'+f) for f in (os.listdir(path+'/'+d)) if not f.startswith('.') and f[f.index('-')+1] == 'R' and f.endswith('SG.csv')]#retrieve the receiver segmentation files

# Arrays to hold the keystrokes
a_log = []
d_log = []
#Arrays to hold the plaintext
a_pt = []
d_pt = []

id = 0
for index in range(len(c_sg_files)):
	id = id + 1
	
	c_file = open(c_sg_files[index],"rU")# read caller segmentation file
	c_intervals = []
	c_reader = csv.reader((line.replace('\0','') for line in c_file), delimiter=",")
	for r in c_reader:
		c_intervals.append((int(r[0]),int(r[1])))
	c_file.close()
	
	
	r_file = open(r_sg_files[index],"rU")# read receiver segmentation file
	r_intervals = []
	r_reader = csv.reader((line.replace('\0','') for line in r_file), delimiter=",")
	for r in r_reader:
		r_intervals.append((int(r[0]),int(r[1])))
	r_file.close()


	c_file = open(c_sg_files[index].replace('SG.csv','IT.csv'),"rU")# read caller individual decision about the items
	c_items = []
	for i, line in enumerate(c_file):
		if i == 1:# to ignore the label row
			list = line.split(',')
			list[-1] = list[-1].replace('\n', '')
			# Reserve the order since the list of items has been written in reverse order
			iterator = reversed(list)
			for item in iterator:
				c_items.append(item)
				c_items = map(int, c_items)
	c_file.close()
	
	r_file = open(r_sg_files[index].replace('SG.csv','IT.csv'),"rU")# read receiver individual decision about the items
	r_items = []
	for i, line in enumerate(r_file):
		if i == 1:# to ignore the label row
			list = line.split(',')
			list[-1] = list[-1].replace('\n', '')
			# Reserve the order since the list of items has been written in reverse order
			iterator = reversed(list)
			for item in iterator:
				r_items.append(item)
				r_items = map(int, r_items)
	r_file.close()
	
	agreement = []
	for i in range(len(c_items)):
		if c_items[i] == r_items[i]:
			agreement.append(1)#agreement
		else:
			agreement.append(0)#disagreement	
	
	c_file = open(c_sg_files[index].replace('-SG',''),"rU")# open the caller log file
	c_log = []
	
	c_reader = csv.reader((line.replace('\0','') for line in c_file), delimiter=",")
	for r in c_reader:
		c_log.append([id]+[r[0],int(r[1])])
	c_file.close()
	
	c_file = open(c_sg_files[index].replace('SG','PT'),"rU")# open the caller plaintext file
	c_pt = []
	
	c_reader = csv.reader((line.replace('\0','') for line in c_file), delimiter=",")
	for r in c_reader:
		c_pt.append([id]+[r[0],int(r[1])])
	c_file.close()	
	
	id = id + 1
	r_file = open(r_sg_files[index].replace('-SG',''),"rU")# open the receiver log file
	r_log = []
	r_reader = csv.reader((line.replace('\0','') for line in r_file), delimiter=",")
	for r in r_reader:
		r_log.append([id]+[r[0],int(r[1])])
	r_file.close()	
	
	r_file = open(r_sg_files[index].replace('SG','PT'),"rU")# open the receiver plaintext file
	r_pt = []
	r_reader = csv.reader((line.replace('\0','') for line in r_file), delimiter=",")
	for r in r_reader:
		r_pt.append([id]+[r[0],int(r[1])])
	r_file.close()
	
	
	c_start = c_log[0][2]-1# start equal to the first timestamp in the caller log minus 1
	if c_intervals[0][0] == 0:# if the first segment is labeled other 
		c_start = c_intervals[0][1]# start equal to the last timestamp in the segment
	
	# segment caller files
	for tup in c_intervals: 
		if tup[0]!= 0:# if the segment not labeled 'other'
			if agreement[tup[0]-1] == 0:# check if they disagree or not in this section
				d_log = d_log+[x for x in c_log if x[2] <= tup[1] and x[2] > c_start]
				d_pt = d_pt+[x for x in c_pt if x[2] <= tup[1] and x[2] > c_start]
			
			else:# if they agree
				a_log = a_log + [x for x in c_log if x[2] <= tup[1] and x[2] > c_start]
				a_pt = a_pt + [x for x in c_pt if x[2] <= tup[1] and x[2] > c_start]
		c_start = tup[1] # start equal to the last timestamp in current segment
		
	r_start = r_log[0][2]-1 # start equal to the first timestamp in the receiver log minus 1
	if r_intervals[0][0] == 0: # if the first segment is labeled other 
		r_start = r_intervals[0][1]# start equal to the last timestamp in the segment
	
	# segment receiver files	
	for tup in r_intervals:
		if tup[0]!= 0:# if the segment not labeled 'other'
			if agreement[tup[0]-1] == 0:# check if they disagree or not in this section
				d_log = d_log + [x for x in r_log if x[2] <= tup[1] and x[2] > r_start]
				d_pt = d_pt + [x for x in r_pt if x[2] <= tup[1] and x[2] > r_start]
			
			else: # if they agree
				a_log = a_log + [x for x in r_log if x[2] <= tup[1] and x[2] > r_start]
				a_pt = a_pt + [x for x in r_pt if x[2] <= tup[1] and x[2] > r_start]
		r_start = tup[1] # start equal to the last timestamp in current segment
		
csv_file = open('agreement-log.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in a_log:
	writer.writerow(entry)
csv_file.close()

csv_file = open('disagreement-log.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in d_log:
	writer.writerow(entry)
csv_file.close()

csv_file = open('agreement-text.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in a_pt:
	writer.writerow(entry)
csv_file.close()

csv_file = open('disagreement-text.csv', "wb")
writer = csv.writer(csv_file, delimiter=',')
for entry in d_pt:
	writer.writerow(entry)
csv_file.close()
		
