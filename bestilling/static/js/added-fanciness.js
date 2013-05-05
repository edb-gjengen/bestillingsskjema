// Only display services that are chosen
$(document).ready(function(){
	$('.service').hide();
	$('.service-nav-element').hide();

	$('#service-picker a.btn').click(function(clickEvent){
		var rel=this.rel;

		// Avoid jumping to the top of the page
		clickEvent.preventDefault();

		if($(this).hasClass('active')){
			// Remove the active class on the button
			$(this).removeClass('active');

			// Set the value of a hidden input field to 0
			$('#'+rel+'pls').val(0);

			// Hide no longer needed sections
			$('#'+rel+'form').hide(400);
			$('#'+rel+'-nav-element').hide(400);
		} else {
			// Make sure the button looks pressed
			$(this).addClass('active');

			// Set the value of a hidden input field to 1
			$('#'+rel+'pls').val(1);

			// Show needed sections
			$('#'+rel+'form').show(400);
			$('#'+rel+'-nav-element').show(400);
		}
	});
});

