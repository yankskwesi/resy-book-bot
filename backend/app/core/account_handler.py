from typing import Dict
import logging
from firebase_admin import App as FirebaseAdminApp
from firebase_admin.auth import Client as FirebaseAuthClient, UserRecord
from firebase_admin.auth import EmailAlreadyExistsError
from google.cloud.firestore import Client as FirestoreClient


class AccountHandler:
	account_handler_logger = logging.getLogger(__name__)
	def __init__(self, firebase_admin: FirebaseAdminApp, firestore_client: FirestoreClient):
		self.firebase_auth = FirebaseAuthClient(firebase_admin)
		self.firestore_client = firestore_client

	def create_new_user_account(self, user_registration: Dict):
		try:
			firebase_user = self.firebase_auth.create_user(
				display_name=user_registration["first_name"],
				email=user_registration["email"],
				password=user_registration["password"],
				phone_number=user_registration["phone_number"]
			)
			return firebase_user
		except EmailAlreadyExistsError as user_exists:
			self.account_handler_logger.error(f"{user_exists}:{user_registration['email']}")
			return None


	def get_user_id(self, email):
		firebase_user: UserRecord = self.firebase_auth.get_user_by_email(email)
		if firebase_user.uid:
			return firebase_user.uid
		return None

	def save_resy_token(self, user_id, user_token):
		self.firestore_client.collection("resy_tokens").document(user_id).create({"_token": user_token})
		return

	def remove_resy_token(self, user_id):
		self.firestore_client.collection("resy_tokens").document(user_id).delete()
		return

	def get_resy_token(self, user_id):
		resy_token = self.firestore_client.collection(user_id).document("_token").get()
		if resy_token.exists:
			token = resy_token.to_dict()
			return token["_token"]
		return None
