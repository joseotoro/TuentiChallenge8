/* 
 * Image unshredder demo (JavaScript)
 * 
 * Copyright (c) 2016 Project Nayuki
 * All rights reserved. Contact Nayuki for licensing.
 * https://www.nayuki.io/page/image-unshredder-by-annealing
 */

"use strict";


/*---- Global variables and initialization ----*/

// HTML elements
var canvasElem = element("canvas");
var graphics = canvasElem.getContext("2d");
var imageSelectElem = element("image-select"     );
var shuffleButton   = element("shuffle-button"   );
var annealButton    = element("anneal-button"    );
var stopButton      = element("stop-button"      );
var imageAttribElem = element("image-attribution");
var imageAttribText    = makeTextNodeChild("image-attribution"  , ""      );
var curIterationsText  = makeTextNodeChild("current-iterations" , "\u2012");

// List of images to play with
var IMAGE_LIST = [
  ["Tuenti"   , "scrambled2.png"   , "IQRemix"                 , "https://contest.tuenti.net"       ],
];

// Base image properties
var baseImage = new Image();
var width = -1;
var height = -1;

// Variables for shuffling
var shuffleStartColumn = -1;
var shuffledImage = null;

// Variables for annealing
var numIterations    = -1;
var startTemperature = -1;
var curIteration     = -1;
var curEnergy        = -1;
var columnDiffs    = null;  // columnDiffs[x0][x1] is the amount of difference between column x0 and column x1 in shuffledImage
var colPermutation = null;
var annealingLastDrawTime = -1;

// Performance tuning
var YIELD_AFTER_TIME = 20;  // In milliseconds; a long computation relinquishes/yields after this amount of time; short will mean high execution overhead; long will mean the GUI hangs
var ANNEAL_REDRAW_TIME = 300;  // In milliseconds; the minimum amount of time between image and text updates when performing annealing


function init() {
  baseImage.onload = function() {
    canvasElem.width = width = baseImage.width;
    canvasElem.height = height = baseImage.height;
    graphics.drawImage(baseImage, 0, 0, width, height);
    setButtonState(1);
    shuffledImage = null;
    columnDiffs = null;
  };
  
  shuffleButton.onclick = startShuffle;
  annealButton .onclick = startAnneal;
  stopButton   .onclick = doStop;
  
  while (imageSelectElem.firstChild != null)
    imageSelectElem.removeChild(imageSelectElem.firstChild);
  IMAGE_LIST.forEach(function(entry) {
    var option = document.createElement("option");
    option.appendChild(document.createTextNode(entry[0]));
    imageSelectElem.appendChild(option);
  });
  
  imageSelectElem.selectedIndex = Math.floor(Math.random() * IMAGE_LIST.length);
  imageSelectElem.onchange = function() {
    width = -1;
    height = -1;
    setButtonState(0);
    var entry = IMAGE_LIST[imageSelectElem.selectedIndex];
    baseImage.src = "" + entry[1];
    imageAttribText.data = " " + entry[2];
    imageAttribElem.href = entry[3];
  };
  imageSelectElem.onchange();
}


/*---- Main functions ----*/

function doStop() {
  shuffleStartColumn = width;
  curIteration = -1;
}


function startShuffle() {
  setButtonState(2);
  curIterationsText.data  = "\u2012";
  graphics.drawImage(baseImage, 0, 0, width, height);
  shuffledImage = graphics.getImageData(0, 0, width, height);
  shuffleStartColumn = 0;
  doShuffle();
}


function doShuffle() {
  var startTime = Date.now();
  var pixels = shuffledImage.data;
  while (shuffleStartColumn < width) {
    // Pick a random column j in the range [i, width) and move it to position i.
    // This Fisher-Yates shuffle is the less efficient than the Durstenfeld shuffle but more animatedly appealing.
    var i = shuffleStartColumn;
    var j = i + Math.floor(Math.random() * (width - i));
    for (var y = 0; y < height; y++) {
      for (var x = j - 1; x >= i; x--) {
        var off = (y * width + x) * 4;
        for (var k = 0; k < 4; k++) {
          var temp = pixels[off + k];
          pixels[off + k] = pixels[off + 4 + k];
          pixels[off + 4 + k] = temp;
        }
      }
    }
    shuffleStartColumn++;
    if (Date.now() - startTime > YIELD_AFTER_TIME)
      break;
  }
  graphics.putImageData(shuffledImage, 0, 0);
  
  // Continue shuffling or finish
  if (shuffleStartColumn < width)
    setTimeout(doShuffle, 0);
  else {
    setButtonState(3);
    curIteration = 0;
    curEnergy = -1;
    columnDiffs = null;
  }
}


function startAnneal() {
  setButtonState(2);
  curIterationsText.data = "Precomputing...";
  setTimeout(doBetterApproach, 0);
}


function computeDiffTable(pixels) {
  var columns = [];
  for (var i = 0; i < width; i++) {
    var row = [];
    for (var j = 0; j < width; j++) {
      if(i === j) row.push(0);
      else if(i < j) row.push(lineDiff(pixels, width, height, i, j));
      else row.push(columns[j][i]);
    }
    columns.push(row);
  }
  return columns;
}

function doBetterApproach() {
  var pixels = shuffledImage.data;
  var diffTable = computeDiffTable(pixels);

  // find the best pair
  var starter = 0, lowestValue = diffTable[0][1];
  for(var i = 0; i < width; i++) {
    for(var j = 0; j < i; j++) {
      if(diffTable[i][j] < lowestValue) {
        starter = i;
        lowestValue = diffTable[i][j];
      }
    }
  }
  //  starter = 0;

  // initialize the same as the shuffled image rotated so that we'll start with a best pair
  var columnOrder = [];
  for(var i = 0; i < width; i++) {
    columnOrder.push( (i + starter) % width );
  }

  var i = 1;
  function processIteration() {
    // find the best column to add on one side of the completed chunk
    var bestColumn = i, newIndex = i, bestValue = diffTable[columnOrder[i - 1]][columnOrder[i]];
    var count = 0, s = 0;
    for(var j = i; j < width; j++) {
      if(diffTable[columnOrder[j]][columnOrder[i - 1]] < bestValue) {
        bestColumn = j;
        newIndex = i;
        bestValue = diffTable[columnOrder[j]][columnOrder[i - 1]];
      }
      else if (diffTable[columnOrder[j]][columnOrder[0]] < bestValue) {
        bestColumn = j;
        newIndex = 0;
        bestValue = diffTable[columnOrder[j]][columnOrder[0]];
      }
      s += diffTable[j][0];
      count++;
    }

    // now move column 'bestColumn' to 'newIndex'
    columnOrder.splice(newIndex, 0, columnOrder.splice(bestColumn, 1)[0]);
    setTimeout(function() { curIterationsText.data = i; }, 0);
    curIterationsText.data = formatWithThousandsSeparators(i+1) + " (" + (((i+1)/width) * 100).toFixed(2) + "%)";

    i++;
    if(i < width) {
      setTimeout(processIteration, 0);
    }
    else {
      updateAnnealedImage(columnOrder);
      curIteration = 0;
      colPermutation = null;
      setButtonState(3);
    }
  }
  processIteration();
}

function updateAnnealedImage(columnOrder) {
    var annealedImage = graphics.createImageData(width, height);
    var shuffledPixels = shuffledImage.data;
    var annealedPixels = annealedImage.data;
    for (var y = 0; y < height; y++) {
      for (var x = 0; x < width; x++) {
        var off0 = (y * width + columnOrder[x]) * 4;
        var off1 = (y * width + x) * 4;
        for (var i = 0; i < 4; i++)
          annealedPixels[off1 + i] = shuffledPixels[off0 + i];
      }
    }
    graphics.putImageData(annealedImage, 0, 0);
}

/*---- Helper functions ----*/

function lineDiff(pixels, width, height, x0, x1) {
  var sum = 0;
  for (var y = 0; y < height; y++) {
    var off0 = (y * width + x0) * 4;
    var off1 = (y * width + x1) * 4;
    for (var i = 0; i < 3; i++) {
      var v = pixels[off0 + i] - pixels[off1 + i];
      sum += Math.abs(v);
    }
  }
  return Math.sqrt(sum);
}


function formatWithThousandsSeparators(n) {
  var s = n.toString();
  for (var i = s.length - 3; i > 0; i -= 3)
    s = s.substr(0, i) + " " + s.substring(i);
  return s;
}


// 0: Loading image, 1: Image loaded, 2: Currently shuffling or annealing, 3: Image shuffled
function setButtonState(state) {
  imageSelectElem.disabled = state == 2;
  shuffleButton.disabled = state == 0 || state == 2;
  annealButton.disabled = state != 3;
  stopButton.disabled = state != 2;
}


function makeTextNodeChild(elemId, initText) {
  var result = document.createTextNode(initText);
  element(elemId).appendChild(result);
  return result;
}


function element(elemId) {
  return document.getElementById(elemId);
}


// We put this call after all global variables are declared
init();
