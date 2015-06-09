from sklearn.cross_validation import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import gc
import itertools

def mygrouper(n, iterable):
	args = [iter(iterable)] * n
	return ([e for e in t if e != None] for t in itertools.izip_longest(*args))

def main():
	gc.collect()
	X = []
	y = []
	count = 0
	notZero = 0
	classWeight = {1 : 49, 2 : 49, 3 : 49, 4 : 49}
	with open('vector_final', 'r') as f:
		for line in f:
			entries = line.strip().split()
			y.append(int(entries[0]))
			X.append([ float(entries[i].split(':')[1])    for i in range(1, len(entries))])

			if int(entries[0]) != 0:
				notZero += 1

			count += 1

	print float(notZero)/count




	# X, y = make_blobs(n_samples=10000, n_features=10, centers=100, random_state=0)

	# clf = DecisionTreeClassifier(max_depth=10, min_samples_split=1,random_state=0)
	# scores = cross_val_score(clf, X, y)
	# print scores.mean()    
	print 0                         


	clf = RandomForestClassifier(class_weight=classWeight,n_estimators=100, max_depth=10, min_samples_split=1, random_state=0)
	clf.fit(X, y)
	X = []
	y = []
	gc.collect()
	print 1

	testX = []
	with open('vector_final_test', 'r') as f:
		for line in f:
			entries = line.strip().split()
			testX.append([ float(entries[i].split(':')[1])    for i in range(1, len(entries))])

	
	pid2price = {}
	print 2
	with open('pid2price', 'r') as f:
		for line in f:
			entries = line.strip().split()
			pid2price[entries[0]] = int(entries[1])


	print 3
	# for test_x in testX:
	# 	predictions = clf.predict(testX)

	pid2sales = {}
	# print 4
	index = 0
	with open('test_map', 'r') as f:
		for test_xs in mygrouper(100000, testX):
			predictions = clf.predict( test_xs )
			index += 1
			print index

			for prediction in predictions:
				line = f.readline()
				pid = line.strip()
				if pid not in pid2sales:
					pid2sales[pid] = 0

				if pid in pid2price:
					pid2sales[pid] += prediction*pid2price[pid]
	print 5
	index = 0
	print_pre = 25
	for w in sorted(pid2sales, key=pid2sales.get, reverse=True):
		print w
		index += 1
		if index >= print_pre:
			break




	# scores = cross_val_score(clf, X, y)
	# print scores.mean()                             


	# clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
	# scores = cross_val_score(clf, X, y)
	# print scores.mean()
	# print 'hello'


if __name__ == '__main__':

	main()