from utils.downloader import *
from glob import glob
from downloader import *

if __name__ == "__main__":


	dataset_url =  "https://www.dropbox.com/s/7vl1sprdln8dg9k/EG_code_data_release.zip?dl=1"
	zip_fname = "dataset_EG.zip"

	dwnld = Downloader(zip_fname, dataset_url)
	dwnld.get_dataset()
