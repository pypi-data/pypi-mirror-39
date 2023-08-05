# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
# 
# Created on 06.11.2017
#
"""
@author: rs
"""

import logging
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self._logger = logging.getLogger(__name__)

    def testLogger(self):
        self._logger.info("Log test with info {}".format("hi there"))
        self._logger.error("Log test with error {}".format("hi there"))
        self._logger.warning("Log test with warning {}".format("hi there"))
        self._logger.debug("Log test with debug {}".format("hi there"))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()