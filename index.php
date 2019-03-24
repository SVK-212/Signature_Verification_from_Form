<?php
session_start();
$op="";
$result="";
if(isset($_POST['py_acc'])){
  $target_dir = "rect/";
$target_file = $target_dir . basename($_FILES["theFilepy"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
$check = getimagesize($_FILES["theFilepy"]["tmp_name"]);
    if($check !== false) {
      move_uploaded_file($_FILES["theFilepy"]["tmp_name"], $target_dir . "rect_sample.png");
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
// Check if image file is a actual image or fake image
exec("rect.py",$op,$result);
exec("predict.py",$op,$result);
$_SESSION['op']=$op;
$_SESSION['res']=$result;
header("Location: Testing.php");
}



?>

<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
#customers {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

#customers td, #customers th {
    border: 1px solid #ddd;
    padding: 8px;
}
s
#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #ddd;}

#customers th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #A9A9A9;
    color: white;
}
#grad1 {
    height: 1000px;
    background-color: #ffffff; /* For browsers that do not support gradients */
    background-image: linear-gradient(#ffffff, #A9A9A9); /* Standard syntax (must be last) */
}
body,h1,h2,h3,h4,h5,h6 {font-family: "Lato", sans-serif}
.w3-bar,.h1,.button {color: #000000; font-family: "Montserrat", sans-serif}
.fa-anchor,.fa-coffee {font-size:200px}
</style>
<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
        $(".add-row").click(function(){
            var name = $("#name").val();
            var email = $("#email").val();
            var markup = "<tr><td><input type='checkbox' name='record'></td><td>" + name + "</td><td>" + email + "</td></tr>";
            $("table tbody").append(markup);
        });
        
        // Find and remove selected table rows
        $(".delete-row").click(function(){
            $("table tbody").find('input[name="record"]').each(function(){
              if($(this).is(":checked")){
                    $(this).parents("tr").remove();
                }
            });
        });
    });    
</script>
</head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-colors-flat.css">
<body>
      
<div id="grad1">


<div class="container-fluid">
    <div class="row content">
      
      </div>




   <div class="w3-container w3-flat-peter-river"; style="border-radius: 10px; margin-top:100px ;  margin-left:10px"><br>
<p style="font-size: 20px; font-family: 'Calibri';" ><u>Upload form for Signature Verification:</u> </p>
<center><form method="post" action="" enctype="multipart/form-data"></center>
<input type="file" id="theFilepy" name="theFilepy"><br><br><br>
<center><input style="color: #000000;" type="submit" name="py_acc" value="Upload"></center>
</form>

</div>
</div>
</div>
</body>
</html>
