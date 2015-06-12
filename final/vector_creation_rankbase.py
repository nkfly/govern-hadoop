import heapq
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.svm import SVR

class PriorityQueue:
	def __init__(self):
		self._queue = []
		self._index = 0

	def push(self, item, priority):
		heapq.heappush(self._queue, (priority, self._index, item))
		self._index += 1

	def pop(self):
		return heapq.heappop(self._queue)[-1]
	def hasItem(self):
		return len(self._queue) > 0
	def toList(self):
		l = []
		while self.hasItem():
			l.append(self.pop())
		return l

class Item:
	def __init__(self, token, entries):
		self.token = token
		self.entries = entries
	def __repr__(self):
		return self.token
	def toString(self):
		return str(self.token)

def time_to_priority(day,hour,minute,second):
	return day*86400 + hour*3600 + minute*60 + second

def get_day_hour_minute_second(entries):
	return int(entries[3]), int(entries[4]), int(entries[5]), int(entries[6])

def get_time_period_number():
	return 3

def get_time_period(hour,minute,second):
	return hour/(24/get_time_period_number())

def get_browser_agent_number():
	return 7

def check_browser_agent(agent):
	if 'MSIE' in agent:
		return 0
	elif 'Firefox' in agent:
		return 1
	elif 'Chrome' in agent and 'Android' in agent:
		return 2
	elif 'Chrome' in agent:
		return 3
	elif 'Mobile' in agent and 'Safari' in agent:
		return 4
	elif 'Safari' in agent:
		return 5
	else:
		return 6


def get_pid2sales(orderFile):
	pid2sales = {}
	with open(orderFile, 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			plist = entries[8]
			plistEntries = plist.split('-')

			for i in range(len(plistEntries)/3):
				if plistEntries[3*i] not in pid2sales:
					pid2sales[plistEntries[3*i]] = 0

				pid2sales[plistEntries[3*i]] += int(plistEntries[3*i+1])*int(plistEntries[3*i+2])

	

	return pid2sales

def get_features(viewFile, searchFile, orderFile):
	pid2viewSum = {}
	pid2uniqueViewer = {}
	pid2searchSum = {}
	pid2uniqueSearch = {}

	erUid2priorityQueue = {}

	with open(viewFile, 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			pid = entries[8]

			if pid not in pid2viewSum:
				pid2viewSum[pid] = 0

			pid2viewSum[pid] += 1

			erUid = entries[10]

			if pid not in pid2uniqueViewer:
				pid2uniqueViewer[pid] = {}


			erUid = entries[10]
			pid2uniqueViewer[pid][erUid] = True


			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)


			if erUid not in erUid2priorityQueue:
				erUid2priorityQueue[erUid] = {}
			if pid not in erUid2priorityQueue[erUid]:
				erUid2priorityQueue[erUid][pid] = PriorityQueue()
				

			erUid2priorityQueue[erUid][pid].push(Item(pid, entries), priority)

	with open(searchFile, 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			erUid = entries[10]
			if erUid in erUid2priorityQueue:
				for pid in erUid2priorityQueue[erUid]:
					erUid2priorityQueue[erUid][pid].push(Item('SEARCH', entries), priority)


	for erUid in erUid2priorityQueue:
		for pid in erUid2priorityQueue[erUid]:
			priorityQueue = erUid2priorityQueue[erUid][pid].toList()

			for i in range(len(priorityQueue)):
				if priorityQueue[i].token == 'SEARCH':
					j = i
					while j < len(priorityQueue) and j <= i + 3:
						if 'SEARCH' not in priorityQueue[j].token:
							pid = priorityQueue[j].token

							if pid not in pid2searchSum:
								pid2searchSum[pid] = 0
							pid2searchSum[pid] += 1


							if pid not in pid2uniqueSearch:
								pid2uniqueSearch[pid] = {}

							pid2uniqueSearch[pid][erUid] = True




						 	# it's a pid

						j += 1
	pid2sales = get_pid2sales(orderFile)

	return pid2viewSum, pid2uniqueViewer, pid2searchSum, pid2uniqueSearch, pid2sales


def get_pid2price(orderFile):
	pid2price = {}
	with open(orderFile, 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			plist = entries[8]
			plistEntries = plist.split('-')

			for i in range(len(plistEntries)/3):
				if plistEntries[3*i] not in pid2price:
					pid2price[plistEntries[3*i]] = int(plistEntries[3*i+2])



	return pid2price


def get_pid2cat():
	pid2cat = {}
	layer = [{}, {}, {}, {}, {}, {}]
	with open('./view.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			pid = entries[8]
			cat = entries[9]

			if pid not in pid2cat:
				pid2cat[pid] = (cat.split('-')[-1]).split('_')

			for i in range(len(pid2cat[pid])):
				if pid2cat[pid][i] not in layer[i]:
					layer[i][pid2cat[pid][i]] = len(layer[i])

	return pid2cat, layer


if __name__ == '__main__':

	pid2viewSum, pid2uniqueViewer, pid2searchSum, pid2uniqueSearch, trainPid2sales = get_features('./train_firsthalf/view.csv', './train_firsthalf/search.csv', './train_firsthalf/order.csv')

	test_pid2viewSum, test_pid2uniqueViewer, test_pid2searchSum, test_pid2uniqueSearch, test_pid2sales = get_features('./train_secondhalf/view.csv', './train_secondhalf/search.csv', './train_secondhalf/order.csv')

	y = []
	X = []

	pid2cat, layer = get_pid2cat()
	layerInclude = 2

	pid2price = get_pid2price('./order.csv')


	for pid in pid2viewSum:
		viewSum = 0 if pid not in pid2viewSum else pid2viewSum[pid]
		uniqueViewer = 0 if pid not in pid2uniqueViewer else len(pid2uniqueViewer[pid])
		searchSum = 0 if pid not in pid2searchSum else pid2searchSum[pid]
		uniqueSearch = 0 if pid not in pid2uniqueSearch else len(pid2uniqueSearch[pid])
		sales = 0 if pid not in trainPid2sales else trainPid2sales[pid]

		test_viewSum = 0 if pid not in test_pid2viewSum else test_pid2viewSum[pid]
		test_uniqueViewer = 0 if pid not in test_pid2uniqueViewer else len(test_pid2uniqueViewer[pid])
		test_searchSum = 0 if pid not in test_pid2searchSum else test_pid2searchSum[pid]
		test_uniqueSearch = 0 if pid not in test_pid2uniqueSearch else len(test_pid2uniqueSearch[pid])
		test_sales = 0 if pid not in test_pid2sales else test_pid2sales[pid]

		price = 0 if pid not in pid2price else pid2price[pid]

		if test_sales - sales >= 0:
			y.append(1)
		else:
			y.append(-1)

		x = [test_viewSum-viewSum, test_uniqueViewer-uniqueViewer, test_searchSum-searchSum, test_uniqueSearch-uniqueSearch, price]

		for i in range(layerInclude):
			for j in range( len(layer[i]) ):
				if j == layer[i][pid2cat[pid][i]]:
					x.append(1)
				else:
					x.append(0)

		X.append(x)


			# w.write('0 ' + str(viewSum) + ' ' + str(uniqueViewer) + ' ' + str(searchSum) + ' ' + str(uniqueSearch) + ' ' + str(sales) + '\n')

	# clf = SVR()
	clf = RandomForestClassifier(n_estimators=100, min_samples_split=1, random_state=0)
	clf.fit(X, y)

	pid2viewSum, pid2uniqueViewer, pid2searchSum, pid2uniqueSearch, trainPid2sales = get_features('./view.csv', './search.csv', './order.csv')

	test_pid2viewSum, test_pid2uniqueViewer, test_pid2searchSum, test_pid2uniqueSearch, test_pid2sales = get_features('./view_test.csv', './search_test.csv', './order_test.csv')


	X = []
	for pid in pid2viewSum:
		viewSum = 0 if pid not in pid2viewSum else pid2viewSum[pid]
		uniqueViewer = 0 if pid not in pid2uniqueViewer else len(pid2uniqueViewer[pid])
		searchSum = 0 if pid not in pid2searchSum else pid2searchSum[pid]
		uniqueSearch = 0 if pid not in pid2uniqueSearch else len(pid2uniqueSearch[pid])
		sales = 0 if pid not in trainPid2sales else trainPid2sales[pid]

		test_viewSum = 0 if pid not in test_pid2viewSum else test_pid2viewSum[pid]
		test_uniqueViewer = 0 if pid not in test_pid2uniqueViewer else len(test_pid2uniqueViewer[pid])
		test_searchSum = 0 if pid not in test_pid2searchSum else test_pid2searchSum[pid]
		test_uniqueSearch = 0 if pid not in test_pid2uniqueSearch else len(test_pid2uniqueSearch[pid])
		test_sales = 0 if pid not in test_pid2sales else test_pid2sales[pid]

		price = 0 if pid not in pid2price else pid2price[pid]

		x = [test_viewSum-viewSum, test_uniqueViewer-uniqueViewer, test_searchSum-searchSum, test_uniqueSearch-uniqueSearch, price]

		for i in range(layerInclude):
			for j in range( len(layer[i]) ):
				if j == layer[i][pid2cat[pid][i]]:
					x.append(1)
				else:
					x.append(0)


		X.append(x)

	predictions = clf.predict(X)

	index = 0
	with open('final_result_final', 'w') as w:
		for pid in pid2viewSum:
			w.write(pid + ' ' + str(predictions[index]) + '\n')
			index += 1





















	

				








				








