from __future__ import annotations

import platform
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path

from build_conf import (
    APP_AUTHOR,
    APP_COMPANY_NAME,
    APP_COPYRIGHT,
    APP_DESCRIPTION,
    APP_FILE_DESCRIPTION,
    APP_ICON_ICO,
    APP_ICON_PNG,
    APP_NAME,
    APP_PRODUCT_NAME,
    APP_VERSION,
    BIN_DIR,
    BUILD_DIR,
    BUILD_FOLDERS,
    DIST_DIR,
    ENTRY_FILE,
    MACOS_BUNDLE_IDENTIFIER,
    MACOS_CATEGORY_TYPE,
    RELEASE_DIR,
    RELEASE_METADATA_FILE,
    ROOT_DIR,
    WINDOWS_VERSION_FILE,
)


#region Common utilities

def run(command: list[str]) -> None:
    """Run a subprocess command from the project root and fail on errors."""
    print(' '.join(command))
    subprocess.run(command, check=True, cwd=ROOT_DIR)


def clean() -> None:
    """Remove build outputs and generated build helper files."""
    for path in [DIST_DIR, BUILD_DIR, RELEASE_DIR]:
        if path.exists():
            shutil.rmtree(path)

    for path in [WINDOWS_VERSION_FILE, BIN_DIR / 'app.icns']:
        if path.exists():
            path.unlink()

    iconset = BIN_DIR / 'app.iconset'
    if iconset.exists():
        shutil.rmtree(iconset)

    for spec in BIN_DIR.glob('*.spec'):
        spec.unlink()


def install_requirements() -> None:
    """Install runtime and build dependencies required by PyInstaller."""
    run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', 'pillow'])


def add_data_args() -> list[str]:
    """Build PyInstaller data-file arguments for project resource folders."""
    separator = ';' if platform.system() == 'Windows' else ':'
    items = []

    for folder in BUILD_FOLDERS:
        path = ROOT_DIR / folder
        if path.exists():
            items.extend(['--add-data', f'{path}{separator}{folder}'])

    return items


def base_pyinstaller_command() -> list[str]:
    """Create the shared PyInstaller command used by all target platforms."""
    return [
        sys.executable,
        '-m',
        'PyInstaller',
        '--noconfirm',
        '--clean',
        '--name',
        APP_NAME,
        '--windowed',
        '--onedir',
        '--distpath',
        str(DIST_DIR),
        '--workpath',
        str(BUILD_DIR),
        '--specpath',
        str(BIN_DIR),
        *add_data_args(),
    ]


def parse_version(version: str) -> tuple[int, int, int, int]:
    """Convert a semantic version string into a four-part version tuple."""
    parts = []

    for part in version.split('.'):
        if part.isdigit():
            parts.append(int(part))
        else:
            break

    return tuple((parts + [0, 0, 0, 0])[:4])


def py_string(value: str) -> str:
    """Return a Python string literal suitable for generated Python files."""
    return repr(value)


def write_release_metadata() -> Path:
    """Write a portable metadata text file for release artifacts."""
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path = RELEASE_DIR / RELEASE_METADATA_FILE
    metadata_path.write_text(
        '\n'.join([
            f'Name: {APP_NAME}',
            f'Version: {APP_VERSION}',
            f'Author: {APP_AUTHOR}',
            f'Copyright: {APP_COPYRIGHT}',
            f'Description: {APP_DESCRIPTION}',
            '',
        ]),
        encoding='utf-8',
    )

    return metadata_path


def copy_release_metadata(destination: Path) -> None:
    """Copy release metadata into an app bundle or distribution folder."""
    metadata_path = write_release_metadata()

    if destination.suffix == '.app':
        target_dir = destination / 'Contents' / 'Resources'
    else:
        target_dir = destination

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(metadata_path, target_dir / RELEASE_METADATA_FILE)

#endregion


#region Linux build and release

def build_for_linux() -> None:
    """Build the Linux application bundle with PyInstaller."""
    command = [
        *base_pyinstaller_command(),
    ]

    if APP_ICON_PNG.exists():
        command.extend(['--icon', str(APP_ICON_PNG)])

    command.append(ENTRY_FILE)
    run(command)


def package_release_for_linux() -> None:
    """Package the Linux build output as a compressed tar archive."""
    source = DIST_DIR / APP_NAME
    copy_release_metadata(source)
    archive = RELEASE_DIR / f'{APP_NAME}-linux'
    shutil.make_archive(str(archive), 'gztar', source)

#endregion


#region macOS build and release

def update_macos_info_plist(app_path: Path) -> None:
    """Apply application metadata to the generated macOS Info.plist file."""
    plist_path = app_path / 'Contents' / 'Info.plist'
    with plist_path.open('rb') as file:
        info = plistlib.load(file)

    info.update({
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': f'{APP_NAME} {APP_VERSION}',
        'CFBundleIdentifier': MACOS_BUNDLE_IDENTIFIER,
        'CFBundleName': APP_NAME,
        'CFBundleShortVersionString': APP_VERSION,
        'CFBundleVersion': APP_VERSION,
        'LSApplicationCategoryType': MACOS_CATEGORY_TYPE,
        'NSHumanReadableCopyright': APP_COPYRIGHT,
    })

    with plist_path.open('wb') as file:
        plistlib.dump(info, file)


def build_for_macos() -> None:
    """Build the macOS .app bundle with PyInstaller."""
    command = [
        *base_pyinstaller_command(),
        '--osx-bundle-identifier',
        MACOS_BUNDLE_IDENTIFIER,
    ]

    if APP_ICON_PNG.exists():
        command.extend(['--icon', str(APP_ICON_PNG)])

    command.append(ENTRY_FILE)
    run(command)
    update_macos_info_plist(DIST_DIR / f'{APP_NAME}.app')


def package_release_for_macos() -> None:
    """Package the macOS .app bundle as a symlink-safe zip archive."""
    source = DIST_DIR / f'{APP_NAME}.app'
    copy_release_metadata(source)
    archive = RELEASE_DIR / f'{APP_NAME}-macos.zip'
    run([
        'ditto',
        '-c',
        '-k',
        '--sequesterRsrc',
        '--keepParent',
        str(source),
        str(archive),
    ])

#endregion


#region Windows build and release

def write_windows_version_file() -> None:
    """Generate a PyInstaller version resource file for Windows metadata."""
    file_version = parse_version(APP_VERSION)
    product_version = file_version

    WINDOWS_VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    WINDOWS_VERSION_FILE.write_text(
        f'''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={file_version},
    prodvers={product_version},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0),
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', {py_string(APP_COMPANY_NAME)}),
          StringStruct('FileDescription', {py_string(APP_FILE_DESCRIPTION)}),
          StringStruct('FileVersion', {py_string(APP_VERSION)}),
          StringStruct('InternalName', {py_string(APP_NAME)}),
          StringStruct('LegalCopyright', {py_string(APP_COPYRIGHT)}),
          StringStruct('OriginalFilename', {py_string(f'{APP_NAME}.exe')}),
          StringStruct('ProductName', {py_string(APP_PRODUCT_NAME)}),
          StringStruct('ProductVersion', {py_string(APP_VERSION)}),
        ],
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])]),
  ],
)
''',
        encoding='utf-8',
    )


def build_for_windows() -> None:
    """Build the Windows executable folder with icon and version metadata."""
    write_windows_version_file()
    command = [
        *base_pyinstaller_command(),
        '--contents-directory',
        '.',
        '--version-file',
        str(WINDOWS_VERSION_FILE),
    ]

    if APP_ICON_ICO.exists():
        command.extend(['--icon', str(APP_ICON_ICO)])

    command.append(ENTRY_FILE)
    run(command)


def package_release_for_windows() -> None:
    """Package the Windows build output as a zip archive."""
    source = DIST_DIR / APP_NAME
    copy_release_metadata(source)
    archive = RELEASE_DIR / f'{APP_NAME}-windows'
    shutil.make_archive(str(archive), 'zip', source)

#endregion


def build_for_system(system: str) -> None:
    """Run the platform-specific build step for the detected system."""
    if system == 'Windows':
        build_for_windows()
    elif system == 'Darwin':
        build_for_macos()
    elif system == 'Linux':
        build_for_linux()
    else:
        raise RuntimeError(f'Unsupported system: {system}')


def package_release_for_system(system: str) -> None:
    """Run the platform-specific release packaging step."""
    if system == 'Windows':
        package_release_for_windows()
    elif system == 'Darwin':
        package_release_for_macos()
    elif system == 'Linux':
        package_release_for_linux()
    else:
        raise RuntimeError(f'Unsupported system: {system}')


def main() -> None:
    """Clean, install dependencies, build, and package for the current OS."""
    system = platform.system()

    clean()
    install_requirements()
    build_for_system(system)
    package_release_for_system(system)

    print()
    print('Ready.')
    print(f'System:  {system}')
    print(f'Build:   {DIST_DIR}')
    print(f'Release: {RELEASE_DIR}')


if __name__ == '__main__':
    main()
