# Copyright (c) 2023 Chang Xiao
# SPDX-License-Identifier: MIT

import logging
import os

def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Create handlers for each log level
    info_handler = logging.FileHandler('log/info.log', mode='a')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(log_format))

    debug_handler = logging.FileHandler('log/debug.log', mode='a')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter(log_format))

    warning_handler = logging.FileHandler('log/warning.log', mode='a')
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(logging.Formatter(log_format))

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set the root logger's level to the lowest level you want to capture

    # Add the handlers to the root logger
    root_logger.addHandler(info_handler)
    root_logger.addHandler(debug_handler)
    root_logger.addHandler(warning_handler)