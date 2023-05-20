import unittest
from unittest.mock import patch, MagicMock, call
import json

import dns

from main import DomainChecker


class TestDomainChecker(unittest.TestCase):
    def setUp(self):
        self.sources = ["https://gist.githubusercontent.com/groundcat/6f58b8d66eff3288fc4b745a55d4b437/raw/5a61ede3461774a6a2c7d74a13696e8cf7b7dfa5/domains.json",
                        "https://gist.githubusercontent.com/groundcat/6f58b8d66eff3288fc4b745a55d4b437/raw/5a61ede3461774a6a2c7d74a13696e8cf7b7dfa5/domains.txt"]
        self.domains = ["temp-mail.org", "10mail.org"]
        self.dummy_json_domains = json.dumps(["33mail.com", "567map.xyz"])
        self.checker = DomainChecker(self.sources)

    @patch('requests.get')
    def test_fetch_domains(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '\n'.join(self.domains)
        mock_get.return_value = mock_response

        self.checker.fetch_domains()

        # Verify if domains were added correctly
        self.assertEqual(self.checker.domains, set(self.domains))

    @patch.object(dns.resolver.Resolver, 'resolve')
    def test_check_mx_record(self, mock_resolve):
        # Mock the behavior of dns.resolver.Resolver.resolve
        mock_resolve.return_value = [MagicMock()]

        # Test if the method returns True when there are MX records
        self.assertTrue(self.checker.check_mx_record('temp-mail.org', '1.1.1.1'))

        # Test if the method returns False when there are no MX records
        mock_resolve.return_value = []
        self.assertFalse(self.checker.check_mx_record('invalid-domain-138729817.com', '8.8.8.8'))

    @patch.object(DomainChecker, 'check_mx_record')
    @patch('concurrent.futures.ThreadPoolExecutor.submit')
    def test_filter_domains(self, mock_submit, mock_check_mx):
        # Mock the behavior of ThreadPoolExecutor.submit and check_mx_record
        mock_submit.return_value.result.return_value = True
        mock_check_mx.return_value = True

        self.checker.domains = set(self.domains)
        self.checker.filter_domains()

        # Verify if all domains have been validated and added to valid_domains
        self.assertEqual(self.checker.domains, self.checker.valid_domains)

    @patch('builtins.open')
    @patch('logging.info')
    def test_write_domains(self, mock_log, mock_open):
        # Mock the behavior of open and logging.info
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        self.checker.valid_domains = set(self.domains)
        self.checker.write_domains()

        # Verify if all domains have been written to the file
        calls = [call.write(f"{domain}\n") for domain in self.checker.valid_domains]
        mock_file.assert_has_calls(calls, any_order=True)

        # Verify if the log written contains "Completed"
        mock_log.assert_called_with("Complete. In total 2 valid domains written to domains.txt")

if __name__ == "__main__":
    unittest.main()
