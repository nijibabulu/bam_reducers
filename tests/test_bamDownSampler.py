from unittest import TestCase
from util import filter_result
import bamreducers

class TestBamDownSampler(TestCase):
    def test_filter_alignment(self):
        self.assertEqual(
            filter_result(bamreducers.BamDownSampler(5, seed=111)),
            'c5d0e66fbb96f153f4236f43a199d486')
