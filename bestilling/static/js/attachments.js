$(function () {
    $('#fileupload').fileupload({
    	formData: {
    		csrfmiddlewaretoken: $("#fileupload-form input[name=csrfmiddlewaretoken]").val(),
    		content_type: $("#fileupload-form input[name=content_type]").val(),
    		object_id: $("#fileupload-form input[name=object_id]").val()
    	},
        dataType: 'json',
        done: function (e, data) {
            $('.attachments ul').append('<li><a href="/media/' + data.result.uploaded_file + '">'+
            	data.files[0].name + '</a> (ny)</li>');

            /* Reset progress */
            setTimeout(function(){
            	$('#progress .bar').css('width', '0%');
            }, 1000);
        },
        progressall: function (e, data) {
	        var progress = parseInt(data.loaded / data.total * 100, 10);
	        $('#progress .bar').css('width', progress + '%');
	    },       
        fail: function (e, data) {
        	var error = "";
        	if(data.jqXHR.responseJSON.hasOwnProperty('uploaded_file') ) {
        		error = data.jqXHR.responseJSON.uploaded_file[0];
        	} else {
        		error = data.jqXHR.responseJSON;
        	}
            $('#progress .bar').css('background-color', '#f2dede').html('<strong>Feil</strong>: '+ error);
        },
        start: function() {
        	$('#progress .bar').html('&nbsp;').css('background-color', '#dff0d8');
        }
    });
});