#!/usr/bin/env python3
import logging
import os.path

import click
import toml
import coloredlogs
from todotxt import TodoFile

from .services import AbstractService

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

_log = logging.getLogger(__name__)


@click.command()
@click.argument('services', nargs=-1, default=None, required=False)
@click.option('--config-file', '-c', default=os.path.expanduser('~/.bugtodo.toml'), help='Configuration file path', type=click.File('r'))
def cli(services, config_file: str) -> None:
    coloredlogs.install(level='INFO', fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
    configuration = toml.load(config_file)
    todo_file = TodoFile(configuration['todotxt']['file_path'])
    todo_file.load()
    if services:
        _log.info('Apply filter, services that will be loaded: %s', services)
    for service_type, service_configurations in configuration.get('services').items():  # type: ignore
        service_class = AbstractService.registered_services.get(service_type)
        if service_class is None:
            _log.error("Cannot find service class for service type %s, skip it", service_type)
            continue
        for service_name, service_params in service_configurations.items():
            if not services or service_name in services:
                service = service_class(  # type: ignore
                    service_name=service_name,
                    **service_params
                )
                service.fetch_issues(todo_file)
    todo_file.save()


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
