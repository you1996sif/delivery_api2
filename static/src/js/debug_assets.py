#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
from odoo.modules.registry import Registry
# Adjust this path to your Odoo installation directory
odoo_path = Path('/usr/lib/python3/dist-packages')
sys.path.append(str(odoo_path))

import odoo
from odoo.tools import config

# Configure logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

def debug_asset_loading(env):
    IrAsset = env['ir.asset']
    IrQweb = env['ir.qweb']

    def check_addon_manifests():
        _logger.info("Checking addon manifests...")
        for addon in odoo.modules.module.get_modules():
            try:
                manifest = odoo.modules.module.get_manifest(addon)
                if 'assets' not in manifest:
                    _logger.warning(f"Addon '{addon}' does not have 'assets' key in its manifest.")
                else:
                    _logger.info(f"Addon '{addon}' has 'assets' key in its manifest.")
            except Exception as e:
                _logger.error(f"Error checking manifest for addon '{addon}': {e}")

    def debug_get_asset_paths():
        _logger.info("Debugging _get_asset_paths method...")
        try:
            paths = IrAsset._get_asset_paths('web.assets_frontend')
            _logger.info(f"Asset paths for 'web.assets_frontend': {paths}")
        except Exception as e:
            _logger.error(f"Error in _get_asset_paths: {e}")

    def debug_get_asset_content():
        _logger.info("Debugging _get_asset_content method...")
        try:
            content = IrQweb._get_asset_content('web.assets_frontend')
            _logger.info(f"Asset content for 'web.assets_frontend': {content}")
        except Exception as e:
            _logger.error(f"Error in _get_asset_content: {e}")

    check_addon_manifests()
    debug_get_asset_paths()
    debug_get_asset_content()

def main():
    config.parse_config([])
    registry = Registry(config['db_name'])
    with registry.cursor() as cr:
        registry = odoo.registry(config['db_name'])
        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
            debug_asset_loading(env)

if __name__ == "__main__":
    main()
