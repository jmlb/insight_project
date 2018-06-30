/**
 * @license
 * Copyright 2018 Google LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */

import * as tf from '@tensorflow/tfjs';
import * as ui from './ui';
import {Webcam} from './webcam';
const LOCAL_MODEL_JSON_URL = 'http://storage.googleapis.com/modelinsight/tfjs/model.json'; 


/**
*  Keep track of the frame rate in a queue
**/
var queue_sz = 20;
var queue_fps = []; //record process time of each frame up to queue_sz # of frames

function show_fps(arr) {
    const reducer = (accumulator, currentValue) => accumulator + currentValue;
    const this_sum = arr.reduce(reducer); //total time for n frames in sec
    const fps = arr.length / ( this_sum )
    document.getElementById("fps").innerHTML = fps.toFixed(2) +"fps";
}


// A webcam class that generates Tensors from the images from the webcam.
const webcam = new Webcam(document.getElementById('webcam'));
const customBKGSelect = document.getElementById("custom_bkg");
const img_sz = 224;
var bkg_data = [];
var predictions = 0

/**
* Load the model locally
**/
let model;
async function loadModel() {
  const model = await tf.loadModel(LOCAL_MODEL_JSON_URL);
  return model
}

function get_background(){
  ui.load_bgd_image();
}


/**
 * Prediction
 */

let isPredicting = false;
let isCustomBackground = false;
var init_time = performance.now();

async function predict() {
    ui.isPredicting();
    while (isPredicting) {
      init_time = performance.now();
      const output = tf.tidy(() => {
        // Capture the frame from the webcam.
        const img = webcam.capture();
        // Inference
        predictions = model.predict(img);
        const img_clone = tf.reshape( img, [img_sz, img_sz, 3]);
        const pred_mask = tf.reshape(predictions, [img_sz, img_sz, 1]);

        //const p_tiled = tf.tile( img, [224, 224, 3] )
        if (isCustomBackground && ( bkg_data.length > 0 )) {
          const this_bkg = new ImageData(bkg_data, img_sz, img_sz)
          const mixed = tf.mul(img_clone, pred_mask);
          const bkg_tf = tf.fromPixels( this_bkg );
          const bkg_norm = tf.div( tf.cast(bkg_tf, "float32"), tf.scalar(255.));
          //Reverse mask: abs(pred_mask - 1)
          const rev_pred_mask = tf.abs( tf.sub(pred_mask, tf.scalar(1.)) );
          const bkg_matted = tf.mul( bkg_norm, rev_pred_mask );
          const combo = tf.div(tf.add(mixed, bkg_matted), tf.scalar(2.0) );
          const predict_t = performance.now();
          return [pred_mask, combo]
        }
        else {
          const combo = tf.mul(img_clone, pred_mask);
          return [pred_mask, combo]
        }
      });

      ui.setPredictedMaskClass(output[0]); //340sec
      ui.setPredictedComboClass(output[1]);

      await tf.nextFrame();
      
      /**
      * Update table of frame rate
      **/
      var elapsed_time = (performance.now() - init_time) * 0.001; //elapsed time in sec
      if (queue_fps.length == queue_sz){
        queue_fps.push(elapsed_time);
        queue_fps.shift();
        show_fps(queue_fps);
      }
      else {
        queue_fps.push(elapsed_time);
      }

    }
  ui.donePredicting();
}


document.getElementById("predict").addEventListener("click", () => {
  isPredicting = true;
  predict();
});

document.getElementById('show_original').addEventListener("click", () => {
  isPredicting = false;
  ui.clearPredictedMaskClass();
});

/**
* Apply custom background
**/
customBKGSelect.addEventListener("change", () => {
    const img_url = customBKGSelect.value;
    isPredicting = false;
    //disable/enable custom background 
    if (img_url == "black")
    { 
      isCustomBackground = false;
      isPredicting = true;
    }
    else
    { 
      //create canvas
      const canvas_bkg = document.createElement("canvas");
      canvas_bkg.id = "canvas_bkg";
      canvas_bkg.width = img_sz;
      canvas_bkg.height = img_sz;
      //const canvas_bkg = document.getElementById('canvas_bkg')
      const context = canvas_bkg.getContext("2d");
      //create new image
      const img_bkg = new Image();
      img_bkg.src = img_url;
      img_bkg.onload = function(){
        context.drawImage(img_bkg, 0, 0, img_sz, img_sz);
        const bkg_ImgData = context.getImageData(0, 0, img_sz, img_sz);
        bkg_data = bkg_ImgData.data
        isPredicting = true;
      }
      isCustomBackground = true;

    }
  }
  , false );


async function init() {
  await webcam.setup();
  model = await loadModel();
  // Warm up the model. This uploads weights to the GPU and compiles the WebGL
  // programs so the first time we collect data from the webcam it will be
  // quick.
  tf.tidy(() => model.predict(webcam.capture()));

  ui.init();
}

// Initialize the application.
init();
