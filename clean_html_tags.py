import glob
import argparse
from os import path, walk, sep, makedirs
from html.parser import HTMLParser
from tqdm import tqdm

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
		if tag == "doc":
			if len(attrs) == 3 and "title" in attrs[-1]:
				self.title = attrs[-1][-1]
			if len(attrs) == 3 and "title" not in attrs[-1]:
				raise AttributeError("title not found")

	def handle_endtag(self, tag):
		pass

	def handle_data(self, data):
		self.data = data

		if "MediaWiki:" not in self.title and "Dosya:" not in self.title and "Yardım:" not in self.title and "File:" not in self.title and "Help:" not in self.title and "Vikipedi:" not in self.title:
			self.con_data += data

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="WikiPedia DataSets HTML Tags Cleaner")

	parser.add_argument('file',type=str,nargs="+",help="File(s) to be clean")

	args = parser.parse_args()

	f_d = map(glob_or_com, args.file)

	f_d = list(chain(*f_d))

	files = []

	files_count = 0

	for i in f_d:
		if path.isdir(i):
			for dirpath, dirnames, filenames in walk(i):
				files.extend(path.join(dirpath,j) for j in filenames if len(j) >= 5 and j.startswith(("wiki")))
		else:
			files.append(i)

	if len(files) > 0:

		filesCount = len(files)

		for fileN in tqdm(files,desc="Cleaned and Saved Files",bar_format="{desc}: {n_fmt}/{total_fmt} | [time left: {remaining}]"):

			fileName = fileN.replace(sep, "/")
			fileDirName = path.dirname(fileName)

			file = open(fileName,"r",encoding="utf-8")

			file_read = file.read()

			file.close()

			parser = MyHTMLParser()
			parser.feed(file_read)

			if path.exists("cleaned_data_sets/"):
				if fileDirName != "":
					if path.exists("cleaned_data_sets/"+fileDirName):
						pass
					else:
						makedirs("cleaned_data_sets/"+fileDirName)
			else:
				makedirs("cleaned_data_sets/")
				if fileDirName != "":
					makedirs("cleaned_data_sets/"+fileDirName)

			file = open("cleaned_data_sets/"+fileName,"w",encoding="utf-8")
			file.write(parser.con_data)
			file.close()