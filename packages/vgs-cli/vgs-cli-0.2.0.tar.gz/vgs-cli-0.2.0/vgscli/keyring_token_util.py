import keyring
import jwt
import sys
from vgscli.utils import expired, eprint


class KeyringTokenUtil:
    SERVICE_NAME = 'vgs-cli'
    ACCESS_TOKEN_KEY = 'access_token'
    REFRESH_TOKEN_KEY = 'refresh_token'

    def validate_access_token(self):
        if self.get_access_token():
            token_json = jwt.decode(self.get_access_token().password, verify=False)
            return not expired(token_json['exp'])
        else:
            self.require_login()

    def validate_refresh_token(self):
        if self.get_refresh_token():
            token_json = jwt.decode(self.get_refresh_token().password, verify=False)
            if expired(token_json['exp']):
                self.require_login()
        else:
            self.require_login()

    def process_token_response(self, response):
        self.put_access_token(response[self.ACCESS_TOKEN_KEY])
        self.put_refresh_token(response[self.REFRESH_TOKEN_KEY])

    def put_access_token(self, token):
        keyring.set_password(self.SERVICE_NAME, self.ACCESS_TOKEN_KEY, token)

    def get_access_token(self):
        return keyring.get_credential(self.SERVICE_NAME, self.ACCESS_TOKEN_KEY)

    def delete_access_token(self):
        try:
            keyring.delete_password(self.SERVICE_NAME, self.ACCESS_TOKEN_KEY)
        except keyring.errors.PasswordDeleteError:
            eprint("You have already logged out")
            sys.exit(1)

    def put_refresh_token(self, token):
        keyring.set_password(self.SERVICE_NAME, self.REFRESH_TOKEN_KEY, token)

    def get_refresh_token(self):
        return keyring.get_credential(self.SERVICE_NAME, self.REFRESH_TOKEN_KEY)

    def delete_refresh_token(self):
        try:
            keyring.delete_password(self.SERVICE_NAME, self.REFRESH_TOKEN_KEY)
        except keyring.errors.PasswordDeleteError:
            eprint("You have already logged out")
            sys.exit(1)

    @staticmethod
    def require_login():
        eprint("You need to run `vgs authenticate` because your session has been expired")
        sys.exit(1)
