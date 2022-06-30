
$(document).ready(function (){

  let click_button = document.querySelector("#subscribe");

  click_button.addEventListener('click', function() {
      document.getElementById("result").innerHTML = "";
      let name = $('#name').val();
      let email = $('#email').val();
      let error_flag = false;
      let error_msg = "<div class='style-msg errormsg'><div class='sb-msg'><i class='icon-remove'></i><strong>Oh snap!</strong> Full Name and Email are required fields in order to subscribe.</div></div>";

      if(name == "" || name === "") {
        //document.getElementById("result").innerHTML = "Full Name is required (*)<br/>";
        error_flag = true;
      }

      if(email == "" || email === "") {
        //document.getElementById("result").innerHTML += "Email is required (*)<br/>";
        error_flag = true;
      }

      if (error_flag == true) {
        document.getElementById("result").innerHTML = error_msg;
        return false;
      }

      fetch("subscribe_ucy.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        body: `name=${name}&email=${email}`,
      })
      .then((response) => response.text())
      .then((res) => (document.getElementById("result").innerHTML = res))
      .then((res) => $('#name').val(''))
      .then((res) => $('#email').val(''));
  });

});
