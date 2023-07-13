<?php
	$name = $_POST['name'];
	$email = $_POST['email'];
	$filename = 'subscribed_users_ucy.csv';

	if (!file_exists($filename)) {
		$data = [
			['Full Name', 'Email', 'Date Enrolled'],
		];
	}
	else {
		$data = [];
	}

	$append_data = [$name, $email, time()];
	array_push($data, $append_data);

	$f = fopen($filename, 'a');

	if ($f === false) {
		die('Unable to subscribe. Try again later.');
	}

	foreach ($data as $row) {
		fputcsv($f, $row);
	}

	fclose($f);
	echo '<div class="style-msg successmsg"><div class="sb-msg"><i class="icon-thumbs-up"></i><strong>Thank you!</strong> You have subscribed to the user study. An email will be sent to you with more information.</div></div>';
?>
