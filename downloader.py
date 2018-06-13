#!/usr/bin/env python

"""
	filename: downloader.py
	Description: Download the dataset as a zip file
				Unzip the file
				Download all the required online images and saves them in a created images/ folder

				If the images/ folder exists and is not empty - pass
"""

__author__      = "Jean-Marc Beaujour"


import urllib.request
import sys
import time
from glob import glob
import zipfile
import os



class DownloadEG():

	def __init__(self):
		"""
			:dataset_url: url where to download the dataset
			:zip_fname: save dataset as a zip file
			:data_path: directory where the data is saved
			:images: 
		"""
		self.dataset_url = "https://www.dropbox.com/s/7vl1sprdln8dg9k/EG_code_data_release.zip?dl=1"
		self.zip_fname = "dataset_EG.zip"
		self.data_path = "[[]EG_code_data[]]_release/data"
		self.imgs_urls = "alldata_urls.txt"
		self.masks_folder = "images_mask"


	def reporthook(self, count, block_size, total_size):
		"""
			Show progress bar during file download
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


	def file_exists(self, this_file, this_folder):
		"""
			check that a file exists in this folder
		""" 
		if this_file in glob(this_folder):
			return True
		else:
			return False


	def folder_exists(self, this_subfolder, this_root):
		"""
			check that the dataset folder exits
		""" 

		if len(this_root) == 0:
			this_root = "*"
			this_subfolder = this_subfolder.replace("[]", "")
		else:
			this_subfolder = this_root +"/"+ this_subfolder
			this_subfolder = this_subfolder.replace("[]", "")
			this_root = this_root +"/*"

		if this_subfolder in glob("{}".format(this_root)):
			return True
		else:
			return False


	def download_dataset(self):
		"""
			Download dataset from 
			url: https://www.dropbox.com/s/7vl1sprdln8dg9k/EG_code_data_release.zip?dl=1
		"""
		flag_zip_exists = self.file_exists(self.zip_fname, "*")
		if flag_zip_exists:
			print("The zip file exists! {}".format(self.zip_fname))
		else:
			urllib.request.urlretrieve(self.dataset_url, self.zip_fname, self.reporthook)


	def unzip_file(self, zipfname):
		"""
			uncompress the downloaded zip file
		"""
		flag_zip_exists = self.file_exists(zipfname, "*")
		data_path_root = self.data_path.split("/")[0]
		flag_EG_folder_exists = self.folder_exists(data_path_root, "")
		
		if flag_zip_exists and not flag_EG_folder_exists:
			with zipfile.ZipFile(zipfname, "r") as zip_ref:
				zip_ref.extractall()
			os.remove(zipfname) #free storage
		else:
			print("No file was unzipped")


	def create_folder(self, new_folder, this_path):
		"""
		Create a folder "images" to store all raw images downloaded from flickr.
		List of urls are in `alldata_urls.txt`
		"""
		new_folder_exists = self.folder_exists(new_folder, this_path)

		if not new_folder_exists:
			path_new_folder = "{}/{}".format( this_path, new_folder)
			path_new_folder = path_new_folder.replace("[]","")
		
			try:
				os.mkdir( path_new_folder )
			except Exception as e:
				print(e)


	def download_jpg(self, save_here):
		"""
		Download image dataset (jpeg) from flickr urls
		"""
		txt_urls = "{}/{}".format( self.data_path, self.imgs_urls )
		txt_urls = txt_urls.replace('[]', '').replace('[]', '')
		img_counter = 0
		
		print("Start downloading Images from Flickr .... ")
		
		with open(txt_urls, "r") as handler:
			for line in handler:
				line = line.strip()
				line = line.split(" ")
				fname, img_url = line[0], line[1]

				if "http://" in img_url:
					img_path = "{}/{}".format(save_here, fname)
					urllib.request.urlretrieve(img_url, img_path)
					img_counter += 1
				
				if img_counter%50 == 0:
					print("Number of Images downloaded: {}".format(img_counter) )

		print()
		print("Total Number of images downloaded: {}".format(img_counter))



	def run(self):

		"""
		Download dataset and inputs
		"""
		flder_images = "images"
		# download zip file
		self.download_dataset()
		
		# Unzip dataset EG file
		self.unzip_file(self.zip_fname)

		#create a folder image in the EG/data folder
		self.create_folder(flder_images, self.data_path)

		#Check if folder images contains jpg images
		img_folder = self.data_path +"/"+ flder_images +"/*.jpg"

		if len(glob(img_folder)) == 0:
			#Download image files in images
			target_flder_dwnld = self.data_path +"/"+ flder_images
			target_flder_dwnld = target_flder_dwnld.replace("[]", "")
			self.download_jpg(target_flder_dwnld)

		print("EG Data acquisition completed!")


	def check_eg_dataset(self):
		"""
			Confirm:
				+ [[]EG_code_data[]]_release/data/images/ exists and is not empty
				+ [[]EG_code_data[]]_release/data/crop.txt exists
				+ [[]EG_code_data[]]_release/data/images_mask exists and not empty
		"""
		print("Check saved Dataset: .... ")
		
		flag_img = self.folder_exists("images", self.data_path)
		if flag_img:
			ls_jpgs = glob(self.data_path +"/images/*.jpg")
			if len(ls_jpgs) == 0:
				print("Image folder empty!")
				return 0
		else:
			print("Image Folder cannot be found!")
			return 0

		crop_file_path = self.data_path.replace("[]", "") +"/crop.txt"
		flag_crop_txt = self.file_exists(crop_file_path, self.data_path +"/*")
		if not flag_crop_txt:
			print("File with image crop specs not found!")
			return 0
		
		flag_masks = self.folder_exists("images_masks", self.data_path)
		if flag_masks:
			ls_mats = glob(self.data_path +"/images_masks/*.mat")
			if len(ls_mats) == 0:
				print("Mask folder empty!")
				return 0

		print("No error found!")


			flder_images = "images"
			# download zip file
			self.download_dataset()
			
			# Unzip dataset EG file
			self.unzip_file(self.zip_fname)

			#create a folder image in the EG/data folder
			self.create_folder(flder_images, self.data_path)

			#Check if folder images contains jpg images
			img_folder = self.data_path +"/"+ flder_images +"/*.jpg"

			if len(glob(img_folder)) == 0:
				#Download image files in images
				target_flder_dwnld = self.data_path +"/"+ flder_images
				target_flder_dwnld = target_flder_dwnld.replace("[]", "")
				self.download_jpg(target_flder_dwnld)

			print("Image acquisition completed!")



if __name__ == "__main__":

	dwnld = DownloadEG()
	dwnld.run()
	dwnld.check_eg_dataset()

