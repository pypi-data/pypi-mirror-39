import logging
import random, string



logger = logging.getLogger('SHORTNR_UTILS')



try:
    from dev.settings import SHORTNR_CONFIG
except ImportError:
    logger.debug('SHORTNR_CONFIG not defined in project settings')



KEY_LEN = SHORTNR_CONFIG.get('KEY_LENGTH') or 6
CHAR_POOL = SHORTNR_CONFIG.get('CHAR_POOL') or string.ascii_letters+string.digits




def generate_key():
    return ''.join(random.choices(CHAR_POOL, k=KEY_LEN))
