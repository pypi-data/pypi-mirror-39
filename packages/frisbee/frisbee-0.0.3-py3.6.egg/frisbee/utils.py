#!/usr/bin/env python
import datetime
import logging
import os
import random
import re
import sys
from typing import Dict
from typing import List
from typing import Pattern


def gen_logger(name: str, log_level: int=logging.INFO) -> logging.Logger:
    """Create a logger to be used between processes.

    :returns: Logging instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    shandler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    fmt: str = '\033[1;32m%(levelname)-5s %(module)s:%(funcName)s():'
    fmt += '%(lineno)d %(asctime)s\033[0m| %(message)s'
    shandler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(shandler)
    return logger


def gen_headers() -> Dict[str, str]:
    """Generate a header pairing."""
    ua_list: List[str] = ['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36']
    headers: Dict[str, str] = {'User-Agent': ua_list[random.randint(0, len(ua_list) - 1)]}
    return headers


def str_datetime(stamp: datetime.datetime) -> str:
    """Convert datetime to str format."""
    return stamp.strftime("%Y-%m-%d %H:%M:%S")


def now_time() -> datetime.datetime:
    """Get the current time."""
    return datetime.datetime.now()


def extract_emails(results: str, domain: str) -> List[str]:
    """Grab email addresses from raw text data."""
    pattern: Pattern = re.compile(r'([\w.-]+@[\w.-]+)')
    hits: List[str] = pattern.findall(results)
    emails: List[str] = [x.lower() for x in hits if x.endswith(domain)]
    return list(set(emails))
