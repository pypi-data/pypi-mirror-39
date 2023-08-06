import json
import unittest


from drongo import Drongo


class TestRequest(unittest.TestCase):
    def setUp(self):
        self.app = Drongo()

    def start_response(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers

    def test_headers(self):
        def sample(ctx):
            ctx.response.set_header('a', 'test')
            ctx.response.set_status('201')

        self.app.add_url('/', 'GET', sample)

        sample_env = dict(
            REQUEST_METHOD='GET',
            GET='',
            PATH_INFO='/'
        )

        self.app(sample_env, self.start_response)
        self.assertIn(('a', 'test'), self.headers)

    def test_content(self):
        def sample(ctx):
            ctx.response.set_content(b'Hello world', 11)

        self.app.add_url('/', 'GET', sample)

        sample_env = dict(
            REQUEST_METHOD='GET',
            GET='',
            PATH_INFO='/'
        )

        resp = self.app(sample_env, self.start_response)
        self.assertIn(b'Hello world', resp)

    def test_cookie(self):
        def sample(ctx):
            ctx.response.set_cookie('a', 'test', 'localhost', secure=True)
            return [b'Hello']

        self.app.add_url('/', 'GET', sample)

        sample_env = dict(
            REQUEST_METHOD='GET',
            GET='',
            PATH_INFO='/'
        )

        self.app(sample_env, self.start_response)
        headers = list(map(
            lambda a: (a[0].lower(), a[1].lower()),
            self.headers
        ))
        self.assertIn(
            (
                'set-cookie',
                'a=test; Domain=localhost; HttpOnly; Path=/; Secure'.lower()
            ), headers)

    def test_redirect(self):
        def sample(ctx):
            ctx.response.set_redirect(url='/hello')
            return []

        self.app.add_url('/', 'GET', sample)

        sample_env = dict(
            REQUEST_METHOD='GET',
            GET='',
            PATH_INFO='/'
        )

        self.app(sample_env, self.start_response)
        self.assertIn(('location', '/hello'), self.headers)

    def test_json(self):
        def sample(ctx):
            ctx.response.set_json({'hello': 'world'})

        self.app.add_url('/', 'GET', sample)

        sample_env = dict(
            REQUEST_METHOD='GET',
            GET='',
            PATH_INFO='/'
        )

        resp = self.app(sample_env, self.start_response)
        resp = json.loads(resp[0].decode('utf8'))
        self.assertEqual({'hello': 'world'}, resp)
