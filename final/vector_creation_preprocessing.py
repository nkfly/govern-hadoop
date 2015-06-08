import heapq

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



if __name__ == '__main__':
	erUid2priorityQueue = {}
	pid2id = {}
	with open('./view.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			pid = entries[8]
			if pid not in pid2id:
				pid2id[pid] = len(pid2id)

			erUid = entries[10]

			if erUid not in erUid2priorityQueue:
				erUid2priorityQueue[erUid] = {}
			if pid not in erUid2priorityQueue[erUid]:
				erUid2priorityQueue[erUid][pid] = PriorityQueue()
				

			erUid2priorityQueue[erUid][pid].push(Item(pid, entries), priority) 


	with open('./search.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			erUid = entries[10]
			if erUid in erUid2priorityQueue:
				for pid in erUid2priorityQueue[erUid]:
					erUid2priorityQueue[erUid][pid].push(Item('SEARCH', entries), priority)


	with open('./order.csv', 'r') as f:
		f.readline();
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			plist = entries[8]
			erUid = entries[9]

			plistEntries = plist.split('-')

			if erUid in erUid2priorityQueue:
				for i in range(len(plistEntries)/3):
					pid = plistEntries[3*i]
					if pid in erUid2priorityQueue[erUid]:
						erUid2priorityQueue[erUid][pid].push(Item('BUY-' + plistEntries[3*i+1], entries), priority)

	with open('vector_final', 'w') as w:
		for erUid in erUid2priorityQueue:
			for pid in erUid2priorityQueue[erUid]:
				priorityQueue = erUid2priorityQueue[erUid][pid]
				# w.write(erUid + ' ' + pid + ' ')

				
				viewTime = 0
				searchTime = 0
				dayOfWeek = -1
				buyCount = 0
				timePeriod = -1
				agent = -1

				while priorityQueue.hasItem():
					item = priorityQueue.pop()
					if 'SEARCH' in item.token:
						searchTime += 1
					elif 'BUY' in item.token:
						buyCount += int(item.token.split('-')[1])
					else:
						viewTime += 1
						dayOfWeek = int(item.entries[3])%7
						day, hour, minute, second = get_day_hour_minute_second(item.entries)
						timePeriod = get_time_period(hour, minute, second)


				w.write(str(buyCount) + ' ') # class

				idDimesion = pid2id[pid]
				index = 1
				# while index <= len(pid2id):
				# 	if index == idDimesion:
				# 		w.write(str(index) + ':1 ' )
				# 	else:
				# 		w.write(str(index) + ':0 ' )
				# 	index += 1


				w.write(str(index) + ':' + str(viewTime) + ' ')
				index += 1
				w.write(str(index) + ':' + str(searchTime) + ' ')
				index += 1

				for i in range(7):
					if dayOfWeek == i:
						w.write(str(index) + ':1 ' )
					else:
						w.write(str(index) + ':0 ' )
					index += 1

				for i in range(get_time_period_number()):
					if timePeriod == i:
						w.write(str(index) + ':1 ' )
					else:
						w.write(str(index) + ':0 ' )
					index += 1

				for i in range(get_browser_agent_number()):
					if agent == i:
						w.write(str(index) + ':1 ' )
					else:
						w.write(str(index) + ':0 ' )
					index += 1
				w.write('\n')

				








				








