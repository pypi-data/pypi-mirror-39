import urllib3
from logging import getLogger

from .extended import all_extended_properties
from exchangelib import Account, ServiceAccount, Configuration, DELEGATE, Message
from exchangelib.folders import Messages, Folder, DeletedItems
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

__author__ = "Jason Scurtu"
__copyright__ = "Copyright 2018, Xarbit - Jason Scurtu"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Jason Scurtu"
__email__ = "scurtu@mail.de"
__status__ = "Development"


LOG = getLogger(__name__)


class Exchange(object):
    """Provides Exchange integration for Flask."""

    def __init__(self, account=None, credentials=None, app=None, ssl=False):
        """
        enable the fault tolerance, create credentials as a service account
        Fault - tolerance means that requests to the server do an exponential backoff and sleep for up to a certain
        threshold before giving up, if the server is unavailable or responding with error messages.
        This prevents automated scripts from overwhelming a failing or overloaded server, and hides
        intermittent service outages that often happen in large Exchange installations.
        """
        self._account = account or Account
        self._service_account = credentials or ServiceAccount
        self._config = Configuration
        self._verify_ssl = ssl

        self.app = None

        if app:
            self.init_app(app)

    @property
    def account(self) -> Account:
        return self._account

    @property
    def get_folders(self) -> list:

        return [
            folder
            for folder in self._account.root.walk()
            if isinstance(folder, Messages) or isinstance(folder, DeletedItems)
        ]

    def get_folder_by_name(self, name) -> Folder:
        root = self._account.root / "Top of Information Store"
        folder = [f for f in root.walk() if f.name == name]
        if folder:
            return folder[0]

    def init_app(self, app):
        """
        Initialize ExchangeLib with a Flask application instance.
        """
        self.app = app

        # make Account accessible with current_app
        self.app.exchange = self

        # Enable/Disable SSL verification
        if not self._verify_ssl:
            BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # get configuration
        self._load_config()
        # setup exchange
        self._init_exchange()
        # reload exchange
        self.reload()

        LOG.info("Flask Exchange App Initialized")

    @staticmethod
    def _register_property_extensions():
        # Pre-register extended properties that are not standard part of EWS/ExchangeLib
        for prop in all_extended_properties:
            Message.register(**prop)

    def _setup_credentials(self):
        """Setup credentials from Flask Config and create a service account"""
        credentials = {}
        username = self.app.config.get("EXCHANGE_ACCOUNT")
        if username:
            credentials["username"] = username
        password = self.app.config.get("EXCHANGE_PASSWORD")
        if password:
            credentials["password"] = password

        self._service_account = self._service_account(**credentials)

    def _setup_configuration(self):
        """Setup Exchange Configuration from Flask Config"""

        exchange_url = self.app.config.get("EXCHANGE_URL")

        configuration = {
            "server": exchange_url,
            "credentials": self._service_account
        }

        self._config = self._config(**configuration)

        ssl = self.app.config.get("EXCHANGE_VERIFY_SSL")
        if ssl:
            self._verify_ssl = ssl

    def _setup_account(self):
        """ Initialize the Account """

        account = {
            "primary_smtp_address": self.app.config.get("EXCHANGE_ACCOUNT"),
            "config": self._config,
            "autodiscover": False,
            "access_type": DELEGATE
        }

        # account['credentials'] = auth

        self._account = self._account(**account)

    def _init_exchange(self):
        self._setup_account()
        self._register_property_extensions()

    def _load_config(self):

        """Load the configuration from the Flask configuration."""
        self._setup_credentials()
        self._setup_configuration()

    def reload(self):

        # fetch the cached values and create the account without autodiscover:
        config = Configuration(
            service_endpoint=self._account.protocol.service_endpoint,
            credentials=self._service_account,
            auth_type=self._account.protocol.auth_type,
        )
        account = Account(
            primary_smtp_address=self._account.primary_smtp_address,
            config=config,
            autodiscover=False,
            access_type=DELEGATE,
        )
        return account

