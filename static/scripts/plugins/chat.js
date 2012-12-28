$(function(){
	var reg = /map\/[0-9]+/
	var mapid = reg.exec(location.href);
	mapid = mapid[0].replace("map/", "");
	var lastid = '';
	var contaier = $('#right-chat-msg-list');
	var show_message = function(msg, msg_type, id) {
		if (lastid == id ) { return ;}
		if (typeof msg_type == 'undefined') msg_type = 'info';
		msg = $('<div/>').text(msg).html();
		msg = msg.replace("\n", "<br />");
		
		var template = $("<div><\/div>")
			.addClass('alert-message')
			.addClass('block-message')
			.addClass(msg_type);
		if (typeof id != 'undefined') {
			template.attr('id', id);
		}
		contaier.append(template.html(msg).hide().fadeIn("fast"));
		lastid = id;
	};

	var update = function (){
		$.ajax({
			url: '/chat/messages',
			type: 'get',
			dataType: 'json',
			success: function(r) {
				try {
					show_message(r.msg, 'info', r.id);
					$("#right-chat-msg-list").scrollTop(document.getElementById('right-chat-msg-list').scrollHeight);
					update();
				} catch (e) {
					//show_message('发生错误：' + e, 'alert');
				}
			},
			error: function(jqxhr, status, thrown) {
				if (status == 'abort' || status == 'timeout' || xhr.status == 0) return;
				$S.alert('与服务器通讯发生错误：' + status.toString(), 2000);
				//show_message('与服务器通讯发生错误：' + status.toString(), 'error');
			},
		});
	}
	$('#message_form').submit(function(){
		$.ajax({
			url: '/chat/messages',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function() {
				update();
	            $("#right-chat-msg-list").scrollTop(document.getElementById('right-chat-msg-list').scrollHeight);
				$("#chat_content").val("");
			},
			error: function(jqxhr, status) {
				if (status == 'abort') return;
				if (status != 'timeout') {
					$S.alert('与服务器通讯发生错误：' + status.toString(), 2000)
					//show_message('向服务器发送消息时发生错误：' + status.toString(), 'error');
				}
				update();
			},
		});
		return false;
	});
	
	update();
});