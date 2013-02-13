(function(window, $) {	
	var szumeetyou = {};

	// 初始化全站统一元素
	szumeetyou.elementInit = function() {
		$('body').prepend($('<div id="full-screen-shadow"></div>').hide()); // 全屏遮盖层
		$('body').prepend($('<div id="message-box"></div>')); // 信息框容器
		$('body').prepend($('<div id="msg-box"></div>')); // 私信容器
		$('body').prepend($('<div id="send-msg-box"></div>')) // 私信回复容器
		$("#msg-box").append('<a href="#" id="msg-box-cls" class="box-cls shadow-cls-btn">X</a>\
			                 <div class="text-center"><h4>私信</h4></div>\
			                 <form id="del-msg-form">\
			                 <input type="hidden" name="msg_kind" id="msg-kind" value="receive" />\
			                 <div id="msg-box-content">加载中...</div>\
			                 <div id="ctrl-borad" class="text-right">\
			                 <input type="submit" value="删除选中的私信" class="btn" id="del-msg-btn" />\
			                 <input type="button" value="全选" class="btn" id="all-select-btn" />\
			                 <input type="button" value="取消全选" disabled class="btn" id="all-select-cancel-btn" />\
			                 </div>\
			                 </form>\
			                 ');
		$("#msg-box").children('div.text-center')
		            .append('<div class="text-left">\
			                <a href="#" id="receive-box-btn" class="box-btn on-chosed">收信箱</a>\
			                <a href="#" id="send-box-btn" class="box-btn">发件箱</a>\
			                </div>\
			                <div class="text-left list-item" style="margin-top:10px;">\
			                <span class="list-header" style="width:5%">选择</span>\
			                <span id="list-txt" class="list-header" style="width:12%">发件人</span>\
			                <span class="list-header" style="width:50%">私信内容</span>\
			                <span class="list-header" style="width:20%">发送时间</span>\
			                <span class="list-header re-list" style="width:5%">回信</span>\
			                </div>');

		$("#msg-box").hide();

		$("#send-msg-box").prepend('<a href="#" id="send-msg-box-cls" class="box-cls">X</a>\
			                     <form id="send-msg-form" style="display:none">\
			                     <input type="hidden" name="msg_id" id="msg-id" value="" />\
                                 <textarea id="send-msg-content" name="send_content" rows="3"></textarea>\
                                 <input type="submit" value="发送" class="btn" />\
			                    </form>\
								<form id="re-msg-form" style="display:none">\
			                     <input type="hidden" name="msg_id" id="re-id" value="" />\
                                 <textarea id="re-msg-content" name="re_content" rows="3"></textarea>\
                                 <input type="submit" value="发送" class="btn" />\
			                    </form>');
		$("#send-msg-box").hide();
	};
	
	// 全站统一信息提示框
	szumeetyou._messagebox = function(message, timeout, specialClass) {
		var entity = $('<div class="message-content"></div>')
			.hide()
			.append($('<span class="message-text"></span>').append(message))
			.append($('<a href="javascript:void(0);" class="msg-button message-close-btn">关闭</a>'))
			.addClass(specialClass);
		
		$('#message-box').append(entity);
		
		entity.fadeIn(500);
		
		if (timeout > 0) {
			setTimeout(function(){
				entity.fadeOut(500, function(){
					$(this).remove();
				});
			}, timeout);
		}
		
		entity.children('a.message-close-btn').click(function(){
			entity.fadeOut(500, function(){
				$(this).remove();
			});
		});
	};
	
	szumeetyou.shadowIn = function() { $("#full-screen-shadow").fadeIn('fast')}
	szumeetyou.shadowOut = function() { $("#full-screen-shadow").fadeOut('fast')}

	szumeetyou.notice = function(message, timeout) { this._messagebox(message, timeout, 'msg-notice'); };
	szumeetyou.alert  = function(message, timeout) { this._messagebox(message, timeout, 'msg-alert');  };
	szumeetyou.error  = function(message, timeout) { this._messagebox(message, timeout, 'msg-error'); };
		
	window.szumeetyou = window.$S = szumeetyou;
})(window, jQuery);

$(function(){
	// 初始化元素
	$S.elementInit();
	checkMsg();

	//Resize frames
	$(".map").css("height",$(window).height() - 40);
	$(".map").css("width",$(window).width() - $("#right").width() );
	$("#right-message").css("height", $(window).height() - 200 );
	$("#right-chat-msg-list").css("max-height", $(window).height() - 200 );
	if ( $(window).width() < 750 ){
		$("#right").css({'width':'0','opacity':'0.2'}); 
		$(".map").css({"height":$(window).height() - 40, "width":$(window).width() - 0 });
	}
	checkHeight();
	reSiteSouthArrow();
    bindBtnFunction();

	$("#msg-box-cls").click(function(){$("#msg-box").fadeOut();})
	$("#send-msg-box-cls").click(function(){$("#send-msg-box").fadeOut();})    

    $("#send-box-btn").click(function(){
    	getMsg(1, 'send');
    	$("#msg-kind").val('send');
    	$("#all-select-btn").removeAttr('disabled');
        $("#all-select-cancel-btn").attr('disabled',true);
        $(".re-list").hide();
    });

    $("#receive-box-btn").click(function(){
	    getMsg(1, 'receive');
	    $("#msg-kind").val('receive');
	    $("#all-select-btn").removeAttr('disabled');
        $("#all-select-cancel-btn").attr('disabled',true);
        $(".re-list").show();
	 });

    $("#all-select-btn").click(function(){
    	$(".msg-checkbox").attr('checked',true);
    	$("#all-select-cancel-btn").removeAttr('disabled');
    	$(this).attr('disabled',true);
    });

    $("#all-select-cancel-btn").click(function(){
    	$(".msg-checkbox").removeAttr('checked');
    	$("#all-select-btn").removeAttr('disabled');
    	$(this).attr('disabled',true);
    });

    $('#del-msg-form').submit(function(){
		$.ajax({
			url: '/account/msg/del/'+$("#msg-kind").val(),
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
                    $S.notice('删除成功',2000);
                    for(i=0;i<response.delID.length;i++){
                    	$("#list-item-"+response.delID[i]).slideUp()
                    }
				}else{
					$S.alert(response.message,2000);
				}
			},
			error: function(jqxhr, status) {
				$S.error('与服务器通讯发生错误，请联系站长。')
			}
		});
		return false;
	});

	$('#send-msg-form').submit(function(){
		$.ajax({
			url: '/account/msg/send',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
                    $S.notice('发信成功',2000);
                    $("#send-msg-box").fadeOut();
					$S.shadowOut();
					$("#send-msg-form").hide();
					$("#re-msg-form").hide();
				}else{
					$S.alert(response.message,2000);
				}
			},
			error: function(jqxhr, status) {
				$S.error('与服务器通讯发生错误，请联系站长。')
			}
		});
		return false;
	});
	
	
	$('#re-msg-form').submit(function(){
		$.ajax({
			url: '/account/msg/re',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
                    $S.notice('回信成功',2000);
                    $("#send-msg-box").fadeOut();
                    $("#send-box-btn").click();
				}else{
					$S.alert(response.message,2000);
				}
			},
			error: function(jqxhr, status) {
				$S.error('与服务器通讯发生错误，请联系站长。')
			}
		});
		return false;
	});

});


// 绑定按钮功能
var bindBtnFunction = function() {

	$(".send-msg-btn").click(function(){
		$("#send-msg-form").show();
        $("#send-msg-box").fadeIn();
        $("#send-msg-content").val('');
		$("#send-msg-box-cls").click(function(){$S.shadowOut();});
        var href = $(this).attr('href')
        id = href.replace('#re:','')
        $("#msg-id").val(id)
    });

    $(".add-friend-btn").click(function(){
    	userid = $(this).attr("href").replace('#addfriend:','')
    	$.ajax({
		    url:'/account/relation/friend/new/' + userid,
		    data:{'_xsrf':get_xsrf()},
		    type:'PUT',
		    async:true ,
		    dataType:'json',
		    success:function(response){
				
		    },
		    error:function(){
				//$S.error('与服务器通讯发生错误，请联系站长。');
		    },
    	});
    });


    $(".remove-friend-btn").click(function(){
    	userid = $(this).attr("href").replace('#removefriend:','')
    	$.ajax({
		    url:'/account/relation/friend/remove/' + userid,
		    type:'PUT',
		    data:{'_xsrf':get_xsrf()},
		    async:true ,
		    dataType:'json',
		    success:function(response){
				
		    },
		    error:function(){
				//$S.error('与服务器通讯发生错误，请联系站长。');
		    },
    	});
    });
	
	$(".re-msg-btn").click(function(){
		$("#re-msg-form").show();
        $("#send-msg-box").fadeIn();
        $("#re-msg-content").val('');
        var href = $(this).attr('href')
        id = href.replace('#re:','')
        $("#re-id").val(id)
    });

	$(".box-btn").click(
	    function(){
	    	$('.box-btn').removeClass('on-chosed');
	    	$(this).addClass('on-chosed');
	    }
    );

    $(".shadow-btn").click(function(){$S.shadowIn();})
    $(".shadow-cls-btn").click(function(){$S.shadowOut();$("#send-msg-form").hide();$("#re-msg-form").hide();})
}

// 检查新私信
var checkMsg = function(){
	$.ajax({
		url:'/account/msg/check',
		type:'GET',
		async:true ,
		dataType:'json',
		success:function(response){
				if( response.new_msg ){
					$("#msg-tips").html(response.num);
					$("#msg-tips-s").html("（"+response.num+"）");
					$("#msg-tips").show();
				}else{
					$("#msg-tips").hide();
				}
			},
			error:function(){
				//$S.error('与服务器通讯发生错误，请联系站长。');
			},
	});
}

// 获取私信列表
var getMsg = function(page, type){
	if (page == '' || page <= 0){
		page=1;
	}
	if( type == null){
		type = 'receive'
		$("#receive-box-btn").addClass("on-chosed");
        $("#send-box-btn").removeClass("on-chosed");
	}
	if ( type == 'send' ){
        $("#list-txt").html('发件人')
	}
	$.ajax({
		url:'/account/msg/get/' + type + '/?page='+page,
		type:'GET',
		async:true ,
		dataType:'json',
		beforeSend:function(){
				$("#msg-box-content").html('加载中...');
				$S.shadowIn();
	            $("#msg-box").fadeIn();
	            $("#msg-tips").hide();
			},
		success:function(response){
			    setTimeout(function(){
			    	$("#msg-box-content").empty();
			    for (i=0;i<response.length;i++){
			    	if (type == 'receive' && response[i].state == 0 ){
			    		newtxt = "<span style='color:#f00'>[新]</span>";
			    	}else{
			    		newtxt = '';
			    	}
			        $("#msg-box-content").append('<div id="list-item-' + response[i].id + '" class="text-left list-item">\
			        	    <span class="list-header list-check" style="width:5%"><input type="checkbox" name="delid" value="'+ response[i].id +'" class="msg-checkbox" /></span>\
			                <span class="list-header" style="width:12%">' + newtxt + response[i].man + '</span>\
			                <span class="list-header" style="width:50%">' + response[i].msg + '</span>\
			                <span class="list-header" style="width:20%">' + response[i].created + '</span>\
			                <span class="list-header re-list" style="width:5%"><a href="#re:' + response[i].id + '" class="re-msg-btn" >回信</a></span>\
			                </div>');	
			    }
			},250);
			},
		complete:function(){
			setTimeout(function(){
			if(type == 'receive'){
				$(".re-list").show();
			}
			else{
				$(".re-list").hide();
			}
			$(".re-msg-btn").click(function(){
				$("#re-msg-form").show();
                $("#send-msg-box").fadeIn();
                $("#re-msg-content").val('');
                var href = $(this).attr('href')
                id = href.replace('#re:','')
                $("#re-id").val(id)
            });
		},251);
        },
		error:function(){
				$S.error('与服务器通讯发生错误，请联系站长。');
		},
	});
}

//重新调整框架尺寸
var resize = function(width){
	$("#right-message").animate({"height":$(window).height() - 200 }, "fast");
	$("#right-chat-msg-list").animate({"max-height":$(window).height() - 200 }, "fast");
	$("#right-chat-msg-list").scrollTop($("#right-chat-msg-list").scrollHeight);
	$(".map").animate({"height":$(window).height() - 40, "width":$(window).width() - width },"fast");
}

//检查可视窗口高度，做相应动作
var checkHeight = function(){
	if ( $(window).height() < 550 ){
		$("#footer").animate({"opacity":'0.2'},"slow");
	}else{
		$("#footer").animate({"opacity":'1'},"slow");
	}
}

// 检查可视窗口宽度，做相应动作
var checkWidth = function (){
	if( $("#right").height() ) {
		if ( $(window).width() < 750 ){
			$("#right").animate({'width':'0','opacity':'0.2'},"0"); 
			resize(0);
		}else{
			$("#right").animate({'width':'250','opacity':'1'},"0");
			resize(250);
		}
	}else{
		resize(0);
	}
}

// 设置下箭头的高度
var reSiteSouthArrow = function(){
	$("#arrow_s").css('margin-top',function(){ return  $("road-bottom").height() - 55 +"px" });
}

// 鼠标悬停在用户昵称时弹窗
var buildUserInforEvent = function(){	
    $("a.user-infor").hover(function(){
    	var userid = $(this).attr('href').replace('#userid:','');
    	var classid = $(this).attr('classid');
    	getUserInfor(userid, classid);
    }, function(){ 
		var userid = $(this).attr('href').replace('#userid:','');
		$( "#user-infor-box-" + userid ).delay(200).fadeOut();
	});
}

// 获取用户信息
var getUserInfor = function(userid, classid){
	if (userid == null){
		return ;
	}
	$.ajax({
		url:'/account/userinfor/get/'+userid,
		type:'GET',
		async:true ,
		dataType:'json',
		beforeSend:function(){},
		success:function(response){
			if (response.friended){
			    var friend = '<a href="#removefriend:'+userid+'" class="remove-friend-btn">移除好友</a>'
			}else{
				var friend = '<a href="#addfriend:'+userid+'" class="add-friend-btn">加为好友</a>'
			}
			   $(".user-infor-box").remove();
			   $('body').prepend('<div class="user-infor-box" id="user-infor-box-' + userid + '">\
			   	<a href="#re:'+userid+'" class="send-msg-btn shadow-btn">私信</a> '+friend+'\
			   	 </div>');
			   offset = $('#user-infor-'+classid+'-'+userid).offset();
			   $("#user-infor-box-"+userid).offset({top:offset.top,left:offset.left});
			   $("#user-infor-box-"+userid).hover(function(){
					$("#user-infor-box-"+userid).stop().stop().show();
				},function(){
					$("#user-infor-box-"+userid).delay(200).fadeOut();
				});
			},
		complete:function(){
			    bindBtnFunction();
			},
		error:function(){
				$S.error('与服务器通讯发生错误，请联系站长。');
		},
	});
}

var StringSub = function(str, len) {
        //length属性读出来的汉字长度为1
        if (str.length * 2 <= len) {
            return str;
        }
        var strlen = 0;
        var s = "";
        for (var i = 0; i < str.length; i++) {
            if (str.charCodeAt(i) > 128) {
                strlen = strlen + 2;
                if (strlen > len) {
                    return s.substring(0, s.length - 1) + "...";
                }
            }
            else {
                strlen = strlen + 1;
                if (strlen > len) {
                    return s.substring(0, s.length - 2) + "...";
                }
            }
            s = s + str.charAt(i);
        }
        return s;
    }

$(window).resize(function(){
	checkHeight();
	checkWidth();
	reSiteSouthArrow();
});

