from loguru import logger
from config.get_config import config


logger.add(config['log']['log_path'],
           rotation=config['log']['rotation'],
           enqueue=True,
           colorize=True,
           encoding='utf-8',
           format=config['log']['format'],
           # retention=config['log']['retention'],
           level='INFO')
