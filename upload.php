<!DOCTYPE html>
<html>
<head>
<title>KOZNA</title>
<link rel="stylesheet" type="text/css" href="tools.css">
</head>   
<body>
    <header>
        <a href=index.html><img src=header.png alt=”header”></a>
    </header>
<nav>
    <ul>
      <li><a href="#news">News</a></li>
      <li><a href="#contact">Contact</a></li>
      <li><a href="#about">About</a></li>
    </ul>
</nav>
<article>
    <h2>Results</h2>
<?php

$user = 'root';
$password = 'root';
$db = 'ScannedRegistration';
$host = 'localhost';
$port = 8889;

$link = mysql_connect(
   "$host:$port", 
   $user, 
   $password
);
$db_selected = mysql_select_db(
   $db, 
   $link
);

$target_dir = "cars/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$target_file_show = $target_file;
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo " ";
}
$target_file = "/Applications/MAMP/htdocs/" . $target_file;
$command = "/Library/Frameworks/Python.framework/Versions/2.7/bin/python /Applications/MAMP/htdocs/python_script.py";
$output = shell_exec($command ." ". $target_file);

if($output && $output != -1){
    $records = mysql_query("SELECT * FROM cars WHERE id = ".$output);
    
    while($row = mysql_fetch_array($records))
    {
        echo "<b>Plate:</b> ". $row['Plate']."</br>";
        echo "<b>Region:</b> ".$row['Region']."</br>";
        echo "<b>Insurance:</b> ".$row['Insurance']."</br>";
        echo "<b>Duration:</b> ".$row['Duration']."</br>";
        echo "<b>Type:</b> ".$row['Type']."</br>";
        echo "<b>Brand:</b> ".$row['Brand']."</br>";
        echo "<img src=". $target_file_show ." width='100%' height='50%' alt='car_pic'>";
    }
} else if ($output == -1) {
    echo "Unable to connect to the database";
} else if ($output == 19) {
    echo "Unable to find licence plate";
}
else {
    echo "output not working";
}
?>

</article>
<footer>
    <p>KOZNA TEAM, 2017</p>
</footer>
</body>
</html>