import os.path
import csv
if __name__ == '__main__':
	test_file = './EHC/test.log'
	train_file = './EHC/train.log'

	if not os.path.exists(test_file) or not os.path.exists(train_file):
		print 'please put the EHC folder in the same layer'
		exit(-1)
	
	directory_file = './train_secondhalf'
	if not os.path.exists(directory_file):
		os.makedirs(directory_file)
	
	directory_file = './train_firsthalf'
	if not os.path.exists(directory_file):
		os.makedirs(directory_file)
	"""
	
	203.145.207.188 - - [01/Feb/2015:00:00:00 +0800] "GET /action?;act=view;uid=;pid=0005158462;cat=J,J_007,J_007_001,J_007_001_001;erUid=41ee27d6-5f83-b982-69f9-f378dc9fc11b; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
	27.240.157.47 - - [01/Feb/2015:00:00:08 +0800] "GET /action?;uid=;act=search;keywords=clarks;name=search;erUid=b577f80c-5822-2a80-cf79-31cd3d5f02a; HTTP/1.1" 302 160 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MAAU; .NET4.0C; BRI/2)"
	114.41.4.218 - - [01/Feb/2015:00:00:01 +0800] "GET /action?;act=order;uid=U312622727;plist=0006944501,1,1069;erUid=252b97f1-25bd-39ea-6006-3f3ebf52c80; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; MAARJS)"
	114.39.107.220 - - [01/Feb/2015:00:00:17 +0800] "GET /action?;act=cart;uid=U465125065;plist=0022588156,1,1782;erUid=b978558e-cefd-d05f-5fa7-4e4520f89fe5; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"

	"""

	v = open('view.csv', 'r')
	#v.write('ip,year,month,day,hour,minute,second,uid,pid,cat,erUid,agent\n')
	s = open('search.csv', 'r')
	#s.write('ip,year,month,day,hour,minute,second,uid,keywords,name,erUid,agent\n')
	o = open('order.csv', 'r')
	#o.write('ip,year,month,day,hour,minute,second,uid,plist,erUid,agent\n')
	c = open('cart.csv', 'r')
	#c.write('ip,year,month,day,hour,minute,second,uid,plist,erUid,agent\n')
	v1 = open('./train_firsthalf/view.csv', 'w')	
	v2 = open('./train_secondhalf/view.csv', 'w')
	s1 = open('./train_firsthalf/search.csv', 'w')
	s2 = open('./train_secondhalf/search.csv', 'w')
	o1 = open('./train_firsthalf/order.csv', 'w')
	o2 = open('./train_secondhalf/order.csv', 'w')
	c1 = open('./train_firsthalf/cart.csv', 'w')
	c2 = open('./train_secondhalf/cart.csv', 'w')

	statistics = {}
	statistics['view'] = 0
	statistics['search'] = 0
	statistics['order'] = 0
	statistics['cart'] = 0
	sum = 0.0
	
	#reader = csv.DictReader(v)
	for items in range(4):
		if items == 0:
			x = v
			x1 = v1
			x2 = v2
		elif items == 1:
			x = s
			x1 = s1
			x2 = s2
		elif items == 2:
			x = o
			x1 = o1
			x2 = o2
		else:
			x = c
			x1 = c1
			x2 = c2	
		line_number = 0
		train_or_val = 0
		for row in csv.reader(x):
			body=''
			length = len(row)
			for i in range(length-1):
				body = body + row[i] + ','
			body = body + row[length-1] + '\n'
			if train_or_val==0 and line_number > 0:
				if int(row[3]) > 16:
					train_or_val = 1
			if line_number == 0:
				x1.write(body)
				x2.write(body)
			elif train_or_val == 0:
		 		x1.write(body)
			else:
				x2.write(body)
			line_number = line_number + 1
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
	v.close()
	s.close()
	o.close()
	c.close()

#print 'view:' + str(statistics['view']/sum) + ' search:'+ str(statistics['search']/sum) + ' cart:'+ str(statistics['cart']/sum)  + ' order:'+ str(statistics['order']/sum) 
	
		
			



