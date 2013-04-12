$(function(){

	var get_classroom = function(classid){
		$("#classinfor-"+classid).empty();
        get_classMate(classid);
	}

	var get_classMate = function(classid){
	    $.ajax({
    		url:'/teach/mate/classid/' + classid,
		    type:'GET',
		    async:true ,
		    dataType:'json',
		    cache:false,
		    success:function(response){
		    	if(response.length>0){
			        $("#classinfor-"+classid).append('<h5>觅友社区的童鞋里修读此课程的还有：</h5>');
    				    for(i=0;i<response.length;i++){
				    	    $("#classinfor-"+classid)
					        .append("<div class='mate-box'>\
					        <a href='#userid:" + response[i]['id'] + "' \
					        class='user-infor' \
					        id='user-infor-"+classid+"-"+ response[i]['id'] +"' \
					        classid='"+classid+"' \
					        >\
					        <img \
					        class='avatar-small' \
					        src='" + response[i]['pic'] + "' \
					        />\
					        "+response[i]['nickname']+"\
					        </a>\
					        </div>");
				        }
				    $("#classinfor-"+classid).append('<br />');
		    	}
			},
			error:function(){
    		    $S.error('与服务器通讯发生错误，请联系站长。');
			},
		    complete:function(){
    			buildUserInforEvent();
    			get_class_comment(classid);
		    }
	    });
	}
    
    var get_class_comment = function(classid){
        $.ajax({
    		url:'/teach/comment/classid/' + classid,
		    type:'GET',
		    async:true ,
		    dataType:'json',
		    cache:false,
		    success:function(response){

		    	if(response.length>0){
			        $("#classinfor-"+classid).append('<h5>觅友社区的童鞋对此课的评价：</h5>');
    			    for(i=0;i<response.length;i++){
					    $("#classinfor-"+classid)
					    .append('#'+response[i]['nickname']+'说：'+
					    response[i]['comment']+'<br />'
					    );
				    }
			    }

		    	$("#classinfor-"+classid).append('发表评价：\
		    		<br />\
		    		<form class="comment-form form-search" id="comment-form-'+classid+'">\
		    		<input type="hidden" value="'+classid+'" name="classid" />\
		    		<div class="input-append">\
		    		<input type="text" name="comment" class="input-xxlarge search-query" />\
		    		<button type="submit" class="btn btn-success">发布</button>\
		    		</div>\
		    		</form>\
		    		<br />\
		        ');
			},
			error:function(){
    				$S.error('与服务器通讯发生错误，请联系站长。');
			},
		    complete:function(){
		        bindform(classid);
		        bind_xsrf($('#comment-form-'+classid));
		    }
	    });
    }

    var bindform = function(classid){
    $('#comment-form-'+classid).submit(function(){
    	$.ajax({
			url: '/teach/comment/new',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function(response) {
				if(response.success){
                    $S.notice('发布成功',2000);
                    get_classroom(classid);
				}else{
					$S.alert(response.messages.join('；'),2000);
				}
			},
			error: function(jqxhr, status) {
				$S.error('与服务器通讯发生错误，请联系站长。')
			},
			complete: function(){

			}
		});
		return false;
    });
}

	$("#shadow").hide();
	$(".room-hide").hide();
	$(".roomsite-block-content").hide();
	$(".roomsite-block-content-1").show();
	
	$(".roomsite-btn").click(function(){
		var id = $(this).attr('href');
		id = id.replace("#id:","").replace("#classid:","")
		thing = '.roomsite-block-content-' + id
		$(".roomsite-block-content").hide();
		$(thing).show();
		get_classroom(id);
	});

	
	$("#leave").click(function(){
		$("#map").fadeOut("fast");
		setTimeout(function(){ location.href = "/map" }, "300");
	});


 
});