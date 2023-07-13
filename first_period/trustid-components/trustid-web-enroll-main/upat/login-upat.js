
$(document).ready(function (){

  let click_button = document.querySelector("#login-btn");

  click_button.addEventListener('click', function() {
      document.getElementById("result").innerHTML = "";
      let username = $('#username').val();
      let password = $('#password').val();
      let error_flag = false;
      let error_msg = "<div class='style-msg errormsg'><div class='sb-msg'><i class='icon-remove'></i><strong>Oh snap!</strong> Username and Password are required fields in order to login.</div></div>";

      if(username == "" || username === "") {
        error_flag = true;
      }

      if(password == "" || password === "") {
        error_flag = true;
      }

      if (error_flag == true) {
        document.getElementById("result").innerHTML = error_msg;
        return false;
      }

      fetch("user_login_upat.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        body: `username=${username}&password=${password}`,
      })
      .then((response) => response.text())
      .then(function(res) {
        var result = JSON.parse(res);

        $('#username').val('');
        $('#password').val('');

        if (result.code == 200) {
            document.getElementById("result").innerHTML = result.msg;
            setTimeout(() => {
              window.location.href = 'enrolled_participants_upat.php'
            }, 1000);
        }
        else {
            document.getElementById("result").innerHTML = result.msg;
        }
      });
  });

});
