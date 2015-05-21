import os.path

def month_to_int(month):
	if month == 'Jan': return 1
	elif month == 'Feb': return 2
	elif month == 'Mar': return 3
	elif month == 'Apr': return 4
	elif month == 'May': return 5
	elif month == 'June': return 6
	elif month == 'July': return 7
	elif month == 'Aug': return 8
	elif month == 'Sept': return 9
	elif month == 'Oct': return 10
	elif month == 'Nov': return 11
	elif month == 'Dec': return 12
	else : 
		print month
		exit(-1)



def process_time(time):
	time = time.strip('[')
	entries = time.split(':')
	prev_3 = entries[0].split('/')
	year = int(prev_3[2])
	month = month_to_int(prev_3[1])
	day = int(prev_3[0])
	hour = int(entries[1])
	minute = int(entries[2])
	second = int(entries[3])
	return year,month,day,hour,minute,second

def process_view(info):
	entries = info.split(';')
	if len(entries) != 7:
		return False,None,None,None,None
	uid = entries[2][4:]
	pid = entries[3][4:]
	cat = entries[4][4:].replace(',', '-')
	erUid = entries[5][6:]

	return True,uid,pid,cat,erUid

def process_search(info):
	entries = info.split(';')
	if len(entries) != 7:
		return False,None,None,None,None

	uid = entries[1][4:]
	keywords = entries[3][9:].replace(',', '-')
	name = entries[4][5:]
	erUid = entries[5][6:]

	return True,uid,keywords,name,erUid

def process_cart_or_order(info):
	entries = info.split(';')
	if len(entries) != 6:
		return False,None,None,None

	uid = entries[2][4:]
	plist = entries[3][6:].replace(',', '-')
	erUid = entries[4][6:]

	return True,uid,plist,erUid



def get_act(line):
	if 'act=view' in line:
		return 'view'
	elif 'act=search' in line:
		return 'search'
	elif 'act=order' in line:
		return 'order'
	elif 'act=cart' in line:
		return 'cart'
	else:
		print 'error in line'
		exit(-1)






if __name__ == '__main__':
	test_file = './EHC/EHC_2nd_round_test.log'
	train_file = './EHC/EHC_2nd_round_train.log'

	if not os.path.exists(test_file) or not os.path.exists(train_file):
		print 'please put the EHC folder in the same layer'
		exit(-1)

	"""
	
	203.145.207.188 - - [01/Feb/2015:00:00:00 +0800] "GET /action?;act=view;uid=;pid=0005158462;cat=J,J_007,J_007_001,J_007_001_001;erUid=41ee27d6-5f83-b982-69f9-f378dc9fc11b; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
	27.240.157.47 - - [01/Feb/2015:00:00:08 +0800] "GET /action?;uid=;act=search;keywords=clarks;name=search;erUid=b577f80c-5822-2a80-cf79-31cd3d5f02a; HTTP/1.1" 302 160 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MAAU; .NET4.0C; BRI/2)"
	114.41.4.218 - - [01/Feb/2015:00:00:01 +0800] "GET /action?;act=order;uid=U312622727;plist=0006944501,1,1069;erUid=252b97f1-25bd-39ea-6006-3f3ebf52c80; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; MAARJS)"
	114.39.107.220 - - [01/Feb/2015:00:00:17 +0800] "GET /action?;act=cart;uid=U465125065;plist=0022588156,1,1782;erUid=b978558e-cefd-d05f-5fa7-4e4520f89fe5; HTTP/1.1" 302 160 "-" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"

	"""

	v = open('view.csv', 'w')
	v.write('ip,year,month,day,hour,minute,second,uid,pid,cat,erUid,agent\n')
	s = open('search.csv', 'w')
	s.write('ip,year,month,day,hour,minute,second,uid,keywords,name,erUid,agent\n')
	o = open('order.csv', 'w')
	o.write('ip,year,month,day,hour,minute,second,uid,plist,erUid,agent\n')
	c = open('cart.csv', 'w')
	c.write('ip,year,month,day,hour,minute,second,uid,plist,erUid,agent\n')

	statistics = {}
	statistics['view'] = 0
	statistics['search'] = 0
	statistics['order'] = 0
	statistics['cart'] = 0
	sum = 0.0

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




	
	v.close()
	s.close()
	o.close()
	c.close()

	print 'view:' + str(statistics['view']/sum) + ' search:'+ str(statistics['search']/sum) + ' cart:'+ str(statistics['cart']/sum)  + ' order:'+ str(statistics['order']/sum) 
	
		
			



