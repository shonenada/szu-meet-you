$(function(){
 
	$(".roomsite-block-content").hide();
	$(".roomsite-block-content-1").show();

	$(".roomsite-btn").click(function(){
		var id = $(this).attr('href');
		id = id.replace("#id:","")
		thing = '.roomsite-block-content-' + id
		$(".roomsite-block-content").hide();
		$(thing).show();
	});

	
	$("#leave").click(function(){
		$("#map").fadeOut("fast");
		setTimeout(function(){ location.href = "/map" }, "300");
	});

	$('#rent-form').submit(function(){
		$.ajax({
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
					$S.notice('申请成功~',1500);
					setTimeout(function(){location.href="/map"},2000)
				}
				else{
					$S.alert(response.messages.join(','),2000);
				}
			},
			error: function() {
				$S.error('程序发生错误，请联系管理员！');
			}
		});
		return false;
	});


});