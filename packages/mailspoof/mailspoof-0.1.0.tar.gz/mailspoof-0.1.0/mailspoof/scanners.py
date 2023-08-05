"""
`mailspoof` provides callable classes for checking SPF and DMARC records for
common issues.
"""

import os
import re
import dns.resolver
import tldextract
import requests

from .issues import ISSUES


WHOAPI_URL = 'https://api.whoapi.com/?domain={domain}&r=taken&apikey={key}'

if 'WHOAPI_KEY' in os.environ:
    WHOAPI_KEY = os.environ['WHOAPI_KEY']
else:
    WHOAPI_KEY = None


class SPFScan():
    """
    A callable for extracting SPF security fails for a domain. Returns an
    SPFResult
    """

    def __init__(self, whoapi_key=None):
        self.fetch = TXTFetch('v=spf1 ')
        self.whoapi_key = whoapi_key

    def __call__(self, domain):
        """
        Returns a list of dictionaries ("issues") highlighting security
        concerns with the SPF record.
        """

        try:
            spf_record = self.fetch(domain)
        except ValueError:
            return [ISSUES['NO_SPF']]
        except dns.resolver.NXDOMAIN:
            issue = dict(ISSUES['NX_DOMAIN'])
            issue['detail'] = issue['detail'].format(domain=domain)
            return [issue]

        issues = []
        terms = spf_record.split(' ')

        # check the 'all' mechanism
        all_qualifier = None
        all_match = re.match(r'^([-?~+])all$', terms[-1])
        if all_match:
            all_qualifier = all_match.group(1)

        if not all_qualifier:
            issues.append(ISSUES['SPF_NO_ALL'])
        elif all_qualifier == '+':
            issues.append(ISSUES['SPF_PASS_ALL'])
        elif all_qualifier == '~':
            issues.append(ISSUES['SPF_SOFT_FAIL_ALL'])

        # recursively count the number of lookups and get the domains used
        included_domains, nb_lookups = self._get_include_domains(domain)

        if nb_lookups > 10:
            issues.append(ISSUES['SPF_LOOKUP_ERROR'])

        # check for any free domains
        free_domains = set()
        if self.whoapi_key:
            for included_domain in included_domains:
                if not self._domain_taken(included_domain):
                    free_domains.add(included_domain)

        if free_domains:
            issue = dict(ISSUES['SPF_UNREGISTERED_DOMAINS'])
            issue['detail'] = issue['detail'].format(domains=', '.join(
                list(free_domains)))
            issues.append(issue)

        return issues

    def _get_include_domains(self, domain):
        """
        Recursively goes through the domain's SPF record and included SPF
        records. Returns a tuple of the root domains encountered and
        Recursively count the number of DNS lookups needed for a recipient to
        validate the SPF record
        """

        domains = set()
        nb_lookups = 0

        def _recurse(domain):
            nonlocal nb_lookups
            nonlocal domains

            try:
                spf_record = self.fetch(domain)
            except ValueError:
                return
            except dns.resolver.NXDOMAIN:
                return

            terms = spf_record.split(' ')
            includes = []

            for term in terms:
                if ':' not in term:
                    continue

                mechanism, value = term.split(':', 1)

                if mechanism == 'include':
                    nb_lookups += 1
                    includes.append(value)
                    domains.add(self._get_registered_domain(value))
                elif mechanism in ['a', 'mx']:
                    nb_lookups += 1
                    domains.add(self._get_registered_domain(value))
                elif mechanism in ['ptr', 'exists', 'redirect']:
                    nb_lookups += 1

            for include in includes:
                _recurse(include)

        _recurse(domain)

        return domains, nb_lookups

    def _domain_taken(self, domain):
        """
        Returns True if the domain is already registered. False means the
        domain is open for registration and could be registered by an attacker.
        """
        response = requests.get(WHOAPI_URL.format(domain=domain,
                                                  key=self.whoapi_key))
        data = response.json()
        if data['status'] != '0':
            raise Exception(data['status_desc'])
        return True if data['taken'] else False

    @staticmethod
    def _get_registered_domain(domain):
        """
        Returns the "registered domain" from a given (sub)domain.

        >>> _get_registered_domain('foo.bar.com')
        bar.com
        """
        parsed_domain = tldextract.extract(domain)
        return '.'.join([parsed_domain.domain, parsed_domain.suffix])


class DMARCScan():
    """
    Callable that return a list of dictionaries ("issues") highlighting
    security concerns with the DMARC record.
    """

    def __init__(self):
        self.fetch = TXTFetch('v=DMARC1; ')

    def __call__(self, domain):
        """
        Returns a list of Issues highlighting potential security issues with
        the DMARC record.
        """

        dmarc_domain = f'_dmarc.{domain}'

        try:
            dmarc_record = self.fetch(dmarc_domain)
        except ValueError:
            return [ISSUES['NO_DMARC']]
        except dns.resolver.NXDOMAIN:
            return [ISSUES['NO_DMARC']]

        issues = []
        terms = [term.strip(' ') for term in dmarc_record.split(';')]

        for term in terms:
            if '=' not in term:
                continue

            tag, value = term.split('=')

            if tag == 'p' and value not in ['quarantine', 'reject']:
                issue = dict(ISSUES['DMARC_LAX_POLICY'])
                issue['detail'] = issue['detail'].format(policy=value)
                issues.append(issue)
            elif tag == 'sp' and value not in ['quarantine', 'reject']:
                # default for 'sp' if not present is the same as 'p'
                issue = dict(ISSUES['DMARC_LAX_SUBDOMAIN_POLICY'])
                issue['detail'] = issue['detail'].format(policy=value)
                issues.append(issue)
            elif tag == 'pct' and int(value) < 100:
                # default for 'pct' if not present is '100'
                issue = dict(ISSUES['DMARC_NOT_100_PCT'])
                issue['detail'] = issue['detail'].format(pct=value)
                issues.append(issue)

        return issues


class TXTFetch():
    """
    A callable for fetching a DNS TXT record with a certain prefix for a
    given domain.
    """

    def __init__(self, txt_prefix, timeout=5, lifetime=5):
        # txt_prefix should be `v=DMARC1; ` or `v=spf1 `
        self.txt_prefix = txt_prefix
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = lifetime

    def __call__(self, domain):
        """
        Fetches a DNS TXT record with a certain prefix for a given domain.
        """
        txt_records = self.resolver.query(domain, 'TXT')
        for txt_record in txt_records:
            value = str(txt_record).strip('"')
            if value.startswith(self.txt_prefix):
                return value
        raise ValueError(f'No record with prefix {self.txt_prefix} for domain '
                         '{domain}')


class Scan():
    """
    Callable that return a list of dictionaries ("issues") highlighting
    security concerns with the SPF and DMARC records.
    """

    def __init__(self):
        self.spf_check = SPFScan(WHOAPI_KEY)
        self.dmarc_check = DMARCScan()

    def __call__(self, domain):
        """
        Returns a list of Issues highlighting potential security issues with
        the SPF and DMARC records.
        """
        return self.spf_check(domain) + self.dmarc_check(domain)
