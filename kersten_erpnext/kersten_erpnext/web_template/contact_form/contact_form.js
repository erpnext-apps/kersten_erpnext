// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {
	if(frappe.utils.get_url_arg('subject')) {
	  $('[name="subject"]').val(frappe.utils.get_url_arg('subject'));
	}

	$('.btn-send').off("click").on("click", function() {
		var email = $('[name="email"]').val();
		var message = $('[name="message"]').val();
		var first_name = $('[name="first_name"]').val();
		var last_name = $('[name="last_name"]').val();
		var organisation_name = $('[name="organisation_name"]').val();
		var mobile_no = $('[name="mobile_no"]').val();
		var postal_code = $('[name="postal_code"]').val();

		if(!(email && message)) {
			frappe.msgprint('{{ _("Please enter both your email and message so that we can get back to you. Thanks!") }}');
			return false;
		}

		if(!validate_email(email)) {
			frappe.msgprint('{{ _("You seem to have written your name instead of your email. Please enter a valid email address so that we can get back.") }}');
			$('[name="email"]').focus();
			return false;
		}

		$("#contact-alert").toggle(false);
		frappe.call({
			method:"kersten_erpnext.kersten_erpnext.web_template.contact_form.contact_form.send_message",
			args: {
				subject: $('[name="subject"]').val(),
				sender: email,
				message: message,
				first_name:first_name,
				last_name:last_name,
				mobile_no:mobile_no,
				organisation_name:organisation_name,
				postal_code : postal_code
			},
			callback: function(r) {
				if (!r.exc) {
					frappe.msgprint('{{ _("Thank you for your message") }}');
				}
				$(':input').val('');
			}
		},this)
		return false;
	});

});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
