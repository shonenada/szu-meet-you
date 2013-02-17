$(function(){
	$("#shadow").hide();
	$(".room-hide").hide();
	$(".roomsite-block-content").hide();
	$(".btn-house").click(function(){
		$("#shadow").fadeIn().delay(150).fadeOut();
		var id = $(this).attr('href');
		id = id.replace("#btn-","");
		var thing = "#room-" + id;
		setTimeout(function(){
			$("#roomsite").show();
			$("#buildings-div").hide();
			$("#quit").hide();
			$("#leave").show();
			$(thing).show();
			$(".roomsite-block-content").hide();
			$(".roomsite-block-content-1").show();
		},500);
	});
	
	$(".roomsite-btn").click(function(){
		var id = $(this).attr('href');
		id = id.replace("#id:","")
		thing = '.roomsite-block-content-' + id
		$(".roomsite-block-content").hide();
		$(thing).show();
	});

	
	$("#leave").click(function(){
		$("#shadow").fadeIn().delay(150).fadeOut();
		setTimeout(function(){
			$("#buildings-div").show();
			$("#quit").show();
			$(".room-hide").hide();	
			$("#leave").hide();
		},500);
	})
});