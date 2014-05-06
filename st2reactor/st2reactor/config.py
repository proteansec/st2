from oslo.config import cfg

CONF = cfg.CONF

logging_opts = [
    cfg.StrOpt('config_file', default='etc/logging.conf',
               help='location of the logging.conf file')
]
CONF.register_opts(logging_opts, group='reactor_logging')

use_debugger = cfg.BoolOpt(
    'use-debugger', default=False,
    help='Enables debugger. Note that using this option changes how the '
         'eventlet library is used to support async IO. This could result in '
         'failures that do not occur under normal operation.'
)
CONF.register_cli_opt(use_debugger)


def parse_args(args=None):
    CONF(args=args)