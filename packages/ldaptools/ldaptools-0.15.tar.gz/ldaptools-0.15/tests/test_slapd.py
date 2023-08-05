import pytest

import ldap


@pytest.mark.parametrize('slapd', [None, 'ldap://localhost:1389'], indirect=True)
def test_checkpoint(slapd):
    conn = slapd.get_connection()
    conn.simple_bind_s('uid=admin,cn=config', 'admin')
    assert conn.whoami_s() == 'dn:uid=admin,cn=config'
    slapd.stop()
    slapd.checkpoint()
    slapd.start()
    slapd.add_ldif('''dn: uid=admin,o=orga
objectclass: person
objectclass: uidObject
uid:in
cn: n
sn: n

''')
    conn = slapd.get_connection()
    assert len(conn.search_s('o=orga', ldap.SCOPE_SUBTREE)) == 2
    slapd.stop()
    slapd.restore()
    slapd.start()
    conn = slapd.get_connection()
    assert len(conn.search_s('o=orga', ldap.SCOPE_SUBTREE)) == 1


def test_any(any_slapd):
    conn = any_slapd.get_connection()
    conn.simple_bind_s('uid=admin,cn=config', 'admin')


def test_ssl_client_cert(slapd_ssl):
    conn = slapd_ssl.get_connection_admin()
    conn.modify_s('cn=config', [
        (ldap.MOD_ADD, 'olcTLSCACertificateFile', slapd_ssl.tls[1]),
        (ldap.MOD_ADD, 'olcTLSVerifyClient', 'demand'),
    ])

    with pytest.raises((ldap.SERVER_DOWN, ldap.CONNECT_ERROR)):
        conn = slapd_ssl.get_connection()
        conn.whoami_s()

    conn = slapd_ssl.get_connection(tls=slapd_ssl.tls)
    conn.whoami_s()


def test_tls_client_cert(slapd_tls):
    test_ssl_client_cert(slapd_tls)
