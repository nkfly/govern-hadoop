


if __name__ == '__main__':
	pid2sales = {}
	with open('order.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split()
			plist = entries[8]
			plistEntries = plist.split('-')

			for i in range(len(plistEntries)/3):
				if plistEntries[3*i] not in pid2sales:
					pid2sales[plistEntries[3*i]] = 0

				pid2sales[plistEntries[3*i]] += int(plistEntries[3*i+1])*int(plistEntries[3*i+1])

	

