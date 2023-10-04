# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from contextlib import suppress

import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import validate_email_address
from frappe.desk.form.utils import add_comment
from erpnext.crm.doctype.lead.lead import make_opportunity
from frappe.model.mapper import get_mapped_doc


sitemap = 1


def get_context(context):
	doc = frappe.get_doc("Contact Us Settings", "Contact Us Settings")

	if doc.query_options:
		query_options = [opt.strip() for opt in doc.query_options.replace(",", "\n").split("\n") if opt]
	else:
		query_options = ["Sales", "Support", "General"]

	out = {"query_options": query_options, "parents": [{"name": _("Home"), "route": "/"}]}
	out.update(doc.as_dict())

	return out


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=1000, seconds=60 * 60)
def send_message(sender, message, first_name = None, last_name = None, mobile_no = None, postal_code=None, organisation_name = None, subject="Website Query" ):
	
	sender = validate_email_address(sender, throw=True)

	with suppress(frappe.OutgoingEmailError):
		if forward_to_email := frappe.db.get_single_value("Contact Us Settings", "forward_to_email"):
			frappe.sendmail(recipients=forward_to_email, reply_to=sender, content=message, subject=subject)

		frappe.sendmail(
			recipients=sender,
			content=f"<div style='white-space: pre-wrap'>Thank you for reaching out to us. We will get back to you at the earliest.\n\n\nYour query:\n\n{message}</div>",
			subject="We've received your query!",
		)

	contact_data = frappe.db.sql(f""" Select co.name , dl.link_name From `tabContact` as co
						  					Left join `tabContact Email` as ce ON ce.parent = co.name
						  					left join `tabDynamic Link` as dl ON dl.parent = co.name
						  					Where ce.email_id = '{sender}' and dl.link_doctype = "Customer" 
											""",as_dict = 1)
	if contact_data:
		doc = frappe.new_doc("Opportunity")
		doc.opportunity_from = "Customer"
		doc.party_name = contact_data[0].link_name
		doc.contact_mobile = mobile_no
		doc.contact_email = sender
		doc.save()
		add_comment("Opportunity" , doc.name , content=message , comment_email = sender, comment_by = None) 
	
	contact_but_no_customer = frappe.db.sql(f""" Select co.name  From `tabContact` as co
						  					Left join `tabContact Email` as ce ON ce.parent = co.name
						  					Where ce.email_id = '{sender}'
											""",as_dict = 1)
	
	if not contact_but_no_customer:
		doc = frappe.new_doc("Lead")
		doc.first_name = first_name
		doc.last_name = last_name
		doc.email_id = sender
		doc.mobile_no = mobile_no
		doc.company_name = organisation_name
		doc.save()
		add_comment("Lead" , doc.name , content=message , comment_email = sender, comment_by = None) 
		
		make_opportunity(doc.name)
		make_customer(doc.name)


def make_opportunity(source_name, target_doc=None):
	def set_missing_values(source, target):
		_set_missing_values(source, target)

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Opportunity",
				"field_map": {
					"campaign_name": "campaign",
					"doctype": "opportunity_from",
					"name": "party_name",
					"lead_name": "contact_display",
					"company_name": "customer_name",
					"email_id": "contact_email",
					"mobile_no": "contact_mobile",
					"lead_owner": "opportunity_owner",
					"notes": "notes",
				},
			}
		},
		target_doc,
		set_missing_values,
	)

	target_doc.save()

def _set_missing_values(source, target):
	address = frappe.get_all(
		"Dynamic Link",
		{
			"link_doctype": source.doctype,
			"link_name": source.name,
			"parenttype": "Address",
		},
		["parent"],
		limit=1,
	)

	contact = frappe.get_all(
		"Dynamic Link",
		{
			"link_doctype": source.doctype,
			"link_name": source.name,
			"parenttype": "Contact",
		},
		["parent"],
		limit=1,
	)

	if address:
		target.customer_address = address[0].parent

	if contact:
		target.contact_person = contact[0].parent

def make_customer(source_name, target_doc=None, ignore_permissions=True):
	def set_missing_values(source, target):
		if source.company_name:
			target.customer_type = "Company"
			target.customer_name = source.company_name
		else:
			target.customer_type = "Individual"
			target.customer_name = source.lead_name

		target.customer_group = frappe.db.get_default("Customer Group")

	doclist = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Customer",
				"field_map": {
					"name": "lead_name",
					"company_name": "customer_name",
					"contact_no": "phone_1",
					"fax": "fax_1",
				},
				"field_no_map": ["disabled"],
			}
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)
	doclist.save()