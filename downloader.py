import urllib.request
import sys
import time
from glob import glob
import zipfile

class Downloader():

	def __init__(self, zip_fname, url):
		self.zip_fname = zip_fname
		self.url = url


	def reporthook(self, count, block_size, total_size):
		"""
			Download progress bar
		"""
		global start_time
		if count == 0:
			start_time = time.time()
			return
		duration = time.time() - start_time
		progress_size = int(count * block_size)
		speed = int(progress_size / (1024 * duration))
		percent = int(count * block_size * 100 / total_size)
		sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
						(percent, progress_size / (1024 * 1024), speed, duration))
		sys.stdout.flush()

	def dwnloaded_file_exists(self):
		if self.zip_fname in glob(self.zip_fname):
			return True
		else:
			return False


	def dataset_downloader(self):
		"""
			Download dataset from url: https://www.dropbox.com/s/7vl1sprdln8dg9k/EG_code_data_release.zip?dl=1
		"""
		if dwnloaded_file_exists:
			pass
		else:
			urllib.request.urlretrieve(self.url, self.zip_fname, reporthook)
			return zip_fname


	def unzip_file(self):
		if self.dwnloaded_file_exists():
			with zipfile.ZipFile(self.zip_fname,"r") as zip_ref:
				zip_ref.extractall()
		else:
			print("Could not find file: {}".format(self.zip_fname))


	def get_dataset(self):
		dataset_url =  "https://www.dropbox.com/s/7vl1sprdln8dg9k/EG_code_data_release.zip?dl=1"
		dataset_save_fname = "dataset_EG.zip"

		#try:
		#	self.dataset_downloader()
		self.unzip_file()

		#except:
		#	print("Could not get data!")