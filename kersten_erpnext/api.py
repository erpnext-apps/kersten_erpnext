import frappe
import frappe.defaults
from frappe import _, bold, throw
from frappe.contacts.doctype.address.address import get_address_display
from frappe.contacts.doctype.contact.contact import get_contact_name
from frappe.utils import cint, cstr, flt, get_fullname
from frappe.utils.nestedset import get_root_of
from frappe.core.doctype.file.utils import extract_images_from_html

from erpnext.accounts.utils import get_account_name
from erpnext.e_commerce.doctype.e_commerce_settings.e_commerce_settings import (
	get_shopping_cart_settings,
)
from erpnext.utilities.product import get_web_item_qty_in_stock

def add_comment(reference_doctype: str, reference_name: str, content: str, comment_email: str, comment_by: str):
	reference_doc = frappe.get_doc(reference_doctype, reference_name)

	comment = frappe.new_doc("Comment")
	comment.update(
		{
			"comment_type": "Comment",
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"comment_email": comment_email,
			"comment_by": comment_by,
			"content": extract_images_from_html(reference_doc, content, is_private=True),
		}
	)
	comment.insert(ignore_permissions=True)

	if frappe.get_cached_value("User", frappe.session.user, "follow_commented_documents"):
		follow_document(comment.reference_doctype, comment.reference_name, frappe.session.user)

	return comment

@frappe.whitelist(allow_guest=True)
def create_lead_for_item_inquiry(lead, subject, message):
	doc = frappe.parse_json(lead)
	
	sender = doc.email_id
	phone = doc.phone
	company_name = doc.company_name
	fullname = doc.lead_name
	message = """
		<div>
			<h5>{subject}</h5>
			<p>{message}</p>
		</div>
		""".format(
				subject=subject, message=message
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
		doc.contact_mobile = phone
		doc.contact_email = sender
		doc.save(ignore_permissions = True)
		
		add_comment("Opportunity" , doc.name , content=message , comment_email = sender, comment_by = None)

	contact_but_no_customer = frappe.db.sql(f""" Select co.name  From `tabContact` as co
						  					Left join `tabContact Email` as ce ON ce.parent = co.name
						  					Where ce.email_id = '{sender}'
											""",as_dict = 1)
	if not contact_but_no_customer:
		customer = frappe.new_doc("Customer")
		customer.customer_name=company_name
		customer.customer_type="Company"
		customer.customer_group="Account Sales"
		customer.territory="All Territories"
		customer.save(ignore_permissions = True)

		opportunity = frappe.new_doc("Opportunity")
		opportunity.opportunity_from = "Customer"
		opportunity.party_name = customer.name
		opportunity.contact_email = sender
		opportunity.contact_mobile = phone
		opportunity.source = ""
		opportunity.save(ignore_permissions = True)
		frappe.db.set_value("Customer" , customer.name , 'opportunity_name' , opportunity.name , update_modified=False)
		add_comment(reference_doctype = "Opportunity", reference_name=opportunity.name, content = message, comment_email=sender, comment_by = frappe.session.user)

		contact = frappe.new_doc("Contact")
		contact.first_name = fullname
		contact.email_id = sender
		contact.mobile_no = phone
		contact.append("email_ids",{
			"email_id":sender,
			"is_primary":1
		})
		contact.append("links",{
			"link_doctype":"Customer",
			"link_name":customer.name
		})
		contact.append("phone_nos",{
			"phone":phone,
			"is_primary_phone":1
		})
		contact.save(ignore_permissions=True)

    frappe.msgprint("Thank you for reaching out to us. We will get back to you at the earliest.")
