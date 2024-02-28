"""
    Sort submodule.
"""

from typing import List

from const import PROP_GROUP_IDENTIFIER
from exceptions import WarningError
from pycatia.in_interfaces.application import Application
from pycatia.knowledge_interfaces.str_param import StrParam
from pycatia.product_structure_interfaces.product import Product
from pycatia.product_structure_interfaces.products import Products
from pytia.log import log
from pywinauto.controls.win32_controls import ButtonWrapper
from pywinauto.controls.win32_controls import ListBoxWrapper
from resources import resource


class Sort:
    """Sort class."""

    def __init__(self, caa: Application) -> None:
        self._caa = caa
        self._list_box: ListBoxWrapper | None = None
        self._btn_up: ButtonWrapper | None = None
        self._delimiter: str | None = None
        self._position: int = 0
        self._products: List[Product] = []

    def set_products(self, products: Products) -> None:
        """Gathers all processable nodes from the graph tree.

        Args:
            products (Products): The products instance from the graph tree object to
            be sorted.
        """
        log.info("Gathering processable products from assembly...")
        for product in products:
            if product.is_catproduct() or product.is_catpart():
                self._products.append(product)

        if resource.settings.debug:
            msg = "\n - ".join(p.name for p in self._products)
            log.debug(f"Processable items:\n - {msg}")

    def set_list_box(self, list_box: ListBoxWrapper) -> None:
        """Sets the list box object.

        Args:
            list_box (ListBoxWrapper): The list box object from which to fetch the
            sort-items.
        """
        self._list_box = list_box

    def set_up_button(self, button: ButtonWrapper) -> None:
        """Sets the up button object.

        Args:
            button (ButtonWrapper): The button which triggers the up command.
        """
        self._btn_up = button

    def set_delimiter(self, delimiter: str, position: int) -> None:
        """Sets the delimiter for the instance number (#IN#) of the graph tree.

        Args:
            delimiter (str): The delimiter which encapsules the instance number.
            position (int): The position where to find the instance number.

        Example:
            If the tree node string looks like this
                        #PN# | #IN# | #SO#
            then the delimiter is ' | ' and the position is '1'.
        """
        self._delimiter = delimiter
        self._position = position

    def sort(self) -> None:
        """
        This requires that the CATIA tree has at least the setting for the
        exemplar name enabled:  #IN#
        enabled in the Infrastructure/Product Structure/Nodes options.
        """

        assert self._products is not None
        assert self._list_box is not None
        assert self._btn_up is not None

        if self._delimiter is None:
            log.warning(
                "No delimiter for tree nodes set. "
                "This may cause inconsistent results."
            )

        log.info("Pre-sorting items from assembly...")
        self._products.sort(
            key=lambda x: (Filter.default(x) is None, Filter.default(x))
        )
        log.info("Pre-sorted items from assembly.")

        unsorted_tree_items = [item for item in self._list_box.item_texts()]
        sorted_tree_items = [None] * len(unsorted_tree_items)

        if len(self._products) != len(sorted_tree_items):
            raise WarningError("Cannot assign all items from assembly to the listbox.")

        for product_index, product_item in enumerate(self._products):
            for tree_index, tree_item in enumerate(unsorted_tree_items):
                if self._delimiter is None:
                    if product_item.name in tree_item:
                        sorted_tree_items[product_index] = unsorted_tree_items[
                            tree_index
                        ]
                else:
                    instance_number = str(tree_item).split(self._delimiter)[
                        self._position
                    ]
                    if instance_number == product_item.name:
                        sorted_tree_items[product_index] = unsorted_tree_items[
                            tree_index
                        ]

        log.info("Assigned product items to the appropriate tree items.")

        # print([i.name for i in self._products])
        # print([item for item in sorted_tree_items])

        log.info("Reordering tree items...")
        for index, value in enumerate(sorted_tree_items):
            self._list_box.select(value)
            current_position = self._list_box.item_texts().index(value)
            target_position = index
            for _ in range(current_position - target_position):
                self._btn_up.click()

        log.info("Successfully reordered graph tree items.")

    def _filter(self, product: Product) -> tuple | None:
        return (
            (product.source, product.name) if isinstance(product.source, int) else None
        )


class Filter:
    """Filter class for the sort algorithm."""

    @staticmethod
    def default(product: Product):
        """
        The default filter for the sort algorithm.
        Filters by the following logic:

        - Source of the tree node
        - Group property of the tree node (if the node has the property "group")
        - Group identifier (the empty CATProduct which is used as separator)
        - Filter property
        - Part number
        - Instance number
        """
        filter_property: StrParam | None = None
        props = product.reference_product.user_ref_properties

        def _exists(name: str):
            for i in range(1, props.count + 1):
                if props.item(i).name == name:
                    return True
            return False

        filter_property = (
            StrParam(props.item(resource.props.filter).com_object)
            if _exists(resource.props.filter)
            else None
        )
        group_property = (
            StrParam(props.item(resource.props.group).com_object)
            if _exists(resource.props.group)
            else None
        )
        group_identifier = (
            StrParam(props.item(PROP_GROUP_IDENTIFIER).com_object)
            if _exists(PROP_GROUP_IDENTIFIER)
            else None
        )

        key = (
            # Items are sorted by their source first
            product.source,
            # Items are then sorted by their group (items with no group are last)
            1 if group_property else 2,
            group_property.value if group_property else "",
            # Group identifiers
            1 if group_identifier else 2,
            group_identifier.value if group_identifier else "",
            # Bought items are then sorted by the filter property
            filter_property.value if filter_property and product.source == 2 else "",
            # Finally items are sorted by the partnumber and name
            product.part_number,
            product.name,
        )

        log.debug(f"Filter key: {key}")
        return key

    @staticmethod
    def default_2(product: Product):
        """Experimental default filter."""
        filter_property: StrParam | None = None

        for prop in product.parameters.all_parameters():
            try:
                prop = StrParam(prop.com_object)
                if prop.name == resource.props.filter:
                    filter_property = prop
                    break
            except Exception:
                pass

        if product.source == 2 and filter_property is not None:
            key = (
                product.source,
                filter_property.value,
                product.part_number,
                product.name,
            )
        else:
            key = (
                product.source,
                product.part_number,
                product.name,
            )

        # log.debug(f"Filter key: {key}")
        return key

    @staticmethod
    def source(product: Product):
        return (
            (product.source, product.name) if isinstance(product.source, int) else None
        )

    @staticmethod
    def unknown(product: Product):
        """Filter by source: unknown."""
        return (product.source, product.name) if product.source == 0 else None

    @staticmethod
    def made(product: Product):
        """Filter by source: made."""
        return (product.source, product.name) if product.source == 1 else None

    @staticmethod
    def bought(product: Product):
        """Filter by source: bought."""
        return (product.source, product.name) if product.source == 2 else None
