if __name__ == '__main__':
	pid2price = {}
	with open('order.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			plist = entries[8]

			plistEntries = plist.split('-')

			for i in range(len(plistEntries)/3):
				pid2price[plistEntries[3*i]] = plistEntries[3*i+2]


	with open('pid2price', 'w') as w:

		for pid in pid2price:
			w.write(pid + ' ' + pid2price[pid] + '\n')


