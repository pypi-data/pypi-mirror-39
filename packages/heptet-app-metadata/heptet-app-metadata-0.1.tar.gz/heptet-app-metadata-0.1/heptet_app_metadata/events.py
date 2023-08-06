import logging

from sqlalchemy.orm import Mapper

from heptet_app_metadata import process_mapper

logger = logging.getLogger(__name__)

mappers = {}

def handle_after_create(target, connection, **kwargs):
    logger.debug("after create %s", target)

