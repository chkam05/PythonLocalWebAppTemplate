from __future__ import annotations
from typing import ClassVar

from flask import jsonify, request

from core.api.base_controller import BaseController
from models.settings_data_model import SettingsDataModel
from storage.settings_storage import SettingsStorage


class SettingsController(BaseController):
    CONTROLLER_NAME: ClassVar[str] = 'SettingsController'

    def __init__(self, settings_storage: SettingsStorage):
        self._settings_storage = settings_storage
        super().__init__()

    def register_routes(self):
        self.add_url_rule('/settings', view_func=self.load_settings, methods=['GET'])
        self.add_url_rule('/settings', view_func=self.save_settings, methods=['POST'])

    # --- ENDPOINTS ---

    def load_settings(self):
        settings = self._settings_storage.load()
        return jsonify(settings.to_dict())

    def save_settings(self):
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({'error': 'Settings payload must be a JSON object.'}), 400

        settings = SettingsDataModel.from_dict(data)
        self._settings_storage.save(settings)
        return jsonify(settings.to_dict())
