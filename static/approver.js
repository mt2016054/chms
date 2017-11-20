var curfew_slot=null;
var approver=null;
var curr=2;
var request=null;

//reply button click
function submitReply(){
		$.ajax({
        url: '/submitReplyApprover',
        data: $('form').serialize(),
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


//approve it!!
function approve(){
	//alert('alert clicked!');
		$.ajax({
        url: '/approve',
        data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
            alert('approved!!');
            //$('#title').empty();
            //$('#title').append(request+' : Approved!!');
            $('#viewRequestModal').modal('hide');
            location.reload();
        },
        error: function(error) {
            alert('Oops!! Something went wrong..');
        }
    });
}

//reject it!!
function reject(){
		$.ajax({
        url: '/reject/'+request,
        data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
            alert('rejected..');
            $('#title').empty();
            $('#title').append(request+' : Rejected!!');
            $('#viewRequestModal').modal('hide');
        },
        error: function(error) {
            alert('Oops!! Something went wrong..');
        }
    });
}

$(window).on('shown.bs.modal', function(event) { 
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

$(window).on('hidden.bs.modal', function() { 
    //$('#viewRequestModal').modal('hide');
    //alert('hidden');
});


