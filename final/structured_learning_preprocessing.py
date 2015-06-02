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
	def __init__(self, token):
		self.token = token
	def __repr__(self):
		return self.token
	def toString(self):
		return str(self.token)

def time_to_priority(day,hour,minute,second):
	return day*86400 + hour*3600 + minute*60 + second

def get_day_hour_minute_second(entries):
	return int(entries[3]), int(entries[4]), int(entries[5]), int(entries[6])



if __name__ == '__main__':
	erUid2priorityQueue = {}
	with open('./view.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			pid = entries[8]
			erUid = entries[10]

			if erUid not in erUid2priorityQueue:
				erUid2priorityQueue[erUid] = PriorityQueue()

			erUid2priorityQueue[erUid].push(Item(pid), priority) 


	with open('./search.csv', 'r') as f:
		f.readline()
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			erUid = entries[10]
			if erUid not in erUid2priorityQueue:
				erUid2priorityQueue[erUid] = PriorityQueue()

			erUid2priorityQueue[erUid].push(Item('SEARCH'), priority)

	with open('./order.csv', 'r') as f:
		f.readline();
		for line in f:
			entries = line.strip().split(',')
			day, hour, minute, second = get_day_hour_minute_second(entries)
			priority = time_to_priority(day,hour,minute,second)

			plist = entries[8]
			erUid = entries[9]

			if erUid not in erUid2priorityQueue:
				erUid2priorityQueue[erUid] = PriorityQueue()

			erUid2priorityQueue[erUid].push(Item(plist), priority)
	with open('structsvm.sentence', 'w') as w:
		for erUid in erUid2priorityQueue:
			priorityQueue = erUid2priorityQueue[erUid]
			w.write(erUid + ' ')

			while priorityQueue.hasItem():
				w.write(priorityQueue.pop().toString() + ' ' )
			w.write('\n')








