<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">

<head>

<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">

<title>News Feed Classifier</title>
<script type="text/javascript" src="tabber.js"></script>
<link rel="stylesheet" href="newsfeed.css" TYPE="text/css" MEDIA="screen">

<script type="text/javascript">

document.write('<style type="text/css">.tabber{display:none;}</style>');

</script>
</head>
<body>

<?php
 
	require_once("facebook.php");
	class Feed
	{
		public $actor_id;
		public $message;
		public $desc;
		public $target_id;
		public $permalink;
		public $viewer_id;
	}

	$config = array();
	$config[‘appId’] = '287218321346565';
	$config[‘secret’] = 'c1773be395aabf0e9916db9ca110009c';
	$config[‘fileUpload’] = false; // optional

	$facebook = new Facebook($config);
  $app_id = '287218321346565';
  $app_secret = 'c1773be395aabf0e9916db9ca110009c';
  $my_url = 'https://apps.facebook.com/ucsd_noobs/';

  $code = $_REQUEST["code"];
 
 //auth user
 if(empty($code)) {
    $dialog_url = 'https://www.facebook.com/dialog/oauth?client_id=' 
    . $app_id . '&redirect_uri=' . urlencode($my_url) ;
    echo("<script>top.location.href='" . $dialog_url . "'</script>");
  }

  //get user access_token
  $token_url = 'https://graph.facebook.com/oauth/access_token?client_id='
    . $app_id . '&redirect_uri=' . urlencode($my_url) 
    . '&client_secret=' . $app_secret 
    . '&code=' . $code;
  $access_token = file_get_contents($token_url);
//+post_id,+actor_id,+target_id,+message+
  // Run fql query
  $fql_query_url = 'https://graph.facebook.com/'
    . '/fql?q=SELECT+post_id,+actor_id,+target_id,+message,+description,+viewer_id,+permalink+FROM+stream+WHERE+filter_key+in+(SELECT+filter_key+FROM+stream_filter+WHERE+uid=me())+AND+is_hidden+=+0'
    . '&' . $access_token;

  $fql_query_result = file_get_contents($fql_query_url);
  $fql_query_obj = json_decode($fql_query_result, true);


  //display results of fql query
//  echo '<pre>';
  //print_r("query results:");
  //print_r($fql_query_obj);
  //echo '</pre>';
  $myArray =array();

foreach($fql_query_obj['data'] as $record )
{
  $myObj = new Feed();
  $myObj->actor_id = $record['actor_id'];
  $myObj->target_id = $record['target_id'];
  $myObj->message = $record['message'];
  $myObj->desc = $record['description'];
  $myObj->permalink = $record['permalink'];
  $viewer_id = $record['viewer_id'];
  $myArray[$record['post_id']] = $myObj;
 
}
  file_put_contents('sample_feed.txt',$fql_query_result);
  system('/var/www/myapp/parser.py ');
  echo '<div class="tabber"><div id="header"></div><br/><div class="tabber">';
  $handle = opendir($viewer_id);

  while($file = readdir($handle))
  {
	if($file == "." || $file == "..")
		continue;
	// echo the tab here
	echo ' <div class="tabbertab">  <h2>'.substr($file, 0, -4).'</h2><ul>';
  	$file_handle = fopen($viewer_id."/".$file,'r');
	while($line = fgets($file_handle) )
	{       $line = rtrim($line); 
		$feed = $myArray[$line]; 
		//echo the content here
		echo '<li>'.$feed->message.' <a href="'.$feed->permalink . '" target="_blank">more...</a></li>'; 

	}
	fclose($file_handle);
	//close the tab here
	echo'</ul></div>';
  }
  closedir($handle);
?>

</body>
</html>

