# -*- coding: utf-8 -*-
<html>
<head>
<title>Zeigest Border</title>
<style type="text/css">
#map{
	background-color:red;
/*	background:url(background.gif);
	background-size:100% 100%;
	background-repeat:no-repeat;
	width:100%;
	height:1000px;*/
}

</style>
<script type="text/javascript">
 function resize(){
 var imageH =  document.getElementById("modelmap").clientHeight;
 var layerMap =document.getElementById("map");
 layerMap.height=imageH;
 console.log(layerMap.height);
}
</script>

</head>

<body>
    % if request.session.peek_flash():
    <div id="flash">
        <% flash = request.session.pop_flash() %>
        % for message in flash:
        ${message}<br>
        % endfor
    </div>
    % endif
	<img src="static/logo.png"/>
    <div id="page">
        ${next.body()}
    </div>
    <div id="footer">
        Feel free to propose a new css :p
    </div>
</body>
</html>
