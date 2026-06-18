from pathlib import Path

from config import (
    APP_AUTHOR,
    APP_DESCRIPTION,
    APP_ICON,
    APP_ICON_WINDOWS,
    APP_NAME,
    APP_VERSION,
)


ROOT_DIR = Path(__file__).resolve().parent

BIN_DIR = ROOT_DIR / 'bin'
BUILD_DIR = BIN_DIR / 'build'
DIST_DIR = BIN_DIR / 'dist'
RELEASE_DIR = BIN_DIR / 'release'

BUILD_FOLDERS = [
    'assets',
    'templates',
]

APP_COPYRIGHT = f'Copyright (c) {APP_AUTHOR}'
APP_COMPANY_NAME = APP_AUTHOR
APP_PRODUCT_NAME = APP_NAME
APP_FILE_DESCRIPTION = APP_DESCRIPTION

APP_ICON_PNG = Path(APP_ICON)
APP_ICON_ICO = Path(APP_ICON_WINDOWS)

ENTRY_FILE = 'app.py'

RELEASE_METADATA_FILE = 'APP_METADATA.txt'
WINDOWS_VERSION_FILE = BIN_DIR / 'version_info.txt'

MACOS_APP_NAME = 'python-local-webapp-template'
MACOS_BUNDLE_IDENTIFIER = f'com.example.{MACOS_APP_NAME}'
MACOS_CATEGORY_TYPE = 'public.app-category.developer-tools'
