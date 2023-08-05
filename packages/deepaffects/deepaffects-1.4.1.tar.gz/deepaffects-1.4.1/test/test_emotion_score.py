# coding: utf-8

"""
    DeepAffects

    OpenAPI Specification of DeepAffects APIs

    OpenAPI spec version: v1
"""


from __future__ import absolute_import

import os
import sys
import unittest

import deepaffects
from deepaffects.rest import ApiException
from deepaffects.models.emotion_score import EmotionScore


class TestEmotionScore(unittest.TestCase):
    """ EmotionScore unit test stubs """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEmotionScore(self):
        """
        Test EmotionScore
        """
        model = deepaffects.models.emotion_score.EmotionScore()


if __name__ == '__main__':
    unittest.main()
