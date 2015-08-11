$(document).ready(function(){
	var time = new Date();
	var msg_template = '<p><span class="msg-block"><strong></strong><span class="time"></span><span class="msg"></span></span></p>';
	
	$('.chat-message button').click(function(){
		var input = $(this).siblings('span').children('input[type=text]');		
		if(input.val() != ''){
			add_message('You','img/demo/av1.jpg',input.val(),true);
		}		
	});
	
	$('.chat-message input').keypress(function(e){
		if(e.which == 13) {	
			if($(this).val() != ''){
				add_message('send',$(this).val(),true);
			}		
		}
	});
	 conn.onmessage = function(e) {
		add_message('receive',e.data,true)
	}
   	var i = 0;
	function add_message(name,msg,clear) {
		i = i + 1;
		var  inner = $('#chat-messages-inner');
		var hours = time.getHours();
		var minutes = time.getMinutes();
		if(hours < 10) hours = '0' + hours;
		if(minutes < 10) minutes = '0' + minutes;
		var id = 'msg-'+i;
        var idname = name.replace(' ','-').toLowerCase();
		var message = {}
		message.msg = msg
		message.hostip = hostip
		conn.send(JSON.stringify(message))
		inner.append('<p id="'+id+'" class="user-'+idname+' span8">'
										+'<span class="msg-block"><strong>'+name+":"+msg+'</strong> <span class="time"> '+hours+':'+minutes+'</span>'
										+'</span></p>');
		$('#'+id).hide().fadeIn(800);
		if(clear) {
			$('.chat-message input').val('').focus();
		}
		$('#chat-messages').animate({ scrollTop: inner.height() },1000);
	}

});
