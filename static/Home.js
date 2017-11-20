var curfew_slot=null;
var approver=null;
var curr=2;
var request=null;
var flag=0;
var out_time=null;
var in_time=null;
$(document).ready(function() {
	//executes when HTML-Document is loaded and DOM is ready
	//alert("Ready")
	var url_string=window.location.href;
	var url = new URL(url_string);
	var reqId = url.searchParams.get("req");
	//alert("reqId: "+reqId);
	request=reqId;
	if(reqId != null){
			flag=1;
			$("#viewRequestModal").modal('show');
	}
	
	//loadConversation(reqId);
});

//reply button click
function submitReply(){
		$.ajax({
        url: '/submitReply',
        data: $('#replyForm').serialize(),
        type: 'POST',
        success: function(data) {
            //alert('replied!');
            loadConversation(request);
        },
        error: function(error) {
            alert('Oops!! Something went wrong..');
        }
    });
}


$(window).on('shown.bs.modal', function(event) { 
	
	if(flag==0){
		var link = $(event.relatedTarget); // Button that triggered the modal
		var reqId = link.data('whatever');
		request=reqId;
	}
    //alert('in shown modal');
    loadConversation(request);
});

function loadConversation(reqId){
	$('#requestConversation').empty();
	request=reqId;
	document.getElementById("reply").value="";
	document.getElementById("hidden_reqId").value=reqId;
	//$('#requestConversation').empty();
	$.ajax({
        url: '/viewRequest/'+reqId,
        //data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
            //console.log(data.list_of_data);
        	//array_data = JSON.parse(data)["result"];
        	//alert('data: '+data);
			var len=data.result.length;
			var arr=data.result;
			var str='';
			for(var i=0;i<len;i++){
				//for(var j=0;j<8;j++){
					//str=str+arr[i][j]+' ';
					
				//}
				str=str+
					'<li class="list-group-item">'+arr[i][4]+
					'<div class="col-md-2"><Strong>'+arr[i][2]+
					'</Strong></div><div class="col-md-3">'+arr[i][5]+
					'</div><div class="col-md-3"><a target="_blank" href="http://127.0.0.1:5000/attachment/'+arr[i][6]+'">'+arr[i][7]+
					'</a></div>'+
					'<div class="clearfix"></div></li>';
				status=arr[i][3];
			}
			//alert('parsed data: '+str);
			var disp_status="";
			if(status==1){disp_status="Applied";}
			else if(status==2){disp_status="Pending";}
			else if(status==3){disp_status="approved";}
			else if(status==4){disp_status="Rejected";}
			$('#title').empty();
			//alert(status);
			$('#title').append(reqId+' : '+disp_status);
			
			$('#requestConversation').append(str);
        },
        error: function(error) {
            alert('Oops!! Something went wrong..');
        }
    });
}


/*
$(window).on('shown.bs.modal', function(event) { 
	//alert('baghaa');
    var link = $(event.relatedTarget); // Button that triggered the modal
    var reqId = link.data('whatever');
    //alert('element: '+recipient);
    var status="";
    document.getElementById("hidden_reqId").value=reqId;
    request=reqId;
    loadConversation(reqId);
});

function loadConversation(reqId){
	document.getElementById("reply").value="";
	$('#requestConversation').empty();
	$.ajax({
        url: '/viewRequest/'+reqId,
        //data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
            //console.log(data.list_of_data);
        	//array_data = JSON.parse(data)["result"];
        	//alert('data: '+data);
			var len=data.result.length;
			var arr=data.result;
			var str='';
			for(var i=0;i<len;i++){
				//for(var j=0;j<8;j++){
					//str=str+arr[i][j]+' ';
					
				//}
				str=str+
					'<li class="list-group-item">'+arr[i][4]+
					'<div class="col-md-2"><Strong>'+arr[i][2]+
					'</Strong></div><div class="col-md-5">'+arr[i][5]+
					'</div>'+
					'<div class="clearfix"></div></li>';
				status=arr[i][3];
			}
			//alert('parsed data: '+str);
			var disp_status="";
			if(status==1){disp_status="Applied";}
			else if(status==2){disp_status="Pending";}
			else if(status==3){disp_status="approved";}
			else if(status==4){disp_status="Rejected";}
			$('#title').empty();
			//alert(status);
			$('#title').append(reqId+' : '+disp_status);
			
			$('#requestConversation').append(str);
        },
        error: function(error) {
            alert('Oops!! Something went wrong..');
        }
    });
}



$(window).on('shown.bs.modal', function(event) { 
    $('#requestConversation').empty();
    var link = $(event.relatedTarget); // Button that triggered the modal
    var reqId = link.data('whatever');
    //alert('element: '+recipient);
    var status="";
    document.getElementById("hidden_reqId").value=reqId;
    
    $.ajax({
        url: '/viewRequest/'+reqId,
        //data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
            //console.log(data.list_of_data);
        	//array_data = JSON.parse(data)["result"];
        	//alert('data: '+data);
			var len=data.result.length;
			var arr=data.result;
			var str='';
			for(var i=0;i<len;i++){
				//for(var j=0;j<8;j++){
					//str=str+arr[i][j]+' ';
					
				//}
				str=str+
					'<li class="list-group-item">'+arr[i][4]+
					'<div class="col-md-2"><Strong>'+arr[i][2]+
					'</Strong></div><div class="col-md-5">'+arr[i][5]+
					'</div>'+
					'<div class="clearfix"></div></li>';
				status=arr[i][3];
			}
			//alert('parsed data: '+str);
			var disp_status="";
			if(status==1){disp_status="pending";}
			else if(status==2){disp_status="approved";}
			else if(status==3){disp_status="rejected";}
			else if(status==4){disp_status="cancelled";}
			$('#title').empty();
			$('#title').append(reqId+' : '+disp_status);
			
			$('#requestConversation').append(str);
        },
        error: function(error) {
            alert('Oops!! Something went wrong..');
        }
    });
    
});
* 
*/


$(window).on('hidden.bs.modal', function() { 
    $('#viewRequest').modal('hide');
    //alert('hidden');
});

function reset(){
	window.location.href = 'Home.html';
}

function addStudent(){
	var str='<div class="form-group">'+
			'<label class="control-label col-sm-2">Student '+curr+'</label>'+
			'<div class="col-sm-5">'+
			'<input class="form-control text-uppercase" id="student'+curr+'" placeholder="Enter RollNo" name="student'+curr+'">'+
			'</div>'+
			'</div>';
	curr=curr+1;
	$('#addstudents').append(str);
}

function selectedCurfewSlot(event){
	curfew_slot=event.target.id;

	$('#curfewslot').text(curfew_slot);
	//$('#hidden_requesttype').text(curfew_slot);
	document.getElementById("hidden_requesttype").value=curfew_slot;
}
function selectedInTime(event){
	in_time=event.target.id;
	
	document.getElementById("hidden_intime").value=in_time;
	if(in_time==="in1"){
		in_time="Non Curfew Time";
	}
	else if(in_time==="in2"){
		in_time="10pm-12am";
	}
	else if(in_time==="in3"){
		in_time="2am-3am";
	}
	else if(in_time==="in4"){
		in_time="3am-6am";
	}
	$('#intime').text(in_time);
}

function selectedOutTime(event){
	out_time=event.target.id;
	document.getElementById("hidden_outtime").value=out_time;
	if(out_time==="out1"){
		out_time="Non Curfew Time";
	}
	else if(out_time==="out2"){
		out_time="10pm-12am";
	}
	else if(out_time==="out3"){
		out_time="2am-3am";
	}
	else if(out_time==="out4"){
		out_time="3am-6am";
	}

	$('#outtime').text(out_time);
}

function selectedApprover(event){
	approver=event.target.id;
	$('#approver').text(approver);
	document.getElementById("hidden_approver").value=approver;
}
 function fileSelected1() {
        var file = document.getElementById('file_upload1').files[0];
        if (file) {
          var fileSize = 0;
          if (file.size > 1024 * 1024)
            fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
          else
            fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

          document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
          document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
          document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
        }
      }
function fileSelected2() {
        var file = document.getElementById('file_upload2').files[0];
        if (file) {
          var fileSize = 0;
          if (file.size > 1024 * 1024)
            fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
          else
            fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

          document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
          document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
          document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
        }
      }
