import logging
from pathlib import Path


def setup_logger(project_root: Path) -> logging.Logger:
    """
    Set up pipeline logging.
    """

    logs_path = project_root / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)

    log_file_path = logs_path / "pipeline_run.log"

    logger = logging.getLogger("enterprise_reporting_pipeline")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger