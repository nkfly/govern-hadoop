if __name__ == '__main__':
	"""
	01,0006584093
02,0000143511
03,0007082051
04,0005772981
05,0014252066
06,0006323656
07,0004607050
08,0024239865
09,0003425855
10,0004134266
11,0006993652
12,0004862454
13,0009727250002
14,0006270095
15,0014252055
16,0006993663
17,0009727290016
18,0018504861
19,0000143500
20,0024634260
	"""
	top_20_dict = {}
	top_20_dict['0006584093'] = True
	top_20_dict['0000143511'] = True
	top_20_dict['0007082051'] = True
	top_20_dict['0005772981'] = True
	top_20_dict['0014252066'] = True
	top_20_dict['0006323656'] = True
	top_20_dict['0004607050'] = True
	top_20_dict['0024239865'] = True
	top_20_dict['0003425855'] = True
	top_20_dict['0004134266'] = True
	top_20_dict['0006993652'] = True
	top_20_dict['0004862454'] = True
	top_20_dict['0009727250002'] = True
	top_20_dict['0006270095'] = True
	top_20_dict['0014252055'] = True
	top_20_dict['0006993663'] = True
	top_20_dict['0009727290016'] = True
	top_20_dict['0018504861'] = True
	top_20_dict['0000143500'] = True
	top_20_dict['0024634260'] = True

	top_20_list = []
	top_20_list.append('0006584093')
	top_20_list.append('0000143511')
	top_20_list.append('0007082051')
	top_20_list.append('0005772981')
	top_20_list.append('0014252066')
	top_20_list.append('0006323656')
	top_20_list.append('0004607050')
	top_20_list.append('0024239865')
	top_20_list.append('0003425855')
	top_20_list.append('0004134266')
	top_20_list.append('0006993652')
	top_20_list.append('0004862454')
	top_20_list.append('0009727250002')
	top_20_list.append('0006270095')
	top_20_list.append('0014252055')
	top_20_list.append('0006993663')
	top_20_list.append('0009727290016')
	top_20_list.append('0018504861')
	top_20_list.append('0000143500')
	top_20_list.append('0024634260')
	

	pid_dict = {}
	with open('view.csv', 'r') as v:
		v.readline()
		for line in v:
			entries = line.strip().split(',')

			if entries[8] not in pid_dict:
				pid_dict[entries[8]] = 1
			else:
				pid_dict[entries[8]] += 1



	index = 0
	print_pre = 20
	for w in sorted(pid_dict, key=pid_dict.get, reverse=True):
		if w in top_20_dict:
  			print 'in', w, pid_dict[w]
  		else:
  			print 'not in', w, pid_dict[w]
  		index += 1
  		if index >= print_pre:
  			break;
	print len(pid_dict)

	for top_20_pid in top_20_list:
		if top_20_pid in pid_dict:
			print 'viewd', pid_dict[top_20_pid]
		else:
			print top_20_pid, 'not been viewd'

