"""
Load plugins cli to yo.
"""
from yo.config import config
from yo.utils import get_disabled_cli_modules, detail_error, logger

DISABLE_PLUGIN_CLI = get_disabled_cli_modules()


def load_cli():
    load_internal_cli()
    load_external_cli()


def get_internal_cli():
    return _get_cli(config.yo_cli_internal)


def get_external_cli():
    return _get_cli(config.yo_cli_external, as_single_file=True)


def load_internal_cli():
    cli_modules = get_internal_cli()
    cli_modules = [p for p in cli_modules if p not in DISABLE_PLUGIN_CLI]
    _dynamic_load('yo.plugin_cli.internal', cli_modules)


def load_external_cli():
    try:
        cli_modules = get_external_cli()
        _dynamic_load('yo.plugin_cli.external', cli_modules)
    except Exception as e:
        logger.log(detail_error(e))
        logger.log('Failed to load external plugins cli, please try `yo plugin reload`')


def _get_cli(cli_folder, as_single_file=False):
    """get module from internal cli folder."""
    cli_modules = []
    for cli_module in cli_folder.glob('*'):
        if as_single_file:
            if cli_module.is_file() \
                    and not cli_module.name.startswith('_') \
                    and cli_module.name.endswith('.py'):
                cli_modules.append(cli_module.stem)
        elif cli_module.is_dir() and not cli_module.name.startswith('_'):
            cli_modules.append(cli_module.stem)

    return cli_modules


def _dynamic_load(prefix, modules):
    """not very strong validation."""
    for module in modules:
        group = getattr(__import__(f'{prefix}.{module}', None, None, [module]), module)
        config.cli.add_command(group)
