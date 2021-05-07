"""
Custom Authenticator to use Azure AD with JupyterHub
"""

import os
import urllib
from distutils.version import LooseVersion as V

import jwt
import msal
from jupyterhub.auth import LocalAuthenticator
from tornado.httpclient import HTTPRequest
from traitlets import Unicode, default

from oauthenticator.oauth2 import OAuthenticator, OAuthLoginHandler

# pyjwt 2.0 has changed its signature,
# but mwoauth pins to pyjwt 1.x
PYJWT_2 = V(jwt.__version__) >= V("2.0")

class ICLLoginHandler(OAuthLoginHandler):

    def authorize_redirect(self, *args, **kwargs):
        secret = self.authenticator.client_secret

        print('secret is ', self.authenticator.__dict__)

        return super().authorize_redirect(*args, client_secret=secret, **kwargs)

class ICLOAuthenticator(OAuthenticator):
    login_service = Unicode(
		os.environ.get('LOGIN_SERVICE', 'Imperial SSO'),
		config=True,
		help="""Azure AD domain name string, e.g. My College"""
	)

    tenant_id = Unicode(config=True, help="The Azure Active Directory Tenant ID")

    login_handler = ICLLoginHandler

    @default('tenant_id')
    def _tenant_id_default(self):
        return os.environ.get('AAD_TENANT_ID', '')

    username_claim = Unicode(config=True)

    @default('username_claim')
    def _username_claim_default(self):
        return 'name'

    @default("authorize_url")
    def _authorize_url_default(self):
        return 'https://login.microsoftonline.com/{0}/oauth2/authorize'.format(self.tenant_id)

    @default("token_url")
    def _token_url_default(self):
        return 'https://login.microsoftonline.com/{0}/oauth2/token'.format(self.tenant_id)



    async def authenticate(self, handler, data=None):
        authority = f'https://login.microsoftonline.com/{self.tenant_id}'

        self.aad = msal.ConfidentialClientApplication(self.client_id,
                                                 self.client_secret,
                                                 authority)

        print(self.authorize_url)

        code = handler.get_argument("code")

        response = self.aad.acquire_token_by_authorization_code(code,
                                                           scopes=[], 
                                                           redirect_uri=self.get_callback_url(handler))

        print(response)

        access_token = response['access_token']
        id_token = response['id_token']

        if PYJWT_2:
            decoded = jwt.decode(
                id_token,
                options={"verify_signature": False},
                audience=self.client_id,
            )
        else:
            # pyjwt 1.x
            decoded = jwt.decode(id_token, verify=False)

        print(decoded)

        decoded["name"] = decoded['preferred_username'].split('@')[0]
        
        userdict = {"name": decoded["name"]}
        userdict["auth_state"] = auth_state = {}
        auth_state['access_token'] = access_token
        # results in a decoded JWT for the user data
        auth_state['user'] = decoded

        return userdict


class LocalICLOAuthenticator(LocalAuthenticator, ICLOAuthenticator):
    """A version that mixes in local system user creation"""
    pass
