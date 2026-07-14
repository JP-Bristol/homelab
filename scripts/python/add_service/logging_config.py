import logging

def setup_logging():

    """Konfiguriert den Root-Logger mit Handlern für Konsole und Log-Datei."""

    logger = logging.getLogger()

    if logger.handlers:
        return logger
    
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("logs/service.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)-12s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(file_handler)


    runbook_logger = logging.getLogger("runbook_data")
    runbook_logger.setLevel(logging.INFO)
    runbook_handler = logging.FileHandler("logs/service_events.log")
    runbook_logger.propagate = False
    runbook_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    runbook_logger.addHandler(runbook_handler)


    return logger