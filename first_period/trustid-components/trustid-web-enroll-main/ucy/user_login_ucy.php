<?php
	session_start();

	$username_array = array(
		"ucy" => "64rfM9k8Gd7K5DbZjg4p"
	);

	$username = $_POST['username'];
	$password = $_POST['password'];


	if (!array_key_exists($username, $username_array)) {
		$_SESSION["logged_in_ucy"] = False;
		$msg = '<div class="style-msg errormsg"><div class="sb-msg"><i class="icon-remove"></i><strong>Oh snap!</strong> Incorrect credentials.</div></div>';
		$response = array(
			'code'=> 401,
			'msg'=> $msg
		);
		echo json_encode($response);
		exit;
	}
	else {
		$stored_password = $username_array[$username];

		if (strcmp($stored_password, $password) != 0) {
			$_SESSION["logged_in_ucy"] = False;
			$msg = '<div class="style-msg errormsg"><div class="sb-msg"><i class="icon-remove"></i><strong>Oh snap!</strong> Incorrect credentials.</div></div>';
			$response = array(
				'code'=> 401,
				'msg'=> $msg
			);
			echo json_encode($response);
			exit;
		}
		else {
			$msg = '<div class="style-msg successmsg"><div class="sb-msg"><i class="icon-thumbs-up"></i><strong>Login success.</div></div>';
			$_SESSION["logged_in_ucy"] = True;
			$response = array(
				'code'=> 200,
				'msg'=> $msg
			);
			echo json_encode($response);
			exit;
		}
	}

?>
