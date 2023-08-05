from oauth2_client.credentials_manager import ServiceInformation, \
    CredentialManager


class Authentication:
    TOKEN_URL = 'https://api.acriticismlab.org/oauth/token/'
    CLIENT_ID = 'databaseAuthentication'
    CLIENT_SECRET = ''
    ENCODING = 'utf-8'
    SCOPES = []

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.do_authorization()

    def do_authorization(self):
        service_information = ServiceInformation(
            'https://api.acriticismlab.org/oauth/authorize',
            'https://api.acriticismlab.org/oauth/token',
            self.CLIENT_ID,
            self.CLIENT_SECRET,
            self.SCOPES
        )

        manager = CredentialManager(
            service_information
        )

        manager.init_with_user_credentials(self.username, self.password)
        self.access_token = manager._access_token
