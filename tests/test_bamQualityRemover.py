from unittest import TestCase
from util import filter_result
import bamreducers

class TestBamQualityRemover(TestCase):
    def test_filter_alignment(self):
        self.assertEqual(filter_result(bamreducers.BamQualityRemover()),
                         'c00396b1fb571850aabe0f8013c124bb')
