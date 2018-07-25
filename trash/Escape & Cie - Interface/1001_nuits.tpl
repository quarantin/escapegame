<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>1001 Nuits interface</title>
	<link rel="stylesheet" type="text/css" href="css/style.css">
	<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
</head>
<body>
	<nav class="navbar navbar-light bg-light">
	  	<span class="navbar-brand mb-0 h1">Escape & Cie Interface Gamemaster</span>
		<a href="/" class="btn btn-primary">Accueil</a>
	</nav>
	<div class="container">
		<div class="title"><h1>1001 NUITS</h1></div>
		<form method="post" action="/1001_nuits">
			<div class="row">
				<div class="col">
			        <label class="head_block">Video Brief</label>
			        <div class="row">
			        	<div class= "col">
			        		<button id="BRIEF" type=submit name="executer" value="brief_nuits">
								<img src=img/icons8-play-100.png>
							</button>
			        	</div>
			        	<div class="col">
			        		<p class="time" id="time_start"></p>
			        	</div>
			        </div>
				</div>
				<div class="col">
			        <label class="head_block">Fontaine</label>
			        <div class="row">
			        	<div class= "col">
			        		<button id="FONTAINE" type=submit name="executer" value="FONTAINE">
							</button>
			        	</div>
			        	<div class ="col">
			        		<div class="row">
			        			<div class ="col">
					        		<button id="FONTAINE" type=submit name="executer" value="Ouvrir">
										<img src=img/icons8-ouvrir-100.png>
									</button>
								</div>
								<div class ="col">
									<button id="FONTAINE" type=submit name="executer" value="fermer">
										<img src=img/icons8-cadenas-100.png>
									</button>
								</div>
							</div>
			        	</div>
			        </div>
				</div>
			</div>
			<div class="row">
				<div class="col">
					<label class="head_block">Caverne</label>
				</div>
				<div class="col">
					<label class="head_block">Lampe</label>
				</div>
			</div>
		</form>
	</div>
</body>
</html>