from flask import Flask, Response, request, render_template, url_for, redirect, g
import requests
from datetime import datetime
import json
from contacts_resource import ContactsResource
from flask_cors import CORS
from response_service import Paginate
from smarty import Smarty
import uuid
from flask_jwt_extended import JWTManager, get_jwt, verify_jwt_in_request, jwt_required

# Create the Flask application object.
app = Flask(__name__)
app.secret_key = 'it-is-hard-to-guess'
app.url_map.strict_slashes = False

CORS(app)
jwt = JWTManager(app)


def check_user_login():    
    print(request.headers)
    verify_jwt_in_request()
    g.user_id = get_jwt()['sub']
    print(g.user_id)

@app.route('/')
def index():
    return '6156-Contact-microservice.'



@app.route("/contacts", methods=["GET"])
def get_all_contacts():
    result = ContactsResource.fetch_all_contacts()
    response = {}
    Paginate.paginate(request.path, result, request.args, response)

    if response['data']:
        rsp = Response(json.dumps(response, default=str), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/contacts/users/", methods=["GET", "PUT", "DELETE"])
def get_contact_by_userid():
    verify_jwt_in_request()
    g.user_id = get_jwt()['sub']
    userid = g.user_id
    print(request.headers)
    if request.method == 'GET':
        result = ContactsResource.get_by_userid(userid)
        if result:
            rsp = Response(json.dumps(result, default=str), status=200, content_type="application.json")
        else:
            ContactsResource.create_contacts(userid, ["update", "update", "update", "update", "update"])
            result = ContactsResource.get_by_userid(userid)
            rsp = Response(json.dumps(result, default=str), status=200, content_type="application.json")

        return rsp

    if request.method == 'PUT':
        updated_info = process_form(request.form)
        ContactsResource.update_contact(userid, updated_info)

        return {"msg": "Information updated"}, 200

    if request.method == 'DELETE':
        ContactsResource.delete_contact(userid)
        return {"msg": "Information deleted"}, 200


@app.route('/contacts/create', methods=['GET', "POST"])
def add_contact():
    if request.method == "GET":
        URL = "https://us-autocomplete-pro.api.smartystreets.com/lookup"
        
        auth_id = "4070fba4-036c-0f2d-aa09-b9ba9cceb8eb"
        token = "XdzuVVnBsOovBpJSZej8"
        search = request.form.get('address')
        print('Smarty Search:', search)
        if search:
            # defining a params dict for the parameters to be sent to the API
            PARAMS = {
                'search':search,
                'auth-id':auth_id,
                'auth-token':token
            }
            
            # sending get request and saving the response as response object
            r = requests.get(url = URL, params = PARAMS)
            
            # extracting data in json format
            data = r.json()
            # print('Smarty Result: ', data)
            return render_template('contacts.html', result=data)

    if request.method == 'POST':
        lastname = request.form.get('last_name')
        firstname = request.form.get('first_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        contact_info = [lastname, firstname, address, phone, email]
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

