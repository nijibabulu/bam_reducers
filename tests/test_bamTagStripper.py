from unittest import TestCase
from util import filter_result
import bamreducers


class TestBamTagStripper(TestCase):
    def test_filter_alignment(self):
        self.assertEqual(filter_result(bamreducers.BamTagStripper()),
                         '69d15ae036602b7198ca6167a48d32e9')





