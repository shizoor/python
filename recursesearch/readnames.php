<?php
$servername = "localhost";
$username = "root";
$password = "passwordhere";
$dbname = "mysql";

$id = intval($_GET['id']);

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT name, children FROM names where id = " . $id . ";";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "{ \"name\":  \"" .  $row["name"] . "\", \"children\": [ " . $row["children"] . " ] } "  ;
    }
} else {
    echo "0 results";
}
$conn->close();

?>
