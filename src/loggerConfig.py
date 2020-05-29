import logging

# Logging is cool!

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('s3transfer').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logFormat = '{"timestamp": "%(asctime)s", "thread": "%(threadName)s",\
 "level": "%(levelname)s",\
 "location": "%(module)s:%(lineno)d", "message": "%(message)s"}'
# logFormat = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
logging.basicConfig(format=logFormat, level=logging.DEBUG)

logger.debug('Inicializando logger')
