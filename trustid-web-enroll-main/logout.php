<?php
	session_start();
	$organization = $_POST['organization'];
	$session_logged_in = "logged_in_".$organization;
	unset($_SESSION[$session_logged_in]);
?>
