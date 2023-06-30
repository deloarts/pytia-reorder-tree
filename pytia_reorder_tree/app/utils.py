"""
    Submodule for language related functions.
"""

from typing import Literal

from app.exit import Exit
from app.log import log
from pycatia.product_structure_interfaces.product import Product
from resources import resource


def get_ui_language(product: Product) -> Literal["en", "de"] | None:
    """Returns the language of the CATIA UI.

    Returns:
        _type_: Literal "de" or "en".
    """
    parameters = product.parameters
    try:
        parameters.get_item(resource.keywords.en.partnumber)
        log.logger.info("UI language is set to 'English'.")
        return "en"
    except:
        pass

    try:
        parameters.get_item(resource.keywords.de.partnumber)
        log.logger.info("UI language is set to 'German'.")
        return "de"
    except:
        pass

    log.logger.error("The UI language is not supported.")
    Exit().keep_open()
