import logging
import logging.config
from .queue0 import RabbitProducer0
from .utils import dump_json
import traceback

__log_path = '.'


def _get_config(root_path='.', is_console=True):
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{levelname}][{asctime}]{message}',
                'style': '{',
            },
        },
        'handlers': {
            'info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': root_path + '/info.log',
                'formatter': 'verbose'
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': root_path + '/error.log',
                'formatter': 'verbose'
            },
        },
        'root': {
            'handlers': ['info', 'error'],
            'level': 'INFO',
        },
    }
    if is_console:
        config['handlers'] = {
            'console': {
                'class': 'logging.StreamHandler',
            }
        }
        config['root'] = {
            'handlers': ['console'],
            'level': 'INFO',
        }
    return config


__logger = None
__module = ''
__producer = None
__monit_queue = None


def log_init_config(module='unknown', root_path='.', monit_queue=''):
    global __logger, __module, __monit_queue
    logging.config.dictConfig(_get_config(root_path, root_path == 'console'))
    __logger = logging.getLogger('root')
    __monit_queue = monit_queue
    if module is not None:
        __module = module


def _check_log_init():
    global __logger
    if __logger is None:
        log_init_config()


def _check_producer():
    global __producer, __monit_queue
    if __producer is not None:
        return __producer
    if __monit_queue is None or __monit_queue == '':
        return None
    __producer = RabbitProducer0(__monit_queue)
    return __producer


def _send_monit_message(topic, module, message):
    try:
        global __module
        if __module is not None and len(module) == 0:
            module = __module
        producer = _check_producer()
        if producer is None:
            return
        json = {'module': module, 'message': message}
        producer.send(topic, dump_json(json))
    except Exception as ex:
        log_exception(ex, False)


def log_info(msg):
    global __logger
    if __logger is None:
        return
    __logger.info(msg)


def log_error(msg, need_monit=True, module=''):
    global __logger, __module
    if __logger is None:
        return
    message = msg
    if module != '':
        message = '[' + module + ']' + msg
    __logger.error(message)
    if need_monit:
        _send_monit_message('error_logs', module, msg)


def raise_exception(msg, need_monit=True, module=''):
    log_exception(msg, need_monit, module)
    raise Exception(msg)


def log_exception(ex, need_monit=True, module=''):
    global __logger
    if __logger is None:
        return
    msg = '[%s]%s' % (module, ex)
    __logger.exception(msg)
    if need_monit:
        detail = traceback.format_exc()
        _send_monit_message('error_logs', module, msg + '\n' + detail)
