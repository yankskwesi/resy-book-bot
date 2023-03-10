from flask import Blueprint, Response, request
from app import account_handler
from app.forms.resy_form import ResyTokenForm
from app.forms.user_account_forms import RegistrationForm
import json

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/register', methods=['POST'])
def register():
	reg_form = RegistrationForm()
	new_user = {
		"email": reg_form.email.data,
		"password": reg_form.password.data,
		"first_name": reg_form.first_name.data,
		"phone_number": reg_form.phone_number.data
	}
	registered_user = account_handler.create_new_user_account(new_user)
	if registered_user is None:
		return Response("User already exists", 400)
	return Response(response=json.dumps({"email": registered_user.email, "name": registered_user.display_name}), status=201)


@user_bp.route('/authorize-resy', methods=['POST'])
def authorize_resy():
	resy_form = ResyTokenForm()
	resy_user_creds = {
		"email": resy_form.email.data,
		"resy_token": resy_form.resy_token.data
	}
	user_id = account_handler.get_user_id(resy_user_creds['email'])
	account_handler.save_resy_token(user_id, resy_user_creds['resy_token'])
	return Response(status=201)


@user_bp.route('/delete-resy-token', methods=['POST'])
def delete_resy_token():
	email = request.args.get('email')
	user_id = account_handler.get_user_id(email)
	account_handler.remove_resy_token(user_id)
	return Response(status=200)