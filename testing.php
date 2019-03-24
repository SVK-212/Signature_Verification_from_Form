<?php
session_start();
?>
<p style="font-size: 20px; text-align: center; padding-top: 30px"> Test Result: 
<?php 
echo $_SESSION['op'][0]."<br>";
?>
</p>
<html>
<body>
<p style="font-size: 30px;background-color: background-color: #ffffff;
    background-image: linear-gradient(#ffffff, #A9A9A9); height: 92%; width: 100%; text-align: center; padding-top: 259px"> Testing done!</p> <br> 



 <div style="position: fixed; top: 23%; left: 48%; background-color: #00ccff; padding: 8px 8px; border-radius: 4px;"> <a href="index.php" style="text-decoration: none; padding-bottom: 10px; color: #FFFFFF;"><b>Home</b></a>
	</div>
</body>
</html>
