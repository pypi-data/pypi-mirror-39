"""
This module assumes that OpenCanary has been installed and is running with the
default settings.

In particular it assumes that OpenCanary is logging to /var/tmp/opencanary.log

It would be much better to setup tests to start the services needed and provide
the configuration files so that tests can be run witout needing to reinstall
and start the service before each test. It would also be better to be able to
test the code directly rather than relying on the out put of loggs.

Still this is a start.
"""

import time
import json
from ftplib import FTP, error_perm
import unittest
import socket

# These libraries are only needed by the test suite and so aren't in the
# OpenCanary requirements, there is a requirements.txt file in the tests folder
# Simply run `pip install -r opencanary/test/requirements.txt`
import requests
import paramiko
import pymysql


def get_last_log():
    """
    Gets the last line from `/var/tmp/opencanary.log` as a dictionary
    """
    with open('/var/tmp/opencanary.log', 'r') as log_file:
        return json.loads(log_file.readlines()[-1])


class TestFTPModule(unittest.TestCase):
    """
    Tests the cases for the FTP module.

    The FTP server should not allow logins and should log each attempt.
    """
    def setUp(self):
        self.ftp = FTP('localhost')

    def test_anonymous_ftp(self):
        """
        Try to connect to the FTP service with no username or password.
        """
        self.assertRaises(error_perm, self.ftp.login)
        log = get_last_log()
        self.assertEqual(log['dst_port'], 21)
        self.assertEqual(log['logdata']['USERNAME'], "anonymous")
        self.assertEqual(log['logdata']['PASSWORD'], "anonymous@")

    def test_authenticated_ftp(self):
        """
        Connect to the FTP service with a test username and password.
        """
        self.assertRaises(error_perm,
                          self.ftp.login,
                          user='test_user',
                          passwd='test_pass')
        last_log = get_last_log()
        self.assertEqual(last_log['dst_port'], 21)
        self.assertEqual(last_log['logdata']['USERNAME'], "test_user")
        self.assertEqual(last_log['logdata']['PASSWORD'], "test_pass")

    def tearDown(self):
        self.ftp.close()


class TestHTTPModule(unittest.TestCase):
    """
    Tests the cases for the HTTP module.

    The HTTP server should look like a NAS and present a login box, any
    interaction with the server (GET, POST) should be logged.
    """
    def test_get_http_home_page(self):
        """
        Simply get the home page.
        """
        request = requests.get('http://localhost/')
        self.assertEqual(request.status_code, 200)
        self.assertIn('Synology RackStation', request.text)
        last_log = get_last_log()
        self.assertEqual(last_log['dst_port'], 80)
        self.assertEqual(last_log['logdata']['HOSTNAME'], "localhost")
        self.assertEqual(last_log['logdata']['PATH'], "/index.html")
        self.assertIn('python-requests', last_log['logdata']['USERAGENT'])

    def test_log_in_to_http_with_basic_auth(self):
        """
        Try to log into the site with basic auth.
        """
        request = requests.post('http://localhost/', auth=('user', 'pass'))
        # Currently the web server returns 200, but in future it should return
        # a 403 statuse code.
        self.assertEqual(request.status_code, 200)
        self.assertIn('Synology RackStation', request.text)
        last_log = get_last_log()
        self.assertEqual(last_log['dst_port'], 80)
        self.assertEqual(last_log['logdata']['HOSTNAME'], "localhost")
        self.assertEqual(last_log['logdata']['PATH'], "/index.html")
        self.assertIn('python-requests', last_log['logdata']['USERAGENT'])
        # OpenCanary doesn't currently record credentials from basic auth.

    def test_log_in_to_http_with_parameters(self):
        """
        Try to log into the site by posting the parameters
        """
        login_data = {
            'username': 'test_user',
            'password': 'test_pass',
            'OTPcode': '',
            'rememberme': '',
            '__cIpHeRtExt': '',
            'isIframeLogin': 'yes'}
        request = requests.post('http://localhost/index.html', data=login_data)
        # Currently the web server returns 200, but in future it should return
        # a 403 statuse code.
        self.assertEqual(request.status_code, 200)
        self.assertIn('Synology RackStation', request.text)
        last_log = get_last_log()
        self.assertEqual(last_log['dst_port'], 80)
        self.assertEqual(last_log['logdata']['HOSTNAME'], "localhost")
        self.assertEqual(last_log['logdata']['PATH'], "/index.html")
        self.assertIn('python-requests', last_log['logdata']['USERAGENT'])
        self.assertEqual(last_log['logdata']['USERNAME'], "test_user")
        self.assertEqual(last_log['logdata']['PASSWORD'], "test_pass")


class TestSSHModule(unittest.TestCase):
    """
    Tests the cases for the SSH server
    """
    def setUp(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def test_ssh_with_basic_login(self):
        """
        Try to log into the SSH server
        """
        self.assertRaises(paramiko.ssh_exception.AuthenticationException,
                          self.connection.connect,
                          hostname="localhost",
                          port=8022,
                          username="test_user",
                          password="test_pass")
        last_log = get_last_log()
        self.assertEqual(last_log['dst_port'], 8022)
        self.assertIn('paramiko', last_log['logdata']['REMOTEVERSION'])
        self.assertEqual(last_log['logdata']['USERNAME'], "test_user")
        self.assertEqual(last_log['logdata']['PASSWORD'], "test_pass")

    def tearDown(self):
        self.connection.close()


class TestNTPModule(unittest.TestCase):
    """
    Tests the NTP server. The server doesn't respond, but it will log attempts
    to trigger the MON_GETLIST_1 NTP commands, which is used for DDOS attacks.
    """
    def setUp(self):
        packet = (
            b'\x17' +  # response more version mode
            b'\x00' +  # sequence number
            b'\x03' +  # implementation (NTPv3)
            b'\x2a' +  # request (MON_GETLIST_1)
            b'\x00' +  # error number / number of data items
            b'\x00' +  # item_size
            b'\x00'    # data
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto(packet, ('localhost', 123))

    def test_ntp_server_monlist(self):
        """
        Check that the MON_GETLIST_1 NTP command was logged correctly
        """
        # The logs take about a second to show up, in other tests this is not
        # an issue, because there are checks that run before looking at the log
        # (e.g. request.status_code == 200 for HTTP) but for NTP we just check
        # the log. A hardcoded time out is a horible solution, but it works.
        time.sleep(1)

        last_log = get_last_log()
        self.assertEqual(last_log['logdata']['NTP CMD'], "monlist")
        self.assertEqual(last_log['dst_port'], 123)

    def tearDown(self):
        self.sock.close()


class TestMySQLModule(unittest.TestCase):
    """
    Tests the MySQL Server attempting to login should fail and
    """

    def test_mysql_server_login(self):
        """
        Login to the mysql server
        """
        self.assertRaises(pymysql.err.OperationalError,
                          pymysql.connect,
                          host="localhost",
                          user="test_user",
                          password="test_pass",
                          db='db',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
        last_log = get_last_log()
        self.assertEqual(last_log['logdata']['USERNAME'], "test_user")
        self.assertEqual(last_log['logdata']['PASSWORD'],
                         "b2e5ed6a0e59f99327399ced2009338d5c0fe237")
        self.assertEqual(last_log['dst_port'], 3306)


if __name__ == '__main__':
    unittest.main()
