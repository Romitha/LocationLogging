from __future__ import unicode_literals

import datetime
# import built-in validators
import logging
import os

from flask import send_file

log = logging.getLogger('BIONS')


class LoggerModel:

    @classmethod
    def createLogDetails(cls, device_id, room_no):
        text = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S") + "|"+device_id+"|"+room_no
        log.info(text)
        # log.warning('A warning occurred (%d apples)', 42)
        # log.error('An error occurred')
        # log.info('Info')

    @classmethod
    def DownloadLogFile(cls, path=None):
        if path is None:
            path = os.path.abspath('info.log')
        try:
            return send_file(path, as_attachment=True)
        except Exception as e:
            print(e)
