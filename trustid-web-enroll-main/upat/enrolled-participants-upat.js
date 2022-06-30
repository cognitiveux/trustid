
$(document).ready(function (){

  $("#logout-btn").hide();

  let organization = "upat";
  let click_button = document.querySelector("#logout-btn");

  click_button.addEventListener('click', function() {
    fetch("logout.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        body: `organization=${organization}`,
      })
      .then((response) => response.text())
      .then(function(res) {
        window.location.href = "login_upat.php";
      });
  });

  fetch("fetch_participants.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        body: `organization=${organization}`,
      })
      .then((response) => response.text())
      .then(function(res) {
        console.log(res);
        var result = JSON.parse(res);

        if (result.code == 200) {
            document.getElementById("result").innerHTML = result.msg;
            $("#logout-btn").show();
        }
        else {
            document.getElementById("result").innerHTML = result.msg;
            $("#logout-btn").hide();
        }
      });

});