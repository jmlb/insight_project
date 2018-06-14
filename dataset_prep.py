#!/usr/bin/env python

"""
	filename: dataset_prep.py
	Description: Clean and validate image, crops and mask of EG dataset
				save a pickle file: a list of dict for each image
				{"img": full_path_to_img, "crops": [x0, d0, y0, h0], "mask": full_path_to_mat_file_mask}
	
	run: `python dataset_prep.py`
"""

import cv2
import numpy
import pickle
from downloader import *


class EGDataset(DownloadEG):
	"""
	Prepare the EG dataset
	Create a list of dict with the following keys : 
		-"img" the path of the image
		-"crop": the vrop specs for the original image
		-"masks": address to the binary mask
	"""

	def __init__(self):
		DownloadEG.__init__(self)
		self.dataset_root = "[[]EG_code_data[]]_release/data"
		self.images_folder = "images" 
		self.crop_txt = "crop.txt"
		self.mask_mats_path = "images_mask"
		self.dataset = [] 

	def read_crop_txt(self):
		"""
		Read crop.txt file and create a dictionary 
		{k: val} with k= image_filename, and value the crop_specs
			output:
				:dict_crop: (dictionary)
		"""
		path_crop_txt = self.dataset_root.replace("[]", "")
		path_crop_txt = "{}/{}".format(path_crop_txt, self.crop_txt)
		dict_crop = dict()
		with open(path_crop_txt, "r") as handler:
			for i, line in enumerate(handler):
				line = line.strip()
				try:
					img_name, x0, d0, y0, h0 = line.split(" ") #last 4 elements are the crop specs
					crop_sz = [int(x0), int(d0), int(y0), int(h0)]
					dict_crop[img_name] =  crop_sz
				except:
					print("Could not process line")   
		return dict_crop
	
	
	def validate_img(self, img):
		"""
		Check validation of an image:  average pixel intensity >1 and < 254 : image is practically all white all back
			arguments
				:img_p: (sring) - path to the image file
			output
				:img_valid: (int) - image valid (1), not valid (0)   
		"""
		thresh_min, thresh_max = 1, 254
		assert isinstance(img, np.ndarray), "img must be an numpy array"
		n_dim = img.ndim
		sum_px = np.sum(img)
		if n_dim == 2:
			w, h = img.shape
			sum_px /= (w * h)    
		elif n_dim == 3:
			w, h, ch =img.shape
			sum_px /= (w * h * ch)
		else:
			sum_px = 0
		
		return ( (sum_px >= thresh_min) or (sum_px) <= thresh_max ) * 1.
		
		
	def read_images_folder(self):
		"""
		List all valid images in images folder
		Create a list of dict 
			output:
				:dict_img: (list) - list of dict where each dict has {k: val} with k=image_filename and 
							val is the status of the image 1=valid, 0=not valid
		"""
		path_imgs = self.dataset_root
		path_imgs = path_imgs +"/"+ self.images_folder +"/*.jpg"
		dict_img = dict()
		for i, img_p in enumerate(glob(path_imgs)):
			img_fname = img_p.split("/")[-1]
			try:
				img = cv2.imread(img_p)
				is_img_valid = self.validate_img(img)
				if is_img_valid:
					dict_img[img_fname] = img_p
			except:
				pass
		return dict_img
		
	
	def read_masks_folder(self):
		"""
		List all valid masks in images folder
			output:
				:dict_masks: (list) - list of dict where each dict has {k: val} with k=img_filename and 
							val: mask_filename is the status of the mask 1=valid, 0=not valid
		"""
		path_mats = self.dataset_root
		path_mats = path_mats +"/"+ self.mask_mats_path +"/*.mat"
		dict_mats = dict()
		for i, mat_p in enumerate(glob(path_mats)):
			try:
				mat = scipy.io.loadmat( mat_p )
				img_fname = mat_p.split("/")[-1]
				img_fname = img_fname.replace("_mask.mat", ".jpg")
				mask_arr = mat["mask"] #uint8 format 0 to 1
				if self.validate_img(mask_arr * 255.):
					dict_mats[img_fname] = mat_p
			except:
				pass
		return dict_mats
		
	
	def build_dataset(self):
		"""
		Compare list of images and masks and keep only images that have corresponding masks
		Create a list of dict with 3 keys: img, mask, crop and save list as pickle file

		"""
		dataset_status = self.check_eg_dataset()
		if dataset_status:
			dict_crops_specs = self.read_crop_txt()
			dict_images = self.read_images_folder()
			dict_masks = self.read_masks_folder()
			for img_fname in dict_images.keys():
				try:
					this_example = dict()
					this_example["img"] = dict_images[img_fname]
					this_example["mask"] = dict_masks[img_fname]
					if img_fname not in dict_crops_specs.keys():
						this_example["crop"] = []
					else:
						this_example["crop"] = dict_crops_specs[img_fname]
					self.dataset.append(this_example)
				except:
					pass
			#save dataset as pickle
			with open("eg_dataset.pickle", "wb") as handle:
				pickle.dump(self.dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)
				print("EG dataset saved in `eg_dataset.pickle`.")


if __name__ == "__main__":

	eg_prep = EGDataset()
	eg_prep.build_dataset()