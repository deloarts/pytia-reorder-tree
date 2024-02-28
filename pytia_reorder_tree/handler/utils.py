"""
    Submodule for language related functions.
"""

from typing import Literal

from exceptions import WarningError
from pycatia.product_structure_interfaces.product import Product
from pytia.log import log
from resources import resource


def get_ui_language(product: Product) -> Literal["en", "de"] | None:
    """Returns the language of the CATIA UI.

    Returns:
        _type_: Literal "de" or "en".
    """
    parameters = product.parameters
    try:
        parameters.get_item(resource.keywords.en.partnumber)
        log.info("UI language is set to 'English'.")
        return "en"
    except:
        pass

    try:
        parameters.get_item(resource.keywords.de.partnumber)
        log.info("UI language is set to 'German'.")
        return "de"
    except:
        pass

    raise WarningError("The UI language is not supported.")
