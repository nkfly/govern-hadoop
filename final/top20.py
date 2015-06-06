import os.path
import csv
if __name__ == '__main__':
	test_file = './EHC/EHC_2nd_round_test.log'
	train_file = './EHC/EHC_2nd_round_train.log'

	if not os.path.exists(test_file) or not os.path.exists(train_file):
		print 'please put the EHC folder in the same layer'
		exit(-1)
	
	directory_file = './train_secondhalf'
	if not os.path.exists(directory_file):
		print 'please cutdata first'
		exit(-1)	
	directory_file = './train_firsthalf'
	if not os.path.exists(directory_file):
		print 'lease cutdata first'
		exit(-1)
		"""
	
	203.145.207.188 - - [01/Feb/2015:00:00:00 +0800] "GET /action?;act=view;uid=;pid=0005158462;cat=J,J_007,J_007_001,J_007_001_001;erUid=41ee27d6-5f83-b982-69f9-f378dc9fc11b; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
	27.240.157.47 - - [01/Feb/2015:00:00:08 +0800] "GET /action?;uid=;act=search;keywords=clarks;name=search;erUid=b577f80c-5822-2a80-cf79-31cd3d5f02a; HTTP/1.1" 302 160 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MAAU; .NET4.0C; BRI/2)"
	114.41.4.218 - - [01/Feb/2015:00:00:01 +0800] "GET /action?;act=order;uid=U312622727;plist=0006944501,1,1069;erUid=252b97f1-25bd-39ea-6006-3f3ebf52c80; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; MAARJS)"
	114.39.107.220 - - [01/Feb/2015:00:00:17 +0800] "GET /action?;act=cart;uid=U465125065;plist=0022588156,1,1782;erUid=b978558e-cefd-d05f-5fa7-4e4520f89fe5; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"

	"""

	o = open('order.csv', 'r')
	#o.write('ip,year,month,day,hour,minute,second,uid,plist,erUid,agent\n')
	o1 = open('./train_firsthalf/order.csv', 'r')
	o2 = open('./train_secondhalf/order.csv', 'r')
	
	top20_file_first = open('./train_firsthalf/top20.txt', 'w')
	top20_file_second = open('./train_secondhalf/top20.txt', 'w')
	for j in range(2):
		if j==0:
			read_file = o1
			write_file = top20_file_first
		else:
			read_file = o2
			write_file = top20_file_second
		dic = dict()
		for row in csv.DictReader(read_file):
			plist = row['plist']
			if not plist is '':
				entries = plist.strip().split('-')
				item_length = len(entries)
				for i in range(item_length):
					if i%3 == 0:
						pid = entries[i]	
					elif i%3 == 1:
						quantity = entries[i]
					elif i%3 == 2:
						price = entries[i]
						if pid not in dic:
							dic[pid] = int(quantity)*int(price)
						else:
							dic[pid] += int(quantity)*int(price)
					else:
						print 'plist error'
						exit(-1)
		top20 = 0;
		for key, value in sorted(dic.iteritems(), key=lambda (k,v): (v,k),
				reverse=True):
			if top20 > 19:
				print
				break
			write_file.write(key+":"+str(value)+'\n')
			print "%s: %s" % (key, value)
			top20 += 1
	'''
	with open(train_file, 'r') as f:
		for line in f:
			entries = line.strip().split()

			act = get_act(line)
			if act == 'view':
				isOk,uid,pid,cat,erUid = process_view(entries[6])
				if not isOk:
					continue

				body = uid+','+pid+','+cat+','+erUid
				statistics['view'] += 1
				w = v

			elif act == 'search':
				isOk,uid,keywords,name,erUid = process_search(entries[6])
				if not isOk:
					continue

				body = uid+','+keywords+','+name+','+erUid
				statistics['search'] += 1
				w = s

			elif act == 'order':
				isOk,uid,plist,erUid = process_cart_or_order(entries[6])
				if not isOk:
					continue

				body = uid+','+plist+','+erUid
				statistics['order'] += 1
				w = o
				

			elif act == 'cart':
				isOk,uid,plist,erUid = process_cart_or_order(entries[6])
				if not isOk:
					continue

				body = uid+','+plist+','+erUid
				statistics['cart'] += 1
				w = c



			w.write(entries[0]) #ip
			w.write(',')
			year,month,day,hour,minute,second = process_time(entries[3])
			w.write(str(year)+','+str(month)+','+str(day)+','+str(hour)+','+str(minute)+','+str(second))
			w.write(',')
			
			w.write(body)
			w.write(',')


			w.write(line.strip().strip('"').split('"')[-1]) #agent
			w.write('\n')

			sum += 1




	'''
