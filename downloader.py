import urllib.request
import sys
import time
from glob import glob
import zipfile
import os

class Downloader():

	def __init__(self, zip_fname, dataset_url):
		self.zip_fname = zip_fname
		self.dataset_url = dataset_url
		self.data_path = "[[]EG_code_data[]]_release/data"
		self.images_folder = "images"
		self.imgs_urls = "alldata_urls.txt"
		self.dataset_images = [] #keep track of images

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
			print("The dataset already there! {}".format(self.zip_name))
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


	def create_image_folder(self):
		"""
		Create a folder "images" to store all raw images downloaded from flickr.
		List of urls are in `alldata_urls.txt`
		"""
		path2imgs = "{}/{}".format( self.data_path, self.images_folder)
		path2imgs = path2imgs.replace("[]","")
		try:
			os.mkdir( path2imgs )
		except Exception as e:
			print(e)
		return path2imgs



	def get_images(self):
		"""
		Download image dataset (jpeg) from flickr urls
		
		"""
		target_folder = self.create_image_folder()
		ls_urls = "{}/{}".format( self.data_path, self.imgs_urls )
		ls_urls = ls_urls.replace('[]', '').replace('[]', '')
		img_counter = 0
		print("Start downloading Images from Flickr .... ")
		with open(ls_urls, "r") as handler:
			for line in handler:
				line = line.strip()
				content = line.split(" ")
				fname = content[0]
				img_url = content[1]

				if "http://" in img_url:
					img_p = "{}/{}".format(target_folder, fname)
					self.dataset_images.append(img_p)
					urllib.request.urlretrieve(img_url, img_p)
					img_counter += 1
				
				if img_counter%50 == 0:
					print("Number of Images downloaded: {}".format(img_counter) )

		print("Total Number of images downloaded: {}".format(img_counter))

