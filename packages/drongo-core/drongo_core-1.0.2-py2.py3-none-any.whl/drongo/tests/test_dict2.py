import unittest

from drongo.utils import dict2


class TestDict2(unittest.TestCase):
    def test_conversion(self):
        obj = {
            'a': 100,
            'b': 'Hello',
            'c': [
                {'a': 3.14},
                'World'
            ],
            'd': {
                'a': ['test'],
                'b': {'a': 6.28, 'b': [1, 2]}
            }
        }

        obj2 = dict2.from_dict(obj).to_dict()
        self.assertEqual(obj, obj2)

        obj2 = dict2.from_dict(obj)
        obj2 = dict2.from_dict(obj2)
        self.assertEqual(obj, obj2)

    def test_set_get(self):
        obj = dict2()
        obj.a = 100
        self.assertEqual(obj.a, 100)

        obj.b.c = 3.14
        self.assertEqual(obj.b, {'c': 3.14})

        self.assertEqual(obj.get_property('b.c'), 3.14)
        self.assertEqual(obj.get_property('b.a'), None)

        obj.c = {'hello': 'world'}
        self.assertEqual(obj.c.hello, 'world')

    def test_update(self):
        obj = {
            'a': 100,
            'b': 'Hello',
            'c': [
                {'a': 3.14},
                'World'
            ],
            'd': {
                'a': ['test'],
                'b': {'a': 6.28, 'b': [1, 2]}
            }
        }

        obj2 = dict2(d={})
        obj2.update(obj)
        self.assertEqual(obj, obj2)

    def test_dummy(self):
        obj = dict2()
        self.assertIn('dict2', repr(obj))
