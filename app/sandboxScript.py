import math
import hashlib
import os

if __name__ == "__main__":
	path = "hashme/"
	dir_list = os.listdir(path)
	f = open(path + dir_list[0], "rb")
	data = f.read()
	sha256 = hashlib.sha256()
	sha256.update(data)
	f.close()
	print(sha256.hexdigest())
	os.remove(path + dir_list[0])
