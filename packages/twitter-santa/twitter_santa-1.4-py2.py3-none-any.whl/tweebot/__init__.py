



import logging
import coloredlogs

from tweebot.agents import UserAgentProvider

__author__ = "Vasyl Paliy"
__version__ = '1.4'
__license___ = "MIT"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)
coloredlogs.install(fmt='%(asctime)s | %(message)s')

ua_provider = UserAgentProvider()
