#############################################################################
# Copyright (c) 2018, Voila Contributors                                    #
#                                                                           #
# Distributed under the terms of the BSD 3-Clause License.                  #
#                                                                           #
# The full license is in the file LICENSE, distributed with this software.  #
#############################################################################

import tornado.web

from jupyter_server.base.handlers import JupyterHandler

import nbformat
from nbconvert.preprocessors.execute import executenb
from nbconvert import HTMLExporter

from .paths import NBCONVERT_TEMPLATE_ROOT


class VoilaHandler(JupyterHandler):
    def initialize(self, notebook_path=None, strip_sources=True, custom_template_path=None, config=None):
        self.notebook_path = notebook_path
        self.strip_sources = strip_sources
        self.template_path = [NBCONVERT_TEMPLATE_ROOT]
        self.exporter_config = config
        if custom_template_path:
            self.template_path.insert(0, custom_template_path)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, path=None):
        if path:
            path += '.ipynb'  # when used as a jupyter server extension, we don't use the extension
        # if the handler got a notebook_path argument, always serve that
        notebook_path = self.notebook_path or path

        model = self.contents_manager.get(path=notebook_path)
        if 'content' in model:
            notebook = model['content']
        else:
            raise tornado.web.HTTPError(404, 'file not found')

        # Fetch kernel name from the notebook metadata
        kernel_name = notebook.metadata.get('kernelspec', {}).get('name', self.kernel_manager.default_kernel_name)

        # Launch kernel and execute notebook
        kernel_id = yield tornado.gen.maybe_future(self.kernel_manager.start_kernel(kernel_name=kernel_name))
        km = self.kernel_manager.get_kernel(kernel_id)
        result = executenb(notebook, km=km)

        # render notebook to html
        resources = {
            'kernel_id': kernel_id,
            'base_url': self.base_url
        }

        exporter = HTMLExporter(
            template_file='voila.tpl',
            template_path=self.template_path,
            config=self.exporter_config
        )

        if self.strip_sources:
            exporter.exclude_input = True
            exporter.exclude_output_prompt = True
            exporter.exclude_input_prompt = True

        # Filtering out empty cells.
        def filter_empty_code_cells(cell):
            return (
                cell.cell_type != 'code' or                     # keep non-code cells
                (cell.outputs and not exporter.exclude_output)  # keep cell if output not excluded and not empty
                or not exporter.exclude_input                   # keep cell if input not excluded
            )
        result.cells = list(filter(filter_empty_code_cells, result.cells))

        html, resources = exporter.from_notebook_node(result, resources=resources)

        # Compose reply
        self.set_header('Content-Type', 'text/html')
        self.write(html)

