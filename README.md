# Zoom Premium
(Insight Project)

![result](https://github.com/jmlb/insight_project/blob/master/results.png)

Zoom premium is a semantic segmentation app that is tasked to remove or replace the background in webcam live video stream. The Deep Learning model is based on MobileNet and UNet, and as a result it has a small footprint: about 6 million parameters. This demo shows how inference conducted exclusively on the client browser can be performed even for ressource heavy tasks such as semantic segmentation. 

 
For more info about how I build the app check out the post.

https://medium.com/@jmlbeaujour/real-time-matting-of-webcam-video-on-the-browser-part-1-2c71a330ed08


## Model

Main File: `Segmentation_Model.ipynb`

Dependencies: `utils/rawdata_prep.py` and `utils/downloader.py`

The jupyter notebook performs the following job:

	1. Download of the Flickr Portrait Dataset from Dropbox (zip file): includes masks (mat files) and image crop info (in text file)

	2. Unzip file

	3. Download the online images

	4. Build the Segmentation model

	5. Train model

	6. Save Keras model

	7. Convert model to TFJS format

	8. Upload converted model to Google Cloud Storage bucket


## The app (in browser)

Files:

	+ `zoom_premium/index.html` : it is the main html page. 
		It displays the 3 items: the original frame from the webcam, the combo frame (the matted portrait + synthetic background) and the predicted mask

	+ `zoom_premium/index.js` : includes the code for prediction and the tensor manipulation to generate the combo frame


	+ `zoom_premium/ui.js` : js methods for user interface

To run the app locally:

	1. Install `yarn`: follow the instructions [here](https://yarnpkg.com/lang/en/docs/install/#debian-stable))

	2. In the Terminal, go to the folder `zoom_premium`

	3. run:  `yarn`

	4. start the app with: `yarn watch`

A window of the browser opens with the address: `http://localhost:1234`. Wait a few seconds for the model to be downloaded locally.

Have a fun!
