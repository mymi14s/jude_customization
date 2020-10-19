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
