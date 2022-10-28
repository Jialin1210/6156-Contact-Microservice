from flask import Flask, Response, request, render_template, url_for, redirect
from datetime import datetime
import json
from contacts_resource import ContactsResource
from flask_cors import CORS
import uuid

# Create the Flask application object.
app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return '6156-Contact-microservice.'

@app.route("/contacts/", methods=["GET"])
def get_all_contacts():
    result = ContactsResource.fetch_all_contacts()

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/contacts/users/<userid>/", methods=["GET", "PUT", "DELETE"])
def get_contact_by_userid(userid):

    if request.method == 'GET':
        result = ContactsResource.get_by_userid(userid)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp

    if request.method == 'PUT':
        updated_info = process_form(request.form)
        ContactsResource.update_contact(userid, updated_info)
        # print('we are here')
        return redirect(url_for('get_all_contacts', request_id=userid))

    if request.method == 'DELETE':
        ContactsResource.delete_contact(userid)
        return redirect(url_for('get_all_contacts'))

@app.route('/contacts/create/', methods=['GET', "POST"])
def add_contact():
    if request.method == 'POST':
        contact_info = process_form(request.form)
        ContactsResource.create_contacts(uuid.uuid4(), contact_info)
        return redirect(url_for('get_all_contacts'))
    return render_template('contacts.html')

def process_form(form):
    lastname = form.get('last_name')
    firstname = form.get('first_name')
    address = form.get('address')
    phone = form.get('phone')
    email = form.get('email')
    info = [lastname, firstname, address, phone, email]
    return info


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)

