import unittest
from nowstagram import app


class NowstagramTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self) -> None:
        print('tearDown')

    '''
    def setUpClass(cls) -> None:
        print('setupClass')
    def tearDownClass(cls) -> None:
        print('tearDownClass')
    '''

    def register(self, username, password):
        return self.app.post('/reg/', data={'username': username, 'password': password}, follow_redircts=True)

    def login(self, username, password):
        return self.app.post('/login/', data={'username': username, 'password': password}, follow_redircts=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_logout_login(self):
        assert self.register('hello', 'world').status_code == 200
        assert '-hello' in self.app.open('/').data
        self.logout()
        assert '-hello' not in self.app.open('/').data
        self.login('hello', 'world')
        assert '-hello' in self.app.open('/').data

    def test_profile(self):
        r = self.app.open('/profile/3/', follow_redirects=True)
        assert r.status_code == 200
        assert 'password' in r.data
        self.register('hello2','world')
        assert 'hello2' in self.app.open('/profile/1/', follow_redirects=True)
