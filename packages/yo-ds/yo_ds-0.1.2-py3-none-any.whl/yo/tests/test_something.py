from unittest import TestCase

import yo

class TestYo(TestCase):
    def test_something(self):
        self.assertListEqual([1,2,3],list(yo.Query().get()))