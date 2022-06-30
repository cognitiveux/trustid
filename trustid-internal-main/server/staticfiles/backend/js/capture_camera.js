
$(document).ready(function (){

  let camera_button = document.querySelector("#start-camera");
  let video = document.querySelector("#video");
  let click_button = document.querySelector("#click-photo");
  let stop_button = document.querySelector("#stop-photo");
  let canvas = document.querySelector("#canvas");

  camera_button.addEventListener('click', async function() {
      let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      video.srcObject = stream;
  });

  click_button.addEventListener('click', function() {
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
      let image_data_url = canvas.toDataURL();
      const base64Canvas = image_data_url.split(';base64,')[1];
      console.log(base64Canvas);
  });

  stop_button.addEventListener('click', function() {
      const stream = video.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach(function(track) {
        track.stop();
      });

      video.srcObject = null;
  });


});