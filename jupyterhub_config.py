import os

c.JupyterHub.authenticator_class = 'icladd'

c.Application.log_level = 'DEBUG'
c.LocalICLOAuthenticator.create_system_users = True
c.LocalICLOAuthenticator.tenant_id = os.environ.get('AAD_TENANT_ID')

c.LocalICLOAuthenticator.oauth_callback_url = 'http://localhost:8000/hub/oauth_callback'
c.LocalICLOAuthenticator.client_id = os.environ.get('AAD_CLIENT_ID')
c.LocalICLOAuthenticator.client_secret = os.environ.get('AAD_CLIENT_SECRET')