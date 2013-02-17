$(function(){
	$('#identity-form').submit(function(){
		$.ajax({
			url: '/office/student/reg',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
					$S.notice('学籍注册成功~',1500);
					setTimeout(function(){$("#identity-form").html("您已完成学籍注册，现已是觅友社区正式成员。")},2000)
				}
				else{
					$S.alert(response.message.join(','),2000);
				}
			},
			error: function() {
				$S.error('程序发生错误，请联系管理员！');
			}
		});
		return false;
	});
});