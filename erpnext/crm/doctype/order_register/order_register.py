# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OrderRegister(Document):
	pass

#Getting contact details after selecting contact name
@frappe.whitelist()
def get_contact_details(contact):
	contact = frappe.get_doc("Contact", contact)
	out = {
		"contact_person": contact.get("name") or " ",
		"contact_display": " ".join(filter(None,
			[contact.get("first_name"), contact.get("last_name")])) or " ",
		"contact_email": contact.get("email_id") or " ",
		"contact_mobile": contact.get("mobile_no")or " ",
		"contact_phone": contact.get("phone") or " ",
		"contact_designation": contact.get("designation") or " ",
		"contact_department": contact.get("department") or " ",
		"contact_personal_email" : contact.get("personal_email") or " "
	}
	return out


