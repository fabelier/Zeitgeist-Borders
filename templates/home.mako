<html>
  <head>
    <title>Google Borders Viewer</title>
	<meta name="description" content=" Google-Borders.com aims at providing a visualization of ALL country specific google search engines suggestions. This way, you can have fun discovering unknown differences or similarities between a great number of countries. " >
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
	<meta name="keywords" content="google,borders,keyword,search,autocompletion,mapping,humanities,completion,suggestion" >
    <link rel="stylesheet" type="text/css" href="http://www.google.com/css/go-x.css">
    <link rel="stylesheet" type="text/css" href="http://www.google.com/css/modules/buttons/g-button.css">
  	<script type="text/javascript" src="static/lib/jquery-1.7.1.min.js"></script>
  	<script type="text/javascript" src="static/lib/underscore-min.js"></script>
	<script type="text/javascript" src="static/lib/raphael-min.js"></script>
	<script type="text/javascript" src="static/lib/scale.raphael.js"></script>
  	<script type="text/javascript" src="static/lib/worldmap.js"></script>

	<style type="text/css">
			.qr{padding:5px;border-bottom: solid 1px #c0c0c0;display:block;overflow: hidden;}
			.qr:hover{background-color:#e9e9e9;}
			.qrt{float:left;display:block;}
			.qrp{float:right;display:block;}
			.qrc{text-align:left;float:left;width:300px;height:300px;border-right:solid 1px #c0c0c0;display:block;position:relative;}
			.lqr{overflow-y:scroll;height:270px;}
			clear { clear: both; }
					
	#countriesLabel{width:596px;height:35px;position:absolute;display:block;left:360px;top:390px;font-size:10px;overflow-y:scroll;border-top:solid 1px #c0C0C0;text-align:center;}
			#loading{position:absolute;left:170;top:240;}
			#error{position:absolute;left:120;top:220;text-align:center;width:150px;}
			.bt{width:71px;height:30px;position:relative;float:left;background:url(static/imgs/buttons.gif);margin-left:2px;margin-right:2px;
			}
			#bt-search{}
			#bt-search:hover{background-position:0px 31px;}
			#bt-random{background-position:71px 0px;}
			#bt-random:hover{background-position:71px 31px;}
			#bt-exemple{background-position:143px 0px;}
			#bt-exemple:hover{background-position:143px 31px;}
			#content{height:31px;}
			.teaser{font-size:15px;position:relative;float:left;}
			.share{margin-left:2px;margin-right:2px;position:relative;float:right;width:200px;}
	</style>
  
  </head>

  <body id="container" >
    <h1>
      <table>
       <tr>
         <td><a href="/">
             <img 
                  src="static/imgs/borders_logo.gif"
                  alt="Google Books"></a>
         </td>
         <td style="padding-left: 0cm; padding-top: 0.035em; color: #009925; font-size: 28px;">What are the borders of Google Autocomplete ?</td>
       </tr>
      </table>
    </h1>
	<blockquote>

	  <div style="height:30px;width:945px;">
		<div class="teaser">
		Map what google <b>suggests</b> for :
	    <input type="text"
	           name="content"
			   id="content"
	           size="34"
	           value="How to"
	           maxlength=240>
	</div>
		<div class="bt" id="bt-search"/></div>
		<div class="bt" id="bt-random"/></div>
    	<div class="bt" id="bt-exemple"/></div>
<div class="share">

	<!-- AddThis Button BEGIN -->
	<div class="addthis_toolbox addthis_default_style ">
		<a class="addthis_button_preferred_4"></a>
	<a class="addthis_button_preferred_1"></a>
	<a class="addthis_button_preferred_2"></a>
	<a class="addthis_button_preferred_3"></a>
	<a class="addthis_button_compact"></a>
	<a class="addthis_button_google_plusone"></a>
	</div>
	<script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#pubid=ra-4f378cbf56f9333b"></script>
	<!-- AddThis Button END -->

		<div>
	  </div>
	  
	</blockquote>
	<div id="loading"><img src="static/imgs/loading.gif"></div>
	<div id="error"></div>
	
	<div id="resultContainer"  style="margin-left:40px;width:900px;height:300px;border:solid 1px #c0c0c0">
		
		<div class="qrc">
			<div class="qr" style="background-color:#e9e9e9;">
			<div class="qrt">Results </div>
			<div class="qrp">Weight</div>
			</div>
			<div class="lqr" >
			</div>
		</div>
		<div id="map">
			<div id="mapHolder"></div>
			<div id="countriesLabel">Select a result to see in witch country it's proposed</div>
		</div>
	</div>
<!--
	SOCIAL AREA
 -->

	<center>Run your own experiment ! Raw data is available for download
	  <a href="#" id="rawdata">here</a>.<br/>
	Contact us <a href="https://docs.google.com/spreadsheet/viewform?formkey=dHpVYWZCVUNIT3c3RjZIZncxMDdscFE6MQ"> here</a>
	</center>

	    <center>
	    <div id="about" style="border-top: 1px solid #ccc;">
			<span style="transform:rotate(180deg);-webkit-transform:rotate(180deg);
			-moz-transform:rotate(180deg);-o-transform:rotate(180deg);
			filter:progid:DXImageTransform.Microsoft.BasicImage(rotation=2); display: inline-block;">&copy;</span> 2011 Fabelier -
	      <a href="http://www.fabelier.org" target="_blank">About Fabelier</a> -

	      <a href="http://support.google.com/websearch/bin/answer.py?hl=en&answer=106230" target="_blank">About Google Autocomplete</a> -
	      <a href="explication.html">About Google Borders</a>
	    </div>
	</center>
<script>

var results 		= [];
var countries;
var paper;
var similarCountry	= [];
var colors 			= ['','#000','#2a2a2a','#494949'];
var radomrequest	= ['how','why','where is','when','what','abortion','How to','why she','am I','Why he','by pass','where are','how to learn','death penalty','what is the best','why children','why men','why woman','why god','why he','why parents','how to be','why he is'];
// share un higtlight

function resultsPush(newresult,country,poid){
	//console.log(newresult);
	var estilla = false;
	for (var i = 0; i < results.length; i++){
		if(results[i].label!=undefined){
			if(results[i].label.toLowerCase()==newresult.toLowerCase()){
				var myresult=results[i];
				estilla=true;
			}
		}
	}
	if(estilla==false){
		results.push({'label':newresult,'country':[{'c':cleanIDcountry(country),'p':poid}],'poid':1});
	}else{
		myresult.country.push({'c':cleanIDcountry(country),'p':poid});
		myresult.poid+=1;
	}
}
function cleanIDcountry(id){
	 id     = id.toUpperCase()
	 comsid = id.search("COM.")
	 cosid  = id.search("CO.")
	//console.log("----> "+id)
	if(id!="COM"){
	 if(comsid!=-1){
		id=id.slice(4,id.length)
	 }else if(cosid!=-1 ){
		id = id.slice(3,id.length)
	 }
	}
	return id
}
function hightlightCountrie(myce){
	 id     = myce.c.toUpperCase()
	 //console.log(myce);
	 var mycountryPath = $('#'+id)
	 $('#'+id).attr({
         'fill': colors[myce.p],
         'stroke': '#fff'
     });
}
function unlightResult(){
	$(".lqr").children().show();
	/*for (var i = 0; i < myElement.country.length; i++){
	}*/
}
function hightlightResult(id){
	$(".lqr").children().hide();
	similarCountry=[];
	var similarCountryTemp=[];
	var estilla;
	var idc= id.toUpperCase()
	var resultTemp=[];
	$("#countriesLabel").text(cnq(idc));
	
	for (var i = 0; i < results.length; i++){
		for (var j = 0; j < results[i].country.length; j++){
			if( results[i].country[j].c==idc){
				resultTemp.push([i,results[i]])
				$("#"+i).show();
			}
			/*
			if(estilla==true && j==results[i].country.length-1){
				similarCountry = concat(similarCountry,similarCountryTemp);
			}*/
		}
		//console.log(resultTemp);
	}
}

function sortByPoid (myarray){
	myarray.sort(function (a, b) {
	    if (a.poid < b.poid) return 1;
	    if (b.poid < a.poid) return -1;
	    return 0;
	});
}
function resultOver(query){
	var myElement = results[query];
	var countryName;
	var countryListeSt="";
	
	for (var i = 0; i < myElement.country.length; i++){
		var myce=myElement.country[i];
		countryListeSt += cnq(myce.c)+" - "
		hightlightCountrie(myce);
		//console.log(myce);
	}
 	$("#countriesLabel").text(countryListeSt);
}
function viderLesResult(){
	$(".lqr").text("");
}
function resultOut(){
	$('#mapHolder').children().children().children().attr({
        fill: "#888888",
        stroke: "#fff"
    }, 300);
	/*if(countryListeSt!=undefined){
		$("#countriesLabel").text(countryListeSt);
	}*/
}
function randomQuery (){
	randomme = radomrequest[Math.floor(Math.random()*radomrequest.length)]
	searchBorders(randomme.toLowerCase());
	//$('#content').atr('value',randomme);
	//console.log(window.location.protocol+'//'+window.location.host+window.location.pathname+"#"+escape(randomme));
	//window.location(window.location.protocol+'//'+window.location.host+window.location.pathname+"#"+randomme);
}

function cnq(query){
	var label = countries.countries[query.toLowerCase()];
	console.log(label)
	if(label==undefined){return "Sorry, I don't find this country "+query }
	else{return label}
}
function drawResult(country){
	viderLesResult();
	var template="<div id='{i}' class='qr' onMouseOver='resultOver(this.id);' onMouseOut='resultOut();'><div class='qrt'>{result}</div><div class='qrp'>{poid}</div></div>";
	var newtemplate="";
	for (var i = 0; i < results.length; i++){
		newtemplate = template.replace(/{result}/, results[i].label);
		newtemplate = newtemplate.replace("{poid}", results[i].poid);
		newtemplate = newtemplate.replace("{i}", i);
		$(newtemplate).appendTo('.lqr');
	}
}
function searchBorders (content){
	$("#error").hide();
	$(".lqr").children().hide();
	$("#loading").children().show();
	$('#content').attr('value',unescape(content));
	var queryurl = "search.json?q="+content;
	$.getJSON(queryurl+"&callback=?",function(data) {
		results    = [];
		var items  = [];
		var taille = 0
		$.each(data.result, function(key, val) {
				for (i=0; i<val.length; i++){
		 			resultsPush(val[i],key,val.length-i);
				}
			taille++;
  		});
		if(results.length<4){
					$("#error").show();
					$("#error").text("Oooops sorry, this is an error here ! We don't know what is it, but just for informations :  Google don't give autocompletion for sex / porn query. :-) ...");
		}
		sortByPoid(results);
		drawResult(null);
		$("#loading").children().hide();
	});
	window.location.hash = "#"+escape(content);
	document.title = "What is the google borders for '"+content+"' ?";
	$('#rawdata').attr('href',queryurl);
	
}

$(document).ready(function() {
	var anchorvalue;
	var url = document.location;
	var strippedUrl = url.toString().split("#");
	if(strippedUrl.length > 1)
	anchorvalue = strippedUrl[1];
	
	$.getJSON("static/countries.json",function(data) {
		countries = data;
	});
	$('#bt-random').click(function() {
		randomQuery();
	});
	$('#bt-search').click(function() {
		searchBorders($('#content').attr('value').toLowerCase());
	});
	$('#bt-exemple').click(function() {
		window.location="static/explication.html"
	});
	drawMap();
	
	//URL anchor search
	if (anchorvalue==undefined){
		randomQuery ();
	}else{
		searchBorders(unescape(anchorvalue));
		$('#content').attr('value',unescape(anchorvalue));
	}
	$("#content").keypress(function(event) {
		if ( event.keyCode == 13 ) {
			searchBorders($('#content').attr('value').toLowerCase());
	  	}
	});
	
	var test = "http://www.google.cz/complete/search?client=chrome&q=culture"
	$('#result').load(test, function() {
	  alert('Load was performed.');
	});
});
</script>

  </body>
</html>