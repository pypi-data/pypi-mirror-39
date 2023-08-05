"""
Application entrypoint
"""

from brewblox_service import brewblox_logger, scheduler, service

from brewblox_datastore import datastore

LOGGER = brewblox_logger(__name__)


def create_parser(default_name='datastore'):
    parser = service.create_parser(default_name=default_name)
    group = parser.add_argument_group('Datastore configuration')
    group.add_argument('--file',
                       help='Backing file for the datastore.',
                       required=True)
    group.add_argument('--volatile',
                       help='Do not write changes to file. [%(default)s]',
                       action='store_true')
    return parser


def main():
    app = service.create_app(parser=create_parser())

    scheduler.setup(app)
    datastore.setup(app)

    service.furnish(app)
    service.run(app)


if __name__ == '__main__':
    main()
