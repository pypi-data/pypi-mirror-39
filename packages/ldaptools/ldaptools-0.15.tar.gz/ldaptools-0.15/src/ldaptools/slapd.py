import time
import tempfile
import shutil
import subprocess
import os
import ldap
import ldap.modlist
import ldap.sasl
import StringIO
import atexit

from ldaptools.ldif_utils import ListLDIFParser
from ldaptools.paged import PagedLDAPObject

SLAPD_PATH = None
SLAPADD_PATH = None
SLAPD_PATHS = ['/bin', '/usr/bin', '/sbin', '/usr/sbin', '/usr/local/bin', '/usr/local/sbin']


def has_slapd():
    global SLAPD_PATH, SLAPADD_PATH, PATHS
    if not SLAPD_PATH or not SLAPADD_PATH:
        for path in SLAPD_PATHS:
            slapd_path = os.path.join(path, 'slapd')
            if os.path.exists(slapd_path):
                SLAPD_PATH = slapd_path
            slapadd_path = os.path.join(path, 'slapadd')
            if os.path.exists(slapd_path):
                SLAPADD_PATH = slapadd_path
    return not (SLAPD_PATH is None or SLAPADD_PATH is None)


class Slapd(object):
    '''Initiliaze an OpenLDAP server with just one database containing branch
       o=orga and loading the core schema. ACL are very permissive.
    '''
    root_bind_dn = 'uid=admin,cn=config'
    root_bind_password = 'admin'

    config_ldif = '''dn: cn=config
objectClass: olcGlobal
cn: config
olcToolThreads: 1
olcLogLevel: -1
olcLogFile: {slapd_dir}/log
{extra_config}

dn: cn=module{{0}},cn=config
objectClass: olcModuleList
cn: module{{0}}
olcModulePath: /usr/lib/ldap
olcModuleLoad: {{0}}back_hdb
olcModuleLoad: {{1}}back_monitor
olcModuleLoad: {{2}}back_mdb
olcModuleLoad: {{3}}accesslog
olcModuleLoad: {{4}}unique
olcModuleLoad: {{5}}refint
olcModuleLoad: {{6}}constraint
olcModuleLoad: {{7}}syncprov

dn: cn=schema,cn=config
objectClass: olcSchemaConfig
cn: schema

dn: olcDatabase={{-1}}frontend,cn=config
objectClass: olcDatabaseConfig
objectClass: olcFrontendConfig
olcDatabase: {{-1}}frontend
olcAccess: {{0}}to *
   by dn.exact=gidNumber={gid}+uidNumber={uid},cn=peercred,cn=external,cn=auth manage
   by * break
olcAccess: {{1}}to dn.exact="" by * read
olcAccess: {{2}}to dn.base="cn=Subschema" by * read
olcSizeLimit: unlimited
olcTimeLimit: unlimited

dn: olcDatabase={{0}}config,cn=config
objectClass: olcDatabaseConfig
olcDatabase: {{0}}config
olcRootDN: uid=admin,cn=config
olcRootPW: admin
olcAccess: {{0}}to *
   by dn.exact=gidNumber={gid}+uidNumber={uid},cn=peercred,cn=external,cn=auth manage
   by * break

'''
    process = None
    schemas = ['core', 'cosine', 'inetorgperson', 'nis', 'eduorg-200210-openldap', 'eduperson',
               'supann-2009']
    schemas_ldif = [open(os.path.join(os.path.dirname(__file__),
                                      'schemas', '%s.ldif' % schema)).read() for schema in schemas]
    checkpoints = None
    data_dirs = None
    db_index = 1
    tls = None

    def create_process(self, args, pipe=True, out=None):
        if pipe:
            return subprocess.Popen(args, stdin=subprocess.PIPE, env=os.environ,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            DEVNULL = open(os.devnull, 'w')
            out = out or DEVNULL
            return subprocess.Popen(args, stdin=DEVNULL, env=os.environ, stdout=out,
                                    stderr=out)

    def __init__(self, ldap_url=None, config_context=None, tls=None):
        assert has_slapd()
        self.checkpoints = []
        self.data_dirs = []
        self.slapd_dir = tempfile.mkdtemp(prefix='slapd-server')
        self.config_dir = os.path.join(self.slapd_dir, 'slapd.d')
        os.mkdir(self.config_dir)
        self.socket = os.path.join(self.slapd_dir, 'socket')
        if not ldap_url:
            ldap_url = 'ldapi://%s' % self.socket.replace('/', '%2F')
        self.ldap_url = ldap_url
        config_context = config_context or {}
        extra_config = ''
        if tls:
            key_file, certificate_file = tls
            real_key = os.path.join(self.slapd_dir, 'key.pem')
            real_cert = os.path.join(self.slapd_dir, 'cert.pem')
            with open(real_key, 'w') as f, open(key_file) as g:
                f.write(g.read())
            with open(real_cert, 'w') as f, open(certificate_file) as g:
                f.write(g.read())
            self.tls = real_key, real_cert

            extra_config += 'olcTLSCertificateKeyFile: %s\n' % real_key
            extra_config += 'olcTLSCertificateFile: %s\n' % real_cert
            extra_config += 'olcSecurity: ssf=1\n'
        config_context.update({
            'slapd_dir': self.slapd_dir,
            'gid': os.getgid(),
            'uid': os.getuid(),
            'extra_config': extra_config,
        })
        self.slapadd(self.config_ldif, context=config_context)
        for schema_ldif in self.schemas_ldif:
            self.slapadd(schema_ldif)
        self.start()
        self.add_db('o=orga')
        ldif = '''dn: o=orga
objectClass: organization
o: orga

'''
        self.add_ldif(ldif)

    def add_db(self, suffix):
        path = os.path.join(self.slapd_dir, suffix)
        os.mkdir(path)
        ldif = '''dn: olcDatabase={{{index}}}mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: mdb
olcSuffix: {suffix}
olcDbDirectory: {path}
olcReadOnly: FALSE
# Index
olcAccess: {{0}}to * by * manage

'''
        self.add_ldif(ldif, context={'index': self.db_index, 'suffix': suffix, 'path': path})
        self.db_index += 1
        self.data_dirs.append(path)

    def slapadd(self, ldif, db=0, context=None):
        assert not self.process

        if context:
            ldif = ldif.format(**context)
        slapadd = self.create_process([SLAPADD_PATH, '-v', '-n%d' % db, '-F', self.config_dir])
        stdout, stderr = slapadd.communicate(input=ldif)
        assert slapadd.returncode == 0, 'slapadd failed: %s' % stderr

    def start(self):
        '''Launch slapd'''
        assert not self.process

        cmd = [SLAPD_PATH,
               '-d768',  # put slapd in foreground
               '-F' + self.config_dir,
               '-h', self.ldap_url]
        out_file = open(os.path.join(self.slapd_dir, 'stdout'), 'w')
        self.process = self.create_process(cmd, pipe=False, out=out_file)
        atexit.register(self.clean)

        c = 0
        while True:
            c += 1
            try:
                conn = self.get_connection()
                conn.whoami_s()
            except ldap.SERVER_DOWN as e:
                if c > 100:
                    raise
                time.sleep(0.1)
            else:
                break

    def stop(self):
        '''Send SIGTERM to slapd'''
        assert self.process

        process = self.process
        process.kill()
        process.wait()

        while True:
            try:
                conn = self.get_connection()
                conn.whoami_s()
            except ldap.SERVER_DOWN:
                break
            else:
                time.sleep(0.1)
        self.process = None

    def checkpoint(self):
        '''Stop slapd and save current data state'''
        assert not self.process

        self.checkpoints.append(
            os.path.join(self.slapd_dir, 'checkpoint-%d' % len(self.checkpoints)))
        for data_dir in self.data_dirs:
            dirname = os.path.basename(data_dir)
            target = os.path.join(self.checkpoints[-1], dirname)
            shutil.copytree(data_dir, target)

    def restore(self):
        '''Stop slapd and restore last data state'''
        assert not self.process
        assert self.checkpoints, 'no checkpoint exists'
        for data_dir in self.data_dirs:
            dirname = os.path.basename(data_dir)
            shutil.rmtree(data_dir)
            shutil.copytree(os.path.join(self.checkpoints[-1], dirname), data_dir)
            shutil.rmtree(self.checkpoints[-1])
            self.checkpoints.pop()

    # Clean behind us
    def __del__(self):
        self.clean()

    def clean(self):
        '''Remove directory'''
        try:
            if self.process:
                self.stop()
        finally:
            if self.slapd_dir:
                if os.path.exists(self.slapd_dir):
                    shutil.rmtree(self.slapd_dir, ignore_errors=True)
                    self.slapd_dir = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.clean()

    def add_ldif(self, ldif, context=None):
        assert self.process

        if context:
            ldif = ldif.format(**context)
        parser = ListLDIFParser(StringIO.StringIO(ldif))
        parser.parse()
        conn = self.get_connection_admin()
        parser.add(conn)

    def get_connection(self, tls=None):
        assert self.process
        conn = PagedLDAPObject(self.ldap_url)
        if tls:
            conn.set_option(ldap.OPT_X_TLS_KEYFILE, tls[0])
            conn.set_option(ldap.OPT_X_TLS_CERTFILE, tls[1])
        if self.tls:
            conn.set_option(ldap.OPT_X_TLS_CACERTFILE, self.tls[1])
            conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
            if not self.ldap_url.startswith('ldaps'):
                conn.start_tls_s()
        return conn

    def get_connection_admin(self):
        conn = self.get_connection()
        conn.simple_bind_s(self.root_bind_dn, self.root_bind_password)
        return conn

    def get_connection_external(self):
        assert self.ldap_url.startswith('ldapi://')

        conn = self.get_connection()
        conn.sasl_interactive_bind_s("", ldap.sasl.external())
        return conn
