from unittest import TestCase
from util import filter_result
import bamreducers

class TestSJValidator(TestCase):
    def test_filter_alignment(self):
        self.assertEqual(filter_result(bamreducers.SJValidator()),
                         '13549a87a6ddd18e6e1dce6788372124')
