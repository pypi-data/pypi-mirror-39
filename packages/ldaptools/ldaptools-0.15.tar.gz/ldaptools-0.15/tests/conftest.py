import pytest
import tempfile
import os
import random

from ldaptools.slapd import Slapd

base_path = os.path.dirname(__file__)
key_file = os.path.join(base_path, 'ssl-cert-snakeoil.key')
certificate_file = os.path.join(base_path, 'ssl-cert-snakeoil.pem')


@pytest.fixture
def slapd(request):
    with Slapd(ldap_url=getattr(request, 'param', None)) as s:
        yield s


@pytest.fixture
def slapd_tcp1(request):
    port = 4389
    with Slapd(ldap_url='ldap://localhost:%s' % port) as s:
        yield s


@pytest.fixture
def slapd_tcp2(request):
    port = 5389
    with Slapd(ldap_url='ldap://localhost:%s' % port) as s:
        yield s


@pytest.fixture
def slapd_ssl(request):
    port = 6389
    with Slapd(ldap_url='ldaps://localhost:%s' % port, tls=(key_file, certificate_file)) as s:
        yield s


@pytest.fixture
def slapd_tls(request):
    port = 7389
    with Slapd(ldap_url='ldap://localhost:%s' % port, tls=(key_file, certificate_file)) as s:
        yield s


@pytest.fixture(params=['slapd_tcp1', 'slapd_ssl', 'slapd_tls'])
def any_slapd(request, slapd_tcp1, slapd_ssl, slapd_tls):
    return vars().get(request.param)


@pytest.fixture
def ldif():
    return '''dn: dc=orga2
o: orga
dc: orga2
objectClass: organization
objectClass: dcObject

dn: uid=admin,dc=orga2
objectClass: inetOrgPerson
cn: John Doe
uid: admin
sn: John
givenName: Doe
mail: john.doe@entrouvert.com

'''


@pytest.fixture
def attributes():
    return ['o', 'objectClass', 'uid', 'sn', 'givenName', 'mail', 'dc', 'cn']


@pytest.fixture
def pivot_attributes():
    return (
        ('organization', 'o'),
        ('inetOrgPerson', 'uid'),
    )


@pytest.fixture
def ldif_path(request, ldif):
    handle, path = tempfile.mkstemp()
    with open(path, 'w') as f:
        f.write(ldif)
        f.flush()
    def finalize():
        os.unlink(path)
    request.addfinalizer(finalize)
    return path


@pytest.fixture
def attributes_path(request, attributes):
    handle, path = tempfile.mkstemp()
    with open(path, 'w') as f:
        for attribute in attributes:
            print >>f, ' %s ' % attribute
        f.flush()
    def finalize():
        os.unlink(path)
    request.addfinalizer(finalize)
    return path
