import glob
import argparse
from re import search
from os import path, walk, mkdir
from itertools import chain
from html.parser import HTMLParser

def glob_or_com(s):
	retval = glob.glob(s)

	if not retval:
		print("File not found:"+s)

	return retval

class MyHTMLParser(HTMLParser):
	con_data = ""
	data = ""
	title = ""
	def handle_starttag(self, tag, attrs):
		if len(attrs) == 3 and "title" in attrs[-1]:
			self.title = attrs[-1][-1]
		if len(attrs) == 3 and "title" not in attrs[-1]:
			raise AttributeError("title not found")

	def handle_endtag(self, tag):
		pass

	def handle_data(self, data):
		self.data = data

		if "MediaWiki:" not in self.title and "Dosya:" not in self.title and "Yardım:" not in self.title and "File:" not in self.title and "Help:" not in self.title:
			self.con_data += data

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="WikiPedia DataSets HTML Tags Cleaner")

	parser.add_argument('file',type=str,nargs="+",help="File(s) to be clean")

	args = parser.parse_args()

	f_d = map(glob_or_com, args.file)

	f_d = list(chain(*f_d))

	files = []

	for i in f_d:
		if path.isdir(i):
			for dirpath, dirnames, filenames in walk(i):
				files.extend(path.join(dirpath,j) for j in filenames if len(j) >= 5 and j.startswith(("wiki")))
		else:
			files.append(i)

	if len(files) > 0:
		for fileName in files:

			file = open(fileName,"r",encoding="utf-8")

			file_read = file.read()

			file.close()

			parser = MyHTMLParser()
			parser.feed(file_read)

			if path.exists("./cleaned_data_sets/"):
				pass
			else:
				mkdir("./cleaned_data_sets/")

			file = open("cleaned_data_sets/"+fileName,"w",encoding="utf-8")
			file.write(parser.con_data)
			file.close()