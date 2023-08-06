# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


import logging

from steelscript.appfwk.apps.jobs.task.base import BaseTask

logger = logging.getLogger(__name__)


class SyncTask(BaseTask):
    def start(self):
        self.call_method()
