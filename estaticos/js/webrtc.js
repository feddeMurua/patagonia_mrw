/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

'use strict';

// Put variables in global scope to make them available to the browser console.
var video = document.querySelector('video');
var canvas = window.canvas = document.querySelector('canvas');
var old_img = document.querySelector('#old-img');
var img = document.querySelector('#foto-img');
var img64 = document.querySelector('#img-base64');
var n_foto = document.querySelector('#nueva-foto');
var e_foto = document.querySelector('#eliminar-foto');
var t_foto = document.querySelector('#tomar-foto');
var c_foto = document.querySelector('#cancelar-foto');
var no_foto = ["", "borrar"]

canvas.width = 320;
canvas.height = 240;

n_foto.onclick = function() {
    $(old_img).attr('hidden',true);
    $(img).attr('hidden',true);
    $(video).attr('hidden',false);
    $(n_foto).addClass('hidden');
    $(e_foto).addClass('hidden');
    $(t_foto).removeClass('hidden');
    $(c_foto).removeClass('hidden');
};

t_foto.onclick = function() {
    canvas.getContext('2d').
        drawImage(video, 0, 0, canvas.width, canvas.height);
    $(video).attr('hidden',true);
    $(n_foto).removeClass('hidden');
    $(e_foto).removeClass('hidden');
    $(t_foto).addClass('hidden');
    $(c_foto).addClass('hidden');
    $(img).attr('hidden',false);
    img.src = canvas.toDataURL('image/png');
    img64.value = img.src;
};

c_foto.onclick = function() {
    $(video).attr('hidden',true);
    $(n_foto).removeClass('hidden');
    if (img64.value && img64.value != "borrar") {
        $(e_foto).removeClass('hidden');
    }
    $(t_foto).addClass('hidden');
    $(c_foto).addClass('hidden');
    if (img64.value != "borrar") {
        $(img).attr('hidden',false);
    }
    if (!(img64.value)) {
        $(old_img).attr('hidden',false);
    }
};

e_foto.onclick = function() {
    $(old_img).attr('hidden',true);
    $(img).attr('hidden',true);
    img64.value = "borrar";
    $(e_foto).addClass('hidden');
}

var constraints = {
  audio: false,
  video: true
};

function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
}

function handleError(error) {
  console.log('navigator.getUserMedia error: ', error);
}

navigator.mediaDevices.getUserMedia(constraints).
then(handleSuccess).catch(handleError);