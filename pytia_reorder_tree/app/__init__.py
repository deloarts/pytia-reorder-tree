"""
    App submodule. Handles the workflow.
"""

from pathlib import Path

from app.exit import Exit
from app.groups import Groups
from app.log import log
from app.permissions import Permissions
from app.renumbering import Renumbering
from app.sort import Sort
from app.utils import get_ui_language
from app.window_handler.reorder_window import ReorderWindow
from exceptions import WindowNotConnectedError
from pycatia import catia
from pycatia.product_structure_interfaces.product import Product
from pycatia.product_structure_interfaces.product_document import ProductDocument
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource


def run() -> None:
    """Runs the application."""
    caa = catia()

    document = ProductDocument(caa.active_document.com_object)
    if not document.is_product:
        log.logger.error("The current document is not a product.")
        Exit().keep_open()

    product = Product(document.product.com_object)

    selection = ProductDocument(caa.active_document.com_object).selection
    selection.clear()

    workspace = Workspace(
        path=Path(document.full_name),
        filename=resource.settings.files.workspace,
        allow_outside_workspace=resource.settings.restrictions.allow_outside_workspace,
    )
    workspace.read_yaml()

    permissions = Permissions(workspace=workspace)
    permissions.check_user_permissions()
    permissions.check_editor_permissions()
    permissions.check_workspace_permissions()

    language = get_ui_language(product=product)
    resource.apply_language(language)  # type: ignore

    # Create new groups (CATIA Product Components)
    groups: Groups | None = None
    if resource.settings.tree.create_groups:
        groups = Groups(caa=caa, product=product)
        groups.create()

    # Select the main product and start the reorder graph tree window
    selection.clear()
    selection.add(product)
    graph_tree_window = ReorderWindow(caa=caa)
    try:
        graph_tree_window.connect()
    except WindowNotConnectedError:
        Exit().keep_open()
    selection.clear()

    # Sort the items of the graph tree window
    # Sorting is done prior by analyzing the graph tree (not the items in the reorder
    # graph tree window)
    try:
        sort = Sort(caa=caa)
        sort.set_products(products=product.products)
        sort.set_list_box(list_box=graph_tree_window.list_box)
        sort.set_up_button(button=graph_tree_window.btn_up)
        sort.set_delimiter(
            delimiter=resource.settings.tree.IN_delimiter,
            position=resource.settings.tree.IN_position,
        )
        sort.sort()

        graph_tree_window.btn_apply.click()
        graph_tree_window.btn_ok.click()
    except Exception as e:
        log.logger.exception(f"Failed to sort nodes: {e}")
        graph_tree_window.btn_abort.click()

    # Renumber all nodes in the product tree.
    try:
        renumbering = Renumbering(caa=caa, product=product)
        renumbering.renumber_all_nodes()
    except Exception as e:
        log.logger.exception(f"Failed to renumber nodes: {e}")

    # Exclude the created groups (CATIA Product Components) from the bill of material.
    # This is done at last, because the `hide from bill of material` option of the
    # property window from those selected CATIA Product Components doesn't recognize a
    # software-click, so the mouse has to be moved over the checkbox and click it.
    # This brings CATIA in the foreground and the user can't see the apps output
    # anymore. To surpass this, this is done at last.
    if groups is not None:
        groups.exclude_from_bom()

    Exit().close()
