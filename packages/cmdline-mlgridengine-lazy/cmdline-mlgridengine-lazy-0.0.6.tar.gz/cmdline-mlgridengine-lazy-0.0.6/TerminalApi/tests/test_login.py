import unittest
import mock
from unittest.mock import Mock, patch
from src.login.login import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.logout.logout import post as logout_post
from src.logout.logout import logout
from src.base_url.base_url import base_url


usr_name = 'no_name'
password = '123456'
remember = True

info = {
    'login': usr_name,
    'password': password,
    'remember': remember
}

res = {
    'profile': {
        'usr_name': usr_name,
        'password': password,
        'remember': remember
    }
}
query_url = '/api/v1/auth/_login'

info_out = {

}

res_out = {

}
query_url_out = '/api/v1/auth/_logout'


class LoginTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(res, 200)
        status_code, response = post(base_url, query_url, info)
        self.assertEqual(mock.call(url + query_url, json=info),
                         mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, res)

        mock_class.return_value = MockResponse(res_out, 200)
        status_code, response = logout_post(base_url, query_url_out, info_out)
        self.assertEqual(mock.call(url + query_url_out, json=info_out),
                         mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, res_out)

    @patch('requests.post')
    def test_response_post_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(res, 404)
        with self.assertRaises(SystemExit) as cm:
            post(base_url, query_url, info)
        self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            logout_post(base_url, query_url_out, info_out)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.login.login.post')
    def test_server_inspect(self, mock_class):
        mock_class.return_value = (200, res)
        runner = CliRunner()
        result = runner.invoke(login, ['--usr-name', usr_name, '--password', password, '--remember', remember])
        output = "usr_name"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('src.logout.logout.post')
    def test_logout(self, mock_class):
        mock_class.return_value = (200, res_out)
        runner = CliRunner()
        result = runner.invoke(logout)
        output = "Logout succeed"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)
