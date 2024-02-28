"""
    Groups submodule.
    Handles the documents product flagged as group identifier.
"""

from typing import Dict
from typing import List

from const import PROP_GROUP_IDENTIFIER
from const import PROP_NO_BOM
from exceptions import WindowNotConnectedError
from handler.window_handler.property_window import PropertyWindow
from pycatia.in_interfaces.application import Application
from pycatia.product_structure_interfaces.product import Product
from pycatia.product_structure_interfaces.product_document import ProductDocument
from pytia.log import log
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
        self._created_groups: List[Product] = []

    def create(self) -> None:
        """Creates the groups by the group property of every child in the product."""
        self._remove()

        groups: Dict[str, int] = {"NO GROUP": 2}
        # The groups dict contains the group name as key and the respective CATIA
        # source as value (0 = unknown, 1 = made, 2 = bought).
        # The source of `no groups` is 2, because the sorting algorithm moves bought
        # nodes at the end of the product tree. So items with no group assigned will
        # be positioned last.

        self._created_groups = []

        log.info("Reading existing groups from properties...")
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
            self._created_groups.append(group_product)

    def exclude_from_bom(self) -> None:
        """Excludes all selected items from the bill of material.

        Requires:
            All product that shall be excluded from the bill of material must be
            selected first (CATIA.Document.Selection).
        """
        selection = ProductDocument(self._caa.active_document.com_object).selection
        selection.clear()
        for group_product in self._created_groups:
            selection.add(group_product)

        window = PropertyWindow(caa=self._caa)
        try:
            window.connect()
            window.uncheck_bom()
            window.btn_ok.click()
        except WindowNotConnectedError:
            pass

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

        log.info(f"Created new product {name!r}.")
        return product

    def _remove(self) -> None:
        """Removes all products flagged as group identifier from the parent product."""
        nodes: List[Product] = []

        log.info("Indexing existing group identifiers...")
        for node in self._product.products:
            props = PyProperties(node.reference_product)
            if props.exists(PROP_GROUP_IDENTIFIER):
                nodes.append(node)

        for node in nodes:
            node_name = node.part_number
            self._product.products.remove(node.product)
            log.info(f"Removed group identifier {node_name!r}.")
