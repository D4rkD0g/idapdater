from bs4 import BeautifulSoup
import requests
import os
import sys


class GetTab(object):
	"""docstring for GetTab"""
	def __init__(self, targetdir, keysfile="idckeys.txt",):
		super(GetTab, self).__init__()
		self.url = "https://www.hex-rays.com/products/ida/support/ida74_idapython_no_bc695_porting_guide.shtml"
		self.keysfile = keysfile
		self.targetdir = targetdir
		self.keys_table = {}

	def down_table(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text,"lxml")

		tables = soup.find_all("table")
		f = open(self.keysfile, "w+")

		print("{} tables".format(len(tables)))
		for table in tables:
			items = table.tbody.find_all("tr")
			print("One has {} items".format(len(items)))
			for item in items:
				idc_keys = item.find_all("td")
				idc_old = idc_keys[0].code
				idc_new = idc_keys[1].code
				if idc_old and idc_new:
					key_old = idc_old.string
					key_new = idc_new.string
					f.write("{}~{}\r\n".format(key_old, key_new))
				else:
					print("Dont include: ", idc_keys)
		f.close()

	def get_table(self):
		if not os.path.exists(self.keysfile):
			self.down_table()

		with open(self.keysfile, "r") as f:
			lines = f.readlines()
		for line in lines:
			keys = line.strip().split("~")
			key_old = keys[0].strip()
			key_new = keys[1].strip()
			self.keys_table[key_old] = key_new
	def trans(self):
		if self.keys_table == {}:
			print("Key Dic is Empty")
			exit(-1)

		td = os.walk(self.targetdir)  

		for path, dir_list, file_list in td:  
			for file_name in file_list:  
				if not file_name.endswith(".py"):
					continue
				filename = os.path.join(path, file_name)
				print(filename)
				for item, value in self.keys_table.items():
					cmd = "sed -i 's/\\<{}\\>/{}/g' {}".format(item, value, filename)
					os.system(cmd)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("./xxx.py targetdir [keyfile]")
		exit(0)
	if len(sys.argv) == 3:
		keysfile = sys.argv[2]
		table = GetTab(targetdir = sys.argv[1], keysfile = keysfile)
	else:
		table = GetTab(targetdir = sys.argv[1])
	table.get_table()
	table.trans()
	print("Done")