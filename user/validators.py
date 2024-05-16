import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Ingrese un nombre de usuario válido. Este valor puede contener solo a-z minúsculas sin acentos"
        "y letras mayúsculas de la A a la Z, números y caracteres @/./+/-/_."
    )
    flags = re.ASCII


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Ingrese un nombre de usuario válido. Este valor puede contener sólo letras,"
        "números y @/./+/-/_ caracteres."
    )
    flags = 0
