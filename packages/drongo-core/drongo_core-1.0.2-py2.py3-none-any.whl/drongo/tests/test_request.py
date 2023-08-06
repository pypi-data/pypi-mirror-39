import unittest


from drongo import Drongo


class TestRequest(unittest.TestCase):
    def setUp(self):
        self.app = Drongo()

    def start_response(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers

    def test_cookie(self):
        sample_env = dict(
            REQUEST_METHOD='GET',
            GET='',
            PATH_INFO='/',
            HTTP_COOKIE='a=test'
        )

        def sample(ctx):
            self.assertEqual(ctx.request.cookies.a, 'test')
            return 'Hello, World!'

        self.app.add_url('/', 'GET', sample)

        self.app(sample_env, self.start_response)
        self.assertIn('200', self.status_code)

    def test_query(self):
        sample_env = dict(
            REQUEST_METHOD='GET',
            GET={'a': ['test']},
            PATH_INFO='/'
        )

        def sample(ctx):
            self.assertEqual(ctx.request.query['a'], ['test'])
            return 'Hello, World!'

        self.app.add_url('/', 'GET', sample)

        self.app(sample_env, self.start_response)
        self.assertIn('200', self.status_code)

    def test_json_body(self):
        sample_env = dict(
            REQUEST_METHOD='GET',
            GET={},
            PATH_INFO='/',
            BODY=b'{"a":"test"}'
        )

        def sample(ctx):
            self.assertEqual(ctx.request.json, {'a': 'test'})
            return 'Hello, World!'

        self.app.add_url('/', 'GET', sample)

        self.app(sample_env, self.start_response)
        self.assertIn('200', self.status_code)
