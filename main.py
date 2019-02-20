from pathlib import Path
import json
import sys

sizes = {}

def BFS(path: Path) -> float:
	p = {str(path): []}
	size = 0
	try:
		for d in path.iterdir():
			if d.is_file():
				p[str(path)].append(str(d))
				ts = d.stat().st_size
				size += ts
				sizes[str(d)] = ts
			elif d.is_dir():
				tp, ts = BFS(d)
				p[str(path)].append(tp)
				size += ts
				sizes[str(d)] = ts
	except OSError:
		pass
	return p, size

def PrintFile(path, depth):
	print(list(path.keys())[0])
	for p in list(path.values())[0]:
		if type(p) == str:
			for n in range(depth):
				print('  ', end = '')
			print(p)
		elif type(p) == dict:
			for n in range(depth):
				print('  ', end = '')
			PrintFile(p,depth+1)

def PrintSize(path):
	for p in list(path.values())[0]:
		if type(p) == str:
			print(ConvertSize(sizes[p])+'\t'+p)
		elif type(p) == dict:
			print(ConvertSize(sizes[list(p.keys())[0]])+'\t'+list(p.keys())[0])

def PrintSortedSize(path):
	plist = []
	slist = []
	for p in list(path.values())[0]:
		if type(p) == str:
			tp = p
			ts = sizes[p]
		elif type(p) == dict:
			tp = list(p.keys())[0]
			ts = sizes[tp]
		plist.append(tp)
		slist.append(ts)
	for n in range(len(plist)):
		ind = slist.index(max(slist))
		print(ConvertSize(slist[ind])+'\t'+plist[ind])
		slist[ind] = -1

def ConvertSize(size):
	if size < 1024:
		return str(round(size,1))+'B'
	elif size < pow(1024,2):
		return str(round(size/pow(1024,1),1)) + 'KB'
	elif size < pow(1024,3):
		return str(round(size/pow(1024,2),1)) + 'MB'
	elif size < pow(1024,4):
		return str(round(size/pow(1024,3),1)) + 'GB'
	elif size < pow(1024,5):
		return str(round(size/pow(1024,4),1)) + 'TB'
	elif size < pow(1024,6):
		return str(round(size/pow(1024,5),1)) + 'PB'
	elif size < pow(1024,7):
		return str(round(size/pow(1024,6),1)) + 'EB'

if __name__ == '__main__':
	if len(sys.argv) != 2:
		path = input('Please enter a path:').replace('/','//')
	else:
		path = sys.argv[1]
	paths = BFS(Path(path))[0]
	PrintSortedSize(paths)
