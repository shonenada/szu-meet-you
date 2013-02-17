$(function(){

	$(".hash-btn").click(function(){
		var hash = $(this).attr("href");
		url = hash.replace("#", "")
		setTimeout(function(){ location.href = url }, "300");
	});
	
	$("#arrow_n").click(function(){
		$("#map").animate({'margin-top':'100%'}, "200");
	});
	
	$("#arrow_e").click(function(){
		$("#map").animate({'margin-left':'-100%'}, "300");
	});
	
	$("#arrow_s").click(function(){
		$("#map").animate({'margin-top':'-100%'}, "200");
	});
	
	$("#arrow_w").click(function(){
		$("#map").animate({'margin-left':'100%'}, "300");
	});
	
	$("#quit").click(function(){
		$("#map").fadeOut("fast");
		setTimeout(function(){ location.href = "/map" }, "300");
	});
	
	$(".building-btn").click(function(){
		$("#map").fadeOut("fast");
	});

}) 