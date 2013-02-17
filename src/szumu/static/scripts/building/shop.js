$(function(){
	$('#shop-private-send-article').submit(function(){
		var title = $("#title").val()
		var content = KE.util.getData('content');
		var shopid = $("#shopid").val();
		$("#content").attr("value", content)
		$.ajax({
			url: '/shop/private/article/new/' + shopid ,
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
					$S.notice('发表成功~',1500);
					setTimeout(function(){location.reload();},2000);
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

	$('#shop-private-del-article').submit(function(){
		$.ajax({
			url: '/shop/private/article/del' ,
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
					$S.notice('删除成功~',1500);
					setTimeout(function(){location.reload();},2000);
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


	$(".del-article-btn").click(function(){
        var aid = $(this).attr('href').replace('#del-id:','')
        $("#del-article-id").attr('value', aid);
        $('#shop-private-del-article').submit();
	});
});
