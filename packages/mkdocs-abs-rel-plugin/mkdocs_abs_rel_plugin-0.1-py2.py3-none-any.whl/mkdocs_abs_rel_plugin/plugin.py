"""Mkdocs plugin for converting absolute paths to relative ones
relative to a given path or default doc path."""
import logging
from pathlib import Path

from mkdocs import utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from mkdocs_abs_rel_plugin import _absolute_to_rel

LOGGER = logging.getLogger(__name__)


class AbsToRelPlugin(BasePlugin):
    def __init__(self):
        pass

    DEFAULT_ROOT_FOLDER = "docs"

    config_scheme = (
        # (
        #     "root_folder",
        #     config_options.Type(
        #         utils.string_types, default=DEFAULT_ROOT_FOLDER
        #     ),
        # ),
    )

    def on_page_markdown(
        self, markdown, page: Page = None, config: Config = None, **kwargs
    ):
        abs_src_path = Path(page.file.abs_src_path)
        doc_folder = Path(config.data.get("docs_dir"))

        new_md = _absolute_to_rel(markdown, abs_src_path, doc_folder)
        return new_md
