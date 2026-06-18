from typing import ClassVar
from flask import render_template

from config import APP_AUTHOR, APP_NAME, APP_VERSION, HOST, PORT
from core.api.base_controller import BaseController


class WindowController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'WindowController'
    
    def register_routes(self):
        self.add_url_rule('/', view_func=self.index, methods=['GET'])
    
    # --- ENDPOINTS ---

    def index(self):
        return render_template(
            'index/index.html',
            app_name=APP_NAME,
            app_version=APP_VERSION,
            app_copyright=f'Copyright (c) {APP_AUTHOR}',
            app_url=f'http://{HOST}:{PORT}'
        )
