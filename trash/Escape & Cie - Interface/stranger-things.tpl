<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Stranger Things interface</title>
	<link rel="stylesheet" type="text/css" href="css/style.css">
	<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
	<script type="text/javascript" src="script.js"></script>
</head>
<body>
	<nav class="navbar navbar-light bg-light">
	  	<span class="navbar-brand mb-0 h1">Escape & Cie Interface Gamemaster</span>
		<a href="/" class="btn btn-primary">Accueil</a>
	</nav>
	<div class="container">
		<div class="title"><h1>STRANGER THINGS</h1></div>
		<form action="stranger-things" method="post">
			<div class="row">
				<div class="col">
			        <label class="head_block">Video Brief</label>
			        <div class="row">
			        	<div class= "col">
			        		<button id="START" type=submit name="executer" value="START">
								<img src=img/icons8-play-100.png>
							</button>
			        	</div>
			        	<div class="col">
			        		<p class="time" id="time_start"></p>
			        	</div>
			        </div>
				</div>
			</div>
			<div class="row">
				<div class="col-sm-6">
			        <label class="head_block">Salle Claire</label>
			        <div class="row">
			        	<div class= "col">
			        		<button id="START" type=submit name="executer" value="START">
							</button>
			        	</div>
			        	<div class="col">
			        		<p class="time" id="time_start"></p>
			        	</div>
			        </div>
			    </div>
			    <div class="col-sm-6">
			        <label class="head_block">Salle Sombre</label>
			        <div class="row">
			        	<div class= "col">
			        		<button id="START" type=submit name="executer" value="START">
							</button>
			        	</div>
			        </div>
				</div>
			</div>
			<div class="row">
				<div class="col">
			        <label class="head_block">La Foret</label>
			        <div class="row">
			        	<div class= "col">
			        		<button id="START" type=submit name="executer" value="START">
							</button>
			        	</div>
			        	<div class="col">
			        		<p class="time" id="time_start"></p>
			        	</div>
			        </div>
				</div>
			</div>
		</form>
	</div>
</body>
</html>