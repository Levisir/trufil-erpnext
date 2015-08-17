from __future__ import unicode_literals
import frappe
from frappe.utils import add_days, cint, cstr, date_diff, rounded, flt, getdate, nowdate, \
	get_first_day, get_last_day,money_in_words, now, nowtime
from frappe import _
from frappe.model.db_query import DatabaseQuery



# Validation customer code on on_update of customer form
def validate_customer_code(doc,method):
	if frappe.db.sql("""select name from `tabCustomer` where name!='%s' and customer_code='%s'"""%(doc.name,doc.customer_code)):
		frappe.msgprint("Customer code '%s' is already assigned for another customer"%doc.customer_code,raise_exception=1)


# Generation of contact code while saving contact form
def generate_contact_code(doc,method):
	if doc.customer_code and doc.user_input:
		doc.contact_code = doc.customer_code + '-' + doc.user_input
	if doc.contact_code:
		if frappe.db.sql("""select name from `tabContact` where name!='%s' and customer='%s' and user_input='%s'"""%(doc.name,doc.customer,doc.user_input)):
			frappe.msgprint("Same user input '%s' is already assigned against same customer in another contact"%doc.user_input,raise_exception=1)


# Generation of address code while saving the new address
def generate_address_code(doc,method):
	if doc.customer_code and doc.user_input:
		doc.address_code = doc.customer_code + '-' + doc.user_input
	if doc.address_code:
		if frappe.db.sql("""select name from `tabAddress` where name!='%s' and customer='%s' and user_input='%s'"""%(doc.name,doc.customer,doc.user_input)):
			frappe.msgprint("Same user input '%s' is already assigned against same customer in another address"%doc.user_input,raise_exception=1)

