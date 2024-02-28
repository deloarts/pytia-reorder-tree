"""
    App submodule. Handles the workflow.
"""

from tkinter import Tk

from app.vars import Variables
from const import STEPS
from exceptions import WarningError
from handler.utils import get_ui_language
from handler.window_handler.reorder_window import ReorderWindow
from pycatia import catia
from pycatia.product_structure_interfaces.product import Product
from pycatia.product_structure_interfaces.product_document import ProductDocument
from pytia.exceptions import PytiaWrongDocumentTypeError
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource
from task.groups import Groups
from task.permissions import Permissions
from task.renumbering import Renumbering
from task.sort import Sort


class Task:
    def __init__(self, root: Tk, vars: Variables) -> None:
        self.root = root
        self.vars = vars

        self.caa = catia()
        self.document = ProductDocument(self.caa.active_document.com_object)
        if not self.document.is_product:
            raise PytiaWrongDocumentTypeError("The current document is not a product.")

        self.product = Product(self.document.product.com_object)

        self.selection = ProductDocument(self.caa.active_document.com_object).selection
        self.selection.clear()

        self.workspace = Workspace(
            path=self.product.path(),
            filename=resource.settings.files.workspace,
            allow_outside_workspace=resource.settings.restrictions.allow_outside_workspace,
        )
        self.workspace.read_yaml()

        permissions = Permissions(workspace=self.workspace)
        permissions.check_user_permissions()
        permissions.check_editor_permissions()
        permissions.check_workspace_permissions()

        language = get_ui_language(product=self.product)
        resource.apply_language(language)  # type: ignore

    def _update_info(self, text: str) -> None:
        self.vars.task.set(self.vars.task.get() + 1)
        self.vars.status.set(f"Step {self.vars.task.get()} of {STEPS}: {text}")
        self.root.update()

    def _create_groups(self) -> None:
        self._update_info("Creating groups...")

        # Create new groups (CATIA Product Components)
        groups: Groups | None = None
        if resource.settings.tree.create_groups:
            try:
                groups = Groups(caa=self.caa, product=self.product)
                groups.create()
                groups.exclude_from_bom()
            except Exception as e:
                msg = (
                    "Failed to create groups. Maybe some nodes in the tree are invalid. "
                    f"Verbose: {e}"
                )
                log.error(msg)
                raise WarningError(msg)

    def _sort_nodes(self) -> None:
        self._update_info("Connecting to graph tree window...")

        # Select the main product and start the reorder graph tree window
        self.selection.clear()
        self.selection.add(self.product)
        graph_tree_window = ReorderWindow(caa=self.caa, vars=self.vars)
        graph_tree_window.connect()
        self.selection.clear()

        # Sort the items of the graph tree window
        # Sorting is done prior by analyzing the graph tree (not the items in the reorder
        # graph tree window)
        try:
            sort = Sort(caa=self.caa)
            sort.set_products(products=self.product.products)
            sort.set_list_box(list_box=graph_tree_window.list_box)
            sort.set_up_button(button=graph_tree_window.btn_up)
            sort.set_delimiter(
                delimiter=resource.settings.tree.IN_delimiter,
                position=resource.settings.tree.IN_position,
            )
            self._update_info("Sorting all nodes in the graph tree...")
            sort.sort()

            graph_tree_window.btn_apply.click()
            graph_tree_window.btn_ok.click()
        except Exception as e:
            msg = f"Failed to sort nodes: {e}"
            log.error(msg)
            graph_tree_window.btn_abort.click()
            raise WarningError(msg)

    def _renumber_nodes(self) -> None:
        self._update_info("Renumbering all nodes...")

        # Renumber all nodes in the product tree.
        try:
            renumbering = Renumbering(caa=self.caa, product=self.product)
            renumbering.renumber_all_nodes()
        except Exception as e:
            msg = f"Failed to renumber nodes: {e}"
            log.error(msg)
            raise WarningError(msg)

    def run(self) -> None:
        self._create_groups()
        self._sort_nodes()
        self._renumber_nodes()

        self.root.destroy()
