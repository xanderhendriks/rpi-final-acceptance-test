import platform
from pathlib import Path
from typing import Optional
from datetime import datetime

from nicegui import events, ui


class LocalFilePicker(ui.label):

    def __init__(self, directory: str, *,
                 upper_limit: Optional[str] = ..., multiple: bool = False, show_hidden_files: bool = False) -> None:
        """Local File Picker

        This is a simple file picker that allows you to select a file from the local filesystem where NiceGUI is running.

        :param directory: The directory to start in.
        :param upper_limit: The directory to stop at (None: no limit, default: same as the starting directory).
        :param multiple: Whether to allow multiple files to be selected.
        :param show_hidden_files: Whether to show hidden files.
        """
        super().__init__()

        self.path = Path(directory).expanduser()
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(directory if upper_limit == ... else upper_limit).expanduser()
        self.show_hidden_files = show_hidden_files

        with self:
            self.grid = ui.aggrid({
                'columnDefs': [{'field': 'name', 'headerName': 'Files'},
                               {'field': 'modified', 'headerName': 'Last modified'},
                               {'field': 'size', 'headerName': 'Size'}],
                'rowSelection': 'multiple' if multiple else 'single',
            }, html_columns=[0]).on('cellDoubleClicked', self._handle_double_click)
        self._update_grid()

    def _update_grid(self) -> None:
        paths = list(self.path.glob('*'))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith('.')]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options['rowData'] = [
            {
                'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
                'modified': f"{datetime.fromtimestamp(p.lstat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
                'size': f'{p.lstat().st_size}',
                'path': str(p),
            }
            for p in paths
        ]
        if self.upper_limit is None and self.path != self.path.parent or \
                self.upper_limit is not None and self.path != self.upper_limit:
            self.grid.options['rowData'].insert(0, {
                'name': '📁 <strong>..</strong>',
                'path': str(self.path.parent),
            })
        self.grid.update()

    def _handle_double_click(self, e: events.GenericEventArguments) -> None:
        self.path = Path(e.args['data']['path'])
        if self.path.is_dir():
            self._update_grid()

    async def get_selected_files(self):
        rows = await ui.run_javascript(f'getElement({self.grid.id}).gridOptions.api.getSelectedRows()')
        return [r['path'] for r in rows]
