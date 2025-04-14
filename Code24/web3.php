
<!doctype html>
<html lang="en">
	<head>
		<title>Jam It</title>
		<link rel="icon" href="/img/localos.png" type="image/png" />
		<link rel="stylesheet" href="/css/style.css" />
	</head>
    <body>
	    <header class="solid">
		    <img class="code-logo" src="/img/code.png" />
	        	<h1 id="challtitle">Jam It</h1>
		    <img class="code-logo" src="/img/localos.png" />
	    </header>
	    <div id="main">
	        <div id="inner">
                <h2 class="invalid">Gimme Beer Plz</h2>
                <div id="formbox">
                <form method="POST" action="#">
                        <input type="text" id="name" name="name" placeholder="Your name">
                        <input type="text" id="beer" name="beer" placeholder="Type of beer">
                        <input type="text" iname="amount" placeholder="Amount of beer">
                        <input type="submit" value="Submit">
                </form>
                </div>

                <?php
                    include('../../beer.php');

                    if(isset($_POST['name']) && isset($_POST['beer'])){
                        if(strcmp( $_POST['name'], $flag ) == 0){
                            if(hash('md4', $_POST['beer']) == $_POST['beer'] && hash('md5', $_POST['name']) === hash('md5', $_POST['amount'])){
                                echo("Now go and grab a beer ...<br>");
                                echo($flag);
                            }
                            else{
                                echo("Jerry has secured his beer reserve!<br>");
                            }
                        }
                        else{
                            echo("No beer for you today!<br>");
                        }

                        echo("<br>");
                    }
                ?>
            </div>
        </div>
    <footer>
        <div id="copy">Copyright &copy; Team localos 2024</div>
    </footer>
    <div class="background-image"></div>
</body>

</html>