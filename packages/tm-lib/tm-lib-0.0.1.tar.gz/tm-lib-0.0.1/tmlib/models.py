from mongoengine import Document, EmbeddedDocument, fields, connect
from tmlib.settings import Settings


class Checkin(EmbeddedDocument):
    symbol = fields.StringField()
    broker = fields.StringField()
    last_checkin = fields.DateTimeField()


class Registration(EmbeddedDocument):
    account_number = fields.IntField()
    broker = fields.StringField()
    rego_key = fields.StringField()
    checkins = fields.EmbeddedDocumentListField(Checkin)


class License(EmbeddedDocument):
    minion_name = fields.StringField()
    wp_membership_id = fields.IntField()
    minion_license = fields.StringField()
    support_expires = fields.DateTimeField()
    account_registrations = fields.EmbeddedDocumentListField(Registration)


class Customer(Document):
    login = fields.EmailField()
    given_name = fields.StringField()
    surname = fields.StringField()
    licenses = fields.EmbeddedDocumentListField(License)

    meta = {
        'collection': 'customers',
        'indexes':
            [{
                'fields': ['login'],
                'unique': True
            }]
    }

    def __str__(self):
        return "Customer <%s>" % self.login

    def get_account_registration(self, *, minion_name: str, account_number: int) -> Registration:
        """
        Get account registration by minion name and account_number
        :param minion_name:
        :param account_number:
        :return: Optional[Registration]
        """
        try:
            license: License = next(
                l for l in self.licenses if l.minion_name == minion_name
            )
            account_registration: Registration = next(
                ac for ac in license.account_registrations if ac.account_number == account_number
            )
            return account_registration
        except (StopIteration, AttributeError) as err:
            raise Customer.DoesNotExist(str(err))


connect('trading_minions', host=Settings.MONGO_URI)
