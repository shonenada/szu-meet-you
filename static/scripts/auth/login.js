$(function(){
	$('#login-form').submit(function(){
		$.ajax({
			url: '/auth/login',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
					$S.notice('欢迎回来觅友社区！~',1500);
					setTimeout(function(){ location.href='/home', 2000});
				}
				else{
					$S.alert(response.message.join('；'));
				}
			},
			error: function() {
				$S.error('程序发生错误，请联系管理员！');
			}
		});
		return false;
	});
});