# TensorFlow.js example to classify binary classes 

We use tensorflowjs to to train directly from the browser of the client. The images are collected from the webcam of the client. 
This code is an editted version of https://github.com/tensorflow/tfjs-examples/tree/master/webcam-transfer-learning

## Getting Started 

### Installing nodejs
* First we need to install nodejs version 8. Check your version of nodejs by typing  `nodejs -v`
* If you you have version 8 or greater then you are done. 
* If you have a lower version then first purge the previous version 
`sudo apt-get purge nodejs npm`
* After that we install nodejs using 

`curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -`

`sudo apt-get install -y nodejs`

### Compiling the code 
* Clone the directory using 

`git clone https://github.com/zaidalyafeai/tensorflowjs-binary`
* cd inside the directory 

`cd tensorflowjs-binary`
* Start the browser using 

`yarn`
 
`yarn watch`

## Interface 

![Alt text](img.png?raw=true "Title")


## Case study 

Here we train on recognizing my face when wearing glasses and without them. I captured around 250 images for the positive class(with glasses on) and around 220 images for the engative class (with glasses off). We train for 20 epochs using the initial hyper-parameters. we get a loss of `0.00217`.

### positive class 
![Alt text](screen-pos.png?raw=true "Title")
### negative class 
![Alt text](screen-neg.png?raw=true "Title")
