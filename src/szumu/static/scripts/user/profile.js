$(function(){
	$('#profile-form').submit(function(){
		$.ajax({
			url: '/account/profile',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
					$S.notice('修改成功~',1500);
					setTimeout(function(){ location.href='/account/profile'}, '2000');
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