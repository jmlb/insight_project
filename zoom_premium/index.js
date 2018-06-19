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

import {ControllerDataset} from './controller_dataset';
import * as ui from './ui';
import {Webcam} from './webcam';

// A webcam class that generates Tensors from the images from the webcam.
const webcam = new Webcam(document.getElementById('webcam'));

let model;
const LOCAL_MODEL_JSON_URL = 'http://storage.googleapis.com/modelinsight/tfjs/model.json'; 
// Loads mobilenet and returns a model
async function loadModel() {
  const model = await tf.loadModel(LOCAL_MODEL_JSON_URL);
  return model
}

/**
 * Sets up and trains the classifier.
 */

let isPredicting = false;

async function predict() {
  ui.isPredicting();
  while (isPredicting) {
    const mask = tf.tidy(() => {
      // Capture the frame from the webcam.
      const img = webcam.capture();
      const img_norm = tf.div(img, tf.scalar(255))
      // Make a prediction through mobilenet, getting the internal activation of
      // the mobilenet model.
      const predictions = model.predict(img);

      // Make a prediction through our newly-trained model using the activation
      // from mobilenet as input.
      //const predictions = model.predict(activation);
      //const binary = predictions.round()
      //const combo = tf.mul(img_norm, binary)
      //const pixel_intensity = tf.scalar(255.);
      //const pred = tf.mul( predictions, pixel_intensity );
      const pred = tf.reshape(predictions, [224, 224, 1]);
      //const pred_ = tf.cast(pred, tf.uint8);
      //const png = tf.image.encode_jpeg( pred );
      //const png = pred
      //png.print();

      // Returns the index with the maximum probability. This number corresponds
      // to the class the model thinks is the most probable given the input.
      //const png = png = tf.image.encode_png(tf.cast((tf.reshape(bgr, [256, 256, 3]) + 1.) * 127.5, tf.uint8))
      //const png = pred_.dataSync();
      //png.print()

      //const png = tf.image.encode_png( tf.cast(tf.reshape(tf.tensor(predictions), [224, 224]), tf.uint8) );
      //const base_image = new Image();
      //base_image.src = png;
      //pred.print()
      
      return pred
    });

    
    ui.setPredictedMaskClass(mask);
    await tf.nextFrame();
  }
  ui.donePredicting();
}


  document.getElementById('predict').addEventListener('click', () => {
  isPredicting = true;
  predict();
});

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
