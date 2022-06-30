<?php
	$dir = 'user_images/';
	$email = $_POST['email'];
	$pose = $_POST['poseType'];
	$img_data = $_POST['img_data'];
	$folder_path = $dir.$email.'/'.$pose;
	$success = False;
	$msg = "OK";

	if (!file_exists($folder_path)) {
		mkdir($folder_path, 0755, true);
	}

	$img_data = str_replace('data:image/png;base64,', '', $img_data);
	$img_data = str_replace(' ', '+', $img_data);

	$curl = curl_init();
	$payload = json_encode( array( "image"=> $img_data ) );

	curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);

	curl_setopt_array($curl, array(
		CURLOPT_URL => 'https://api.trustid-project.eu/backend/head_pose_classification',
		CURLOPT_RETURNTRANSFER => true,
		CURLOPT_ENCODING => '',
		CURLOPT_MAXREDIRS => 10,
		CURLOPT_TIMEOUT => 30,
		CURLOPT_FOLLOWLOCATION => true,
		CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
		CURLOPT_CUSTOMREQUEST => 'POST',
		CURLOPT_POSTFIELDS => $payload,
		CURLOPT_HTTPHEADER => array(
			'Content-Type: application/json'
		),
	));

	$response = curl_exec($curl);

	if ($response === false) {
		$response = curl_error($curl);
		$msg = "ERROR";

		$result = array(
			'code'=> 500,
			'msg'=> $msg
		);
		echo json_encode($result);
		exit;
	}
	else {
		$json = json_decode($response, true);

		if ($json['resource_str'] === $pose) {
			$success = True;
		}

	}

	curl_close($curl);


	if ($success) {
		$output_file = $folder_path.'/'.uniqid().'-'.time().'-'.$email.'.png';
		file_put_contents($output_file, base64_decode($img_data));
		$msg = "OK";
	}
	else {
		$misclassified_folder_path = $dir.$email.'/'.$pose.'/misclassified';

		if (!file_exists($misclassified_folder_path)) {
			mkdir($misclassified_folder_path, 0755, true);
		}

		$output_file = $misclassified_folder_path.'/'.uniqid().'-'.time().'-'.$email.'.png';
		file_put_contents($output_file, base64_decode($img_data));
		$msg = "RETRY";

	}

	$result = array(
		'code'=> 200,
		'msg'=> $msg
	);
	echo json_encode($result);

?>
