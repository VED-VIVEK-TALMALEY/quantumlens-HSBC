# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import logging
import os

LOG_DIR = "logs"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            "logs/quantumlens.log",
            encoding="utf-8"
        ),

        logging.StreamHandler()
    ]
)

logger = logging.getLogger(
    "QuantumLens"
)