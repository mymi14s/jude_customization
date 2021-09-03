from datetime import datetime
import subprocess
import frappe
from frappe import _
from .utils import get_system_site_name

def create_note_from_meeting_notice_board(doc, handler=None):
# create Hse Meeting notice board
    print("CREATING NOTE")
    print(doc.minutes)
    newdoc = frappe.new_doc("Note")
    newdoc.title = doc.name
    newdoc.public = True
    newdoc.notify_on_login = True
    newdoc.notify_on_every_login = True
    newdoc.expire_notification_on = doc.meeting_date
    newdoc.content = "Date: <b>{0}</b><br>Time: <b>{1}</b>\
                <br>Venue: <b>{2}</b><br>Link : <b><a style='color:red;' \
                href='{4}/desk#Form/HSE%20Meeting%20Notice%20Board/{3}'> Click here to visit </a></b>\
                ".format(datetime.strptime(str(doc.meeting_date), '%Y-%m-%d').strftime('%d-%m-%Y'), datetime.strptime(str(doc.meeting_time), '%H:%M:%S').strftime('%I:%M%p').lower(), doc.meeting_venue, doc.name, frappe.utils.get_url())
    newdoc.insert()

    #  get users email and send mail
    # link = "<p>Attached is the minutes of the last HSE meeting.</p><br>Attachment : <b><a style='color:red;' href='http://41.73.226.7"+doc.minutes+"'> Click here to download </a></b><p></p>" if doc.minutes else "<hr>"
    download = "<a style='color:red;' href='"+frappe.utils.get_url()+doc.minutes+"'> download </a></b><p></p>" if doc.minutes else "<hr>"
    link = "<a style='color:red;' href='"+ frappe.utils.get_url() +"/desk#Form/HSE%20Meeting%20Notice%20Board/"+doc.name+"'> visit </a>"
    emails = [i[0] for i in frappe.db.sql("SELECT email FROM tabUser WHERE email LIKE '%@%';", as_list=True)]
    email_args = {
				"recipients": [],
				"message": "",
				"subject": '',
				"reference_doctype": doc.doctype,
				"reference_name": doc.name
				}
    email_args["recipients"] = emails
    # try:
    #     email_args['attachments'] = [] #doc.attachments
    # except Exception as e:
    #     pass
    meeting_msg = frappe.get_doc("Meeting Notice Setup").meeting_message
    email_args["message"] = meeting_msg.format(
            month=doc.month, year=doc.year, date=datetime.strptime(str(doc.meeting_date), '%Y-%m-%d').strftime('%d-%m-%Y'), time=datetime.strptime(str(doc.meeting_time), '%H:%M:%S').strftime('%I:%M%p').lower(),
            meeting_venue=doc.meeting_venue, download=download, docname=doc.name, here=link)
    email_args['subject'] = "HSE Meeting Notification"
    frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    # redirect
    # frappe.local.flags.redirect_location = '/desk#Form/HSE%20Meeting%20Notice%20Board/{0}'.format(doc.name)
    # raise frappe.Redirect
    print("dONE CREATING NOTE")

def delete_note_on_delete_hse_meeting(doc, event):
    try:
        note = frappe.get_doc("Note", doc.name)
        notename = note.name
        note.delete()
        # frappe.msgprint("Note: {0}, has been deleted/".format(notename))
    except Exception as e:
        pass

def cancel_not_on_cancel_meeting(doc, event):
    try:
        note = frappe.get_doc("Note", doc.name)
        note.public = False
        note.notify_on_login = False
        note.notify_on_every_login = False
        note.expire_notification_on = datetime.today().strftime('%Y-%m-%d')
        note.save()
        # frappe.msgprint("Note: {0}, has been deleted/".format(notename))
    except Exception as e:
        pass

def copy_minute_to_public(doc, event):
    if (event == "before_insert" or event == "on_update"):
        print(event)
        site_name = get_system_site_name()
        if doc.minutes:
            print(doc.minutes)
            file_name_list = str(doc.minutes).split('/')
            print(file_name_list)
            if 'private' in file_name_list:
                full_path = site_name + doc.minutes
                subprocess.call(["mv", "{0}".format(full_path), "{0}/public/files".format(site_name)])
                doc.minutes = doc.minutes.replace("/private", '')
                print(doc.minutes, "/n/n/n/n/n/n")




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
        email_args["message"] = "<b>Leave Application</b><br>Employee: {0}<br>Approve/Reject:  <a href='{2}/desk#Form/Leave%20Application/{1}'>{2}/desk#Form/Leave%20Application/{1}</a>".format(doc.employee_name, doc.name, frappe.utils.get_url())
        email_args['subject'] = "Leave Application for {0}".format(doc.employee_name)
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    elif doc.workflow_state == "Pending HR Approval" and doc.status == "Open":
        company = frappe.get_doc('Company', frappe.get_doc('Leave Application', doc.name).company)
        #company_abbr = f"{company.name} - {company.abbr}"
        hrm = frappe.get_doc("Department", "Administration/Human Resources/Corporate Services - {0}".format(company.abbr)).leave_approvers[0].approver
        email_args["recipients"] = [hrm]
        email_args["message"] = "<b>Leave Application</b><br>Employee: {0}<br>Approve/Reject:  <a href='{2}/desk#Form/Leave%20Application/{1}'>{2}/desk#Form/Leave%20Application/{1}</a>".format(doc.employee_name, doc.name, frappe.utils.get_url())
        email_args['subject'] = "Leave Application for {0}: HR Action".format(doc.employee_name)
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    elif doc.workflow_state == "HOD Rejected" or doc.workflow_state == "HR Rejected":
        email_args["recipients"] = [frappe.get_doc("Employee", doc.employee).user_id]
        email_args["message"] = "<b>Leave Application rejected</b><br>Link: <a href='{1}/desk#Form/Leave%20Application/{0}'>{1}/desk#Form/Leave%20Application/{0}</a>".format(doc.name, frappe.utils.get_url())
        email_args['subject'] = "Leave Application Rejected"
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    elif doc.workflow_state == "Approved by HR":
        email_args["recipients"] = [frappe.get_doc("Employee", doc.employee).user_id]
        email_args["message"] = "<b>Leave Application Approved</b><br>Link: <a href='{1}/desk#Form/Leave%20Application/{0}'>{1}/desk#Form/Leave%20Application/{0}</a>".format(doc.name, frappe.utils.get_url())
        email_args['subject'] = "Leave Application Approved"
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)


def compute_salary_slip_paye(doc, event):
    # frappe.msgprint(_(event))
    # for i in doc.earnings:
    #     print(i.name, i.salary_component, i.abbr)
    annual_gross_pay = doc.gross_pay * 12
    annual_pension = sum([i.amount for i in doc.earnings if i.salary_component.upper() in ["BASIC SALARY", "HOUSING ALLOWANCE", 'TRANSPORT ALLOWANCE']]) * 12
    annual_pension_08 = annual_pension * 0.08
    if((annual_gross_pay * 0.01) > 200000):consolidated_relief_allowance=(annual_gross_pay * 0.2) + (annual_gross_pay * 0.01)
    else:consolidated_relief_allowance=(annual_gross_pay * 0.2 + (200000))

    # other reliefs
    other_reliefs = sum([i.amount for i in doc.earnings if i.abbr.upper() in ["NHF", "NHIS"]]) * 12
    non_taxable_annual = consolidated_relief_allowance + annual_pension_08 + other_reliefs
    taxable_annual = annual_gross_pay - non_taxable_annual

    def tax_band_calculator(taxable):
        band_list = [
            {'amount':300000, 'per':0.07},
            {'amount':300000, 'per':0.11},
            {'amount':500000, 'per':0.15},
            {'amount':500000, 'per':0.19},
            {'amount':1600000, 'per':0.21},
            # {'amount':3200000, 'per':0.0},
        ]
        tax_to_pay = 0
        if(taxable>3200000):tax_to_pay=((taxable-3200000)*0.24) + 560000
        else:
            taxable_copy = taxable
            for i, val in enumerate(band_list):
                if((taxable_copy<val['amount']) and taxable_copy>0):
                    tax_to_pay += taxable_copy * val['per']
                    break
                elif(taxable_copy<0):
                    break
                else:
                    taxable_copy -= val['amount']
                    tax_to_pay += val['amount'] * val['per']
                    # if(taxable_copy<0):
                    #     break
        return tax_to_pay

    # get taxable_annual
    tax_to_pay_annually = tax_band_calculator(taxable_annual)
    if((tax_to_pay_annually/12)<(0.01*doc.gross_pay)):tax_to_pay_monthly=0.01*doc.gross_pay
    else:tax_to_pay_monthly = tax_to_pay_annually/12

    # create new PAYE
    # check PAYE
    checker = False
    doc_total_deductions = 0
    for i in doc.deductions:
        if i.salary_component == "PAYE Tax":
            checker = True
            i.amount = tax_to_pay_monthly
            i.default_amount = tax_to_pay_monthly
            # doc.save()
    if checker:
        doc.total_deduction = ((annual_pension/12)/12) + tax_to_pay_monthly
        doc.net_pay = doc.gross_pay - doc.total_deduction
        doc.rounded_total = round(doc.net_pay, 2)
        doc.total_in_words = frappe.utils.money_in_words(doc.rounded_total)

    # create new Salary Componetnt
    # if not checker:
    #     doc.append('deductions', {
    #         'abbr': 'PAYE',
    # 		'amount' : tax_to_pay_monthly,
    #         'salary_component' : 'PAYE Tax'
    # 	})
        # doc.save()
        # frappe.db.commit()
    # doc.save()
    # doc.reload()
    # return doc
    if not checker:
        newdoc = frappe.new_doc("Salary Detail")
        newdoc.parent = doc.name
        newdoc.parenttype = 'Salary Slip'
        newdoc.parentfield = 'deductions'
        newdoc.salary_component = 'PAYE Tax'
        newdoc.abbr = 'PAYE'
        newdoc.amount = tax_to_pay_monthly
        newdoc.insert(ignore_permissions=True)
        # print(newdoc.amount)
        doc.reload()

        # return newdoc
    # return doc
            # if(str(event)=="after_insert"):
            #     doc.reload()
            # doc.total_deduction = ((annual_pension/12)/12) + tax_to_pay_monthly
            # doc.net_pay = doc.gross_pay - doc.total_deduction
            # doc.rounded_total = round(doc.net_pay, 2)
            # doc.total_in_words = frappe.utils.money_in_words(doc.rounded_total)
            # doc.save()
    # check_paye = frappe.get_doc("Salary detail", frappe.get_doc("Salary Com"))
    # check_paye = frappe.db.sql("""SELECT parent, parentfield, parenttype, salary_component FROM `tabSalary Detail` WHERE parent='{0}' AND salary_component='{1}' AND parentfield='{2}';""".format(
    # doc.name, 'PAYE Tax', 'deductions'))
    # print(check_paye)

    # consolidated_relief_allowance = (annual_gross_pay * 0.2 + (200000)) + (annual_gross_pay * 0.01) if (annual_gross_pay * 0.01) > 200000 or (annual_gross_pay * 0.2 + (200000))
    # print("GI: {0}, AP: {1}".format(annual_gross_pay, annual_pension), "\n\n\n\n\n")
    # frappe.throw(_("GI: {0}, AP: {1}\nCRA: {2}, nta {3}\nTaxable {4}, Tax Year: {5}\nTax month {6}".format(
        # annual_gross_pay, annual_pension_08, consolidated_relief_allowance, non_taxable_annual,
        # taxable_annual, tax_to_pay_annually, tax_to_pay_monthly)))
