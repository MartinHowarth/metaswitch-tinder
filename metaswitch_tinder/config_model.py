from schematics.models import Model
from schematics.types import ModelType, URLType, ListType, StringType


class MetaswitchTinder(Model):
    css_cdn = URLType(default='https://maxcdn.bootstrapcdn.com/bootswatch/4.0.0/minty/bootstrap.min.css')
    ducks = ListType(URLType(required=True))
    DATABASE_URL=StringType(required=True)
