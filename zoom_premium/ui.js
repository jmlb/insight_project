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


export function init() {
  document.getElementById('controller').style.display = '';
  statusElement.style.display = 'none';
}

const statusElement = document.getElementById('status');

const predictedMaskElement = document.getElementById('mask_class');
const predictedComboElement = document.getElementById('combo_class');


export function setPredictedMaskClass(mask) {
  //add a Alpha channel
  tf.toPixels( mask, predictedMaskElement );
}

export function setPredictedComboClass(combo) {
  const alpha_ch = tf.ones([224, 224, 1]);
  tf.toPixels( combo.concat(alpha_ch, 2), predictedComboElement );
}         

export function clearPredictedMaskClass() {
  const context = predictedMaskElement.getContext('2d');
  context.clearRect(0, 0, 224, 224);
}

export function clearPredictedComboClass() {
  const context = predictedComboElement.getContext('2d');
  context.clearRect(0, 0, 224, 224);
}

export function isPredicting() {
  statusElement.style.visibility = 'visible';
}

export function donePredicting() {
  statusElement.style.visibility = 'hidden';
}
