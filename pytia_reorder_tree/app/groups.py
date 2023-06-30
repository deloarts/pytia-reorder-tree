"""
    Groups submodule.
    Handles the documents product flagged as group identifier.
"""

from typing import Dict, List

from app.log import console, log
from app.window_handler.property_window import PropertyWindow
from const import PROP_GROUP_IDENTIFIER, PROP_NO_BOM
from exceptions import WindowNotConnectedError
from pycatia.in_interfaces.application import Application
from pycatia.product_structure_interfaces.product import Product
from pycatia.product_structure_interfaces.product_document import ProductDocument
from pytia.wrapper.properties import PyProperties
from resources import resource


class Groups:
    """Groups class."""

    def __init__(self, caa: Application, product: Product) -> None:
        """Inits the class.

        Args:
            caa (Application): The catia application instance.
            product (Product): The catia product in which to create the groups.
        """
        self._caa = caa
        self._product = product

    def create(self) -> None:
        """Creates the groups by the group property of every child in the product."""
        self._remove()

        selection = ProductDocument(self._caa.active_document.com_object).selection
        selection.clear()

        groups: Dict[str, int] = {"NO GROUP": 2}
        with console.status("Reading existing groups from properties..."):
            for node in self._product.products:
                props = PyProperties(node.reference_product)
                if props.exists(resource.props.group):
                    groups[props.get_by_name(resource.props.group).value] = node.source

        for index, group in enumerate(groups):
            group_product = self._create(
                name=resource.settings.tree.group_prefix
                + str(group).upper()
                + resource.settings.tree.group_postfix,
                value=None if index == 0 else group,
                source=groups[group],
                index=index,
            )
            selection.add(group_product)

        self._exclude_from_bom()
        selection.clear()

    def _create(self, name: str, value: str | None, source: int, index: int) -> Product:
        """Create a new product flagged as group identifier.

        Args:
            name (str): The name of the product.
            value (str | None): The value of the group property.
            source (int): The source of the product.
            index (int): The index of the product (instance number).

        Returns:
            Product: The newly created product.
        """
        product = self._product.products.add_new_product(name)
        product.source = source
        product.name = f"{' - '*(70-len(name))}.{index}"

        props = PyProperties(product.reference_product)
        props.create(name=PROP_GROUP_IDENTIFIER, value="1")
        props.create(name=PROP_NO_BOM, value="1")
        if value:
            props.create(name=resource.props.group, value=value)

        log.logger.info(f"Created new product {name!r}.")
        return product

    def _remove(self) -> None:
        """Removes all products flagged as group identifier from the parent product."""
        nodes: List[Product] = []

        with console.status("Indexing existing group identifiers..."):
            for node in self._product.products:
                props = PyProperties(node.reference_product)
                if props.exists(PROP_GROUP_IDENTIFIER):
                    nodes.append(node)

        for node in nodes:
            node_name = node.part_number
            self._product.products.remove(node.product)
            log.logger.info(f"Removed group identifier {node_name!r}.")

    def _exclude_from_bom(self) -> None:
        """Excludes all selected items from the bill of material.

        Requires:
            All product that shall be excluded from the bill of material must be
            selected first (CATIA.Document.Selection).
        """
        window = PropertyWindow(caa=self._caa)
        try:
            window.connect()
            window.uncheck_bom()
            window.btn_ok.click()
        except WindowNotConnectedError:
            pass
