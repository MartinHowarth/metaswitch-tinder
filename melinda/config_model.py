"""Definition of the app configuration model that handles parsing and validation."""
from schematics.models import Model
from schematics.types import EmailType, ListType, StringType, URLType


class Melinda(Model):
    """Schematics model to parse and validate the app config."""

    app_name = StringType(required=True)
    css_cdn = URLType(
        default="https://maxcdn.bootstrapcdn.com/bootswatch/4.0.0/"
        "minty/bootstrap.min.css"
    )
    default_user_image = URLType(required=True)
    ducks = ListType(URLType(required=True))
    sad_ducks = ListType(URLType(required=True))
    serious_ducks = ListType(URLType(required=True))
    report_email_address = EmailType(required=True)
