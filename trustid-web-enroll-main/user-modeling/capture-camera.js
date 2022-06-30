
$(document).ready(function (){

  let camera_button = document.querySelector("#start-camera");
  let video = document.querySelector("#video");
  let click_button = document.querySelector("#click-photo");
  let stop_button = document.querySelector("#stop-photo");
  let canvas = document.querySelector("#canvas");
  let recording_button = document.querySelector("#recording");
  let oTimer;
  //let video_area = document.querySelector("#video-area");

  camera_button.addEventListener('click', async function() {
      let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      $("#video-area").show("slow");
      video.srcObject = stream;
  });

  click_button.addEventListener('click', function() {
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
      let image_data_url = canvas.toDataURL();
      const base64Canvas = image_data_url.split(';base64,')[1];
      console.log(base64Canvas);
      let email = $('#email').val();

      fetch("save_img.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        body: `img_data=${base64Canvas}&email=${email}`,
      })
      .then((response) => response.text())
      .then((res) => (document.getElementById("result").innerHTML = res));
  });

  recording_button.addEventListener('click', function() {
    oTimer = setInterval(Recording, 500);
  });

  function Recording() {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let image_data_url = canvas.toDataURL();
    const base64Canvas = image_data_url.split(';base64,')[1];
    console.log(base64Canvas);
    let email = $('#email').val();

    fetch("save_img.php", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      },
      body: `img_data=${base64Canvas}&email=${email}`,
    })
    //.then((response) => response.text())
    //.then((res) => (document.getElementById("result").innerHTML = res));
  }

  stop_button.addEventListener('click', function() {
      const stream = video.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach(function(track) {
        track.stop();
      });

      video.srcObject = null;

      $("#video-area").hide("slow");
      clearInterval(myVar);
  });


});