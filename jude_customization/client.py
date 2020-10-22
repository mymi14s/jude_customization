from datetime import datetime
import frappe

def create_note_from_meeting_notice_board(doc, handler=None):
# create Hse Meeting notice board
    print("CREATING NOTE")
    newdoc = frappe.new_doc("Note")
    newdoc.title = doc.name
    newdoc.public = True
    newdoc.notify_on_login = True
    newdoc.content = "Date: <b>{0}</b><br>Time: <b>{1}</b>\
                <br>Venue: <b>{2}</b><br>Link : <b><a style='color:red;' \
                href='http://192.168.25.3/desk#Form/HSE%20Meeting%20Notice%20Board/{3}'> Click here to visit </a></b>\
                ".format(datetime.strptime(doc.meeting_date, '%Y-%m-%d').strftime('%d-%m-%Y'), datetime.strptime(doc.meeting_time, '%H:%M:%S').strftime('%I:%M%p').lower(), doc.meeting_venue, doc.name)
    newdoc.insert()
    print("dONE CREATING NOTE")


def send_leave_application_email(doc, handler=None):
    # send email based on workflow status
    email_args = {
				"recipients": [],
				"message": "",
				"subject": '',
				"reference_doctype": doc.doctype,
				"reference_name": doc.name
				}
    if doc.workflow_state == "Pending HOD Approval":
        email_args["recipients"] = [doc.leave_approver]
        email_args["message"] = "<b>Leave Application</b><br>Employee: {0}<br>Approve/Reject:  <a href='http://192.168.25.3/desk#Form/Leave%20Application/{1}'>http://192.168.25.3/desk#Form/Leave%20Application/{1}</a>".format(doc.employee_name, doc.name)
        email_args['subject'] = "Leave Application for {0}".format(doc.employee_name)
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    elif doc.workflow_state == "Pending HR Approval" and doc.status == "Open":
        company = frappe.get_doc('Company', frappe.get_doc('Leave Application', doc.name).company)
        #company_abbr = f"{company.name} - {company.abbr}"
        hrm = frappe.get_doc("Department", "Administration/Human Resources/Corporate Services - AFIS").leave_approvers[0].approver
        email_args["recipients"] = [hrm]
        email_args["message"] = "<b>Leave Application</b><br>Employee: {0}<br>Approve/Reject:  <a href='http://192.168.25.3/desk#Form/Leave%20Application/{1}'>http://192.168.25.3/desk#Form/Leave%20Application/{1}</a>".format(doc.employee_name, doc.name)
        email_args['subject'] = "Leave Application for {0}: HR Action".format(doc.employee_name)
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    elif doc.workflow_state == "HOD Rejected" or doc.workflow_state == "HR Rejected":
        email_args["recipients"] = [frappe.get_doc("Employee", doc.employee).user_id]
        email_args["message"] = "<b>Leave Application rejected</b><br>Link: <a href='http://192.168.25.3/desk#Form/Leave%20Application/{0}'>http://192.168.25.3/desk#Form/Leave%20Application/{0}</a>".format(doc.name)
        email_args['subject'] = "Leave Application Rejected"
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    elif doc.workflow_state == "Approved by HR":
        email_args["recipients"] = [frappe.get_doc("Employee", doc.employee).user_id]
        email_args["message"] = "<b>Leave Application Approved</b><br>Link: <a href='http://192.168.25.3/desk#Form/Leave%20Application/{0}'>http://192.168.25.3/desk#Form/Leave%20Application/{0}</a>".format(doc.name)
        email_args['subject'] = "Leave Application Approved"
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
