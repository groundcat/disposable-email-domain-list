import requests
import json
import logging
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import os
from collections import deque

logging.basicConfig(format='%(asctime)s %(message)s', filename="validation.log", level=logging.INFO)


class DomainChecker:
    def __init__(self, sources):
        self.sources = sources
        self.domains = set()
        self.valid_domains = set()
        self.dns_servers = ["1.1.1.1", "8.8.8.8", "8.8.4.4", "1.0.0.1", "9.9.9.9"]
        self.allowlist = set()

    def fetch_domains(self):
        for source in self.sources:
            try:
                response = requests.get(source)
                if response.status_code == 200:
                    content = response.text.strip()
                    if source.endswith('.json'):
                        domains = json.loads(content)
                    else:
                        domains = content.splitlines()
                    self.domains.update(domains)
                    logging.info(f"Successfully fetched {len(domains)} domains from {source} ")
                else:
                    logging.info(f"{response.status_code} - Could not fetch data from {source}")
            except Exception as e:
                logging.info(f"Exception occurred while fetching data from {source}: {str(e)}")

    def fetch_allowlist(self):
        try:
            with open('allowlist.txt', 'r') as f:
                self.allowlist = set(f.read().splitlines())
        except Exception as e:
            logging.info(f"Exception occurred while reading the allowlist: {str(e)}")

    def check_mx_record(self, domain, server):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [server]
        try:
            mx_records = resolver.resolve(domain, 'MX')
            if mx_records:
                return True
        except:
            return False

    def filter_domains(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for i, domain in enumerate(self.domains):
                server = self.dns_servers[i % 5]
                if executor.submit(self.check_mx_record, domain, server).result():
                    self.valid_domains.add(domain)

    def exclude_allowlisted_domains(self):
        self.valid_domains -= self.allowlist

    def write_domains(self):
        with open('domains.txt', 'w') as f:
            for domain in self.valid_domains:
                f.write(f"{domain}\n")
        logging.info(f"Complete. In total {len(self.valid_domains)} valid domains written to domains.txt")

    def write_domains_json(self):
        with open('domains.json', 'w') as f:
            json.dump(list(self.valid_domains), f)
        logging.info(f"Complete. In total {len(self.valid_domains)} valid domains written to domains.json")

    def prune_log(self):
        try:
            with open('validation.log', 'r') as f:
                lines = deque(f, 50)
            with open('validation.log', 'w') as f:
                f.writelines(lines)
        except FileNotFoundError:
            logging.info("validation.log file not found")

    def run(self):
        self.fetch_domains()
        self.fetch_allowlist()
        self.filter_domains()
        self.exclude_allowlisted_domains()
        self.write_domains()
        self.write_domains_json()
        self.prune_log()


if __name__ == "__main__":

    sources = []
    with open('sources.txt', 'r') as f:
        for line in f:
            sources.append(line.strip())

    checker = DomainChecker(sources)
    checker.run()
