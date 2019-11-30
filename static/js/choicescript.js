
$('#add_more').click(function() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});

$('#delete_one').click(function() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('.no_error:eq(-2)').remove();
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx)-1);
});