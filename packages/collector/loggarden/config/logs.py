import logging

internal_logger = logging.getLogger("loggarden.internal")
internal_logger.propagate = False

handler = logging.FileHandler("loggarden_errors.log")
handler.setLevel(logging.ERROR)

internal_logger.addHandler(handler)