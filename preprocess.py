import sys


if __name__ == '__main__':
	with open('EHC_1st_round.log', 'w') as o:
		with open('preprocess.csv', 'w') as f:
			f.write('pid,sum\n')
			for line in sys.stdin:
				o.write(line)
				if 'act=order' in line:
					entries = line.split(';')
					plist_string = entries[3]
					plist_entries = plist_string.split('=')
					plist = plist_entries[1].split(',')
					for i in range( len(plist)/3 ):
						f.write(plist[3*i] + ',' + str(int(plist[3*i+1])*int(plist[3*i+2])) + '\n')






