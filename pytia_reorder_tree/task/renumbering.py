"""
    Groups submodule.
    Handles the documents product flagged as group identifier.
"""

from typing import Dict
from typing import List

from const import PROP_GROUP_IDENTIFIER
from pycatia.in_interfaces.application import Application
from pycatia.product_structure_interfaces.product import Product
from pytia.log import log
from pytia.wrapper.properties import PyProperties
from resources import resource
from type_collections import InstanceIndex
from type_collections import PartNumber


class Renumbering:
    """Renumbering class."""

    def __init__(self, caa: Application, product: Product) -> None:
        """Inits the class.

        Args:
            caa (Application): The catia application instance.
            product (Product): The catia product which nodes to renumber.
        """
        self._caa = caa
        self._product = product
        self._created_groups: List[Product] = []

    def renumber_all_nodes(self) -> None:
        """
        Renumbers all nodes in the product. Start index is set in the settings.json.
        Skips the task if `renumber` in the settings.json is set to false.
        """
        if not resource.settings.tree.renumber:
            log.info("Skipped renumbering product nodes.")
            return

        log.info("Renumbering all nodes...")
        self._renumber(make_hash=True)
        self._renumber(make_hash=False)

    def _renumber(self, make_hash: bool) -> None:
        """Does the actual renumbering.

        Args:
            make_hash (bool): If true, all instance number will be set to the hash \
                value of the correct new instance number.
        """
        node_index: Dict[PartNumber, InstanceIndex] = {}
        for node in self._product.products:
            props = PyProperties(node.reference_product)

            if node.part_number in node_index:
                node_index[node.part_number] += 1
            else:
                node_index[node.part_number] = resource.settings.tree.start_index

            if not props.exists(PROP_GROUP_IDENTIFIER):
                node_name = f"{node.part_number}.{node_index[node.part_number]}"
                node.name = str(hash(node_name)) if make_hash else node_name
