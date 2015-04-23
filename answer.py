import operator


if __name__ == '__main__':

	pid_to_sales = {}
	with open('EHC_1st_round.log', 'r') as f:
		for line in f:
			entries = line.strip().split(';')
			if 'act=order' in entries[1]:
				plist_string = entries[3]
				assert 'plist' in plist_string
				plist_entries = plist_string.split('=')
				plist = plist_entries[1].split(',')

				for i in range( len(plist)/3 ):
					if plist[3*i] not in pid_to_sales:
						pid_to_sales[plist[3*i]] = float(int(plist[3*i+1])*int(plist[3*i+2]))
					else:
						pid_to_sales[plist[3*i]] += float(int(plist[3*i+1])*int(plist[3*i+2]))


	index = 0
	print_pre = 20
	for w in sorted(pid_to_sales, key=pid_to_sales.get, reverse=True):
  		print w, pid_to_sales[w]
  		index += 1
  		if index >= print_pre:
  			break;



