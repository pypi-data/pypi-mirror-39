#!/usr/bin/env python
import sys

from comet_ml.config import get_config
from comet_ml.comet import get_api_key
from comet_ml.offline import OfflineSender, unzip_offline_archive


def upload(offline_archive_path):
    unzipped_directory = unzip_offline_archive(offline_archive_path)
    config = get_config()
    api_key = get_api_key(None, config)
    sender = OfflineSender(api_key, unzipped_directory)
    sender.send()
    sender.close()


def main():
    upload(sys.argv[1])


if __name__ == "__main__":
    upload(sys.argv[1])
