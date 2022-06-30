<?php
	session_start();

	$organization = $_POST['organization'];
	$filename = 'subscribed_users_'.$organization.'.csv';
	$data = [];
	$list_of_emails = [];

	$session_logged_in = "logged_in_".$organization;
	$login_url = "login_".$organization.".php";

	if (!isset($_SESSION[$session_logged_in]) || ($_SESSION[$session_logged_in] == False)) {
		$msg = 'You must login to view enrolled participants. Login <a href="'.$login_url.'">here</a>';
		$response = array(
			'code'=> 401,
			'msg'=> $msg
		);
		echo json_encode($response);
		exit;
	}

	if (!file_exists($filename)) {
		$msg = 'Currently there are not any enrolled participants.';
		$response = array(
			'code'=> 200,
			'msg'=> $msg
		);
		echo json_encode($response);
		exit;
	}
	else {
		$f = fopen($filename, 'r');
		while (($row = fgetcsv($f)) !== false) {
			if (!in_array($row[1], $list_of_emails)) {
				array_push($list_of_emails, $row[1]);
				$data[] = $row;
			}
		}

		fclose($f);

		$html = '<table class="table">';
		$header = true;

		foreach($data as $key=>$value){
			if ($header == true) {
				$html .= '<tr>';
				$html .= '<th>' . htmlspecialchars($value[0]) . '</th>';
				$html .= '<th>' . htmlspecialchars($value[1]) . '</th>';
				$html .= '<th>' . htmlspecialchars($value[2]) . '</th>';
				$html .= '</tr>';
				$header = false;
			}
			else {
				$html .= '<tr>';
				foreach($value as $key2=>$value2){
					if ($key2 == 2){
						$html .= '<td>' . gmdate("d-m-Y H:i:s", intval($value2)) . '</td>';
					}
					else {
						$html .= '<td>' . htmlspecialchars($value2) . '</td>';
					}
				}
				$html .= '</tr>';
			}
		}

		$html .= '</table>';
		$response = array(
			'code'=> 200,
			'msg'=> $html
		);
		echo json_encode($response);
		exit;
	}

?>
