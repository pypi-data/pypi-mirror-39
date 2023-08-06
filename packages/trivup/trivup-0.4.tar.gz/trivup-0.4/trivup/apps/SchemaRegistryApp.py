from trivup import trivup

import contextlib
import os
import socket
import time

class SchemaRegistryApp (trivup.App):
    """ Confluent Schema Registry app """
    def __init__(self, cluster, conf=None, on=None):
        """
        @param cluster     Current cluster
        @param conf        Configuration dict, see below.
        @param on          Node name to run on

        Supported conf keys:
           * version - Confluent Platform version to use.
           * listener_types - Listener types (http,https)
           * listener_host - alternative listener host instead of node name (e.g., '*')
           * port_base - Low TCP port base to start allocating from (random)
           * kafka_path - Path to Kafka build tree (for trunk usage)
           * fdlimit - RLIMIT_NOFILE (default: system)
           * conf - arbitary server.properties config as a list of strings.
        """
        super(SchemaRegistryApp, self).__init__(cluster, conf=conf, on=on)

        zk = cluster.find_app('ZookeeperApp')
        if zk is None:
            raise Exception('ZookeeperApp required')

        self.conf['zk_connect'] = zk.get('address', None)
        if self.conf['zk_connect'] is None:
            raise Exception('ZookeeperApp lacks address')

        if self.conf.get('version', None) is None:
            self.conf['version'] = '4.1.1'

        if 'fdlimit' not in self.conf:
            self.conf['fdlimit'] = 50000

        listener_host = self.conf.get('listener_host', self.conf.get('0.0.0.0'))

        # Arbitrary (non-template) configuration statements
        conf_blob = self.conf.get('conf', list())

        # Create listeners
        ports = [(x, trivup.TcpPortAllocator(self.cluster).next(self, self.conf.get('port_base', None))) for x in sorted(set(self.conf.get('listeners', ['http', 'https']).split(',')))]
        self.conf['listeners'] = ','.join(['%s://%s:%d' % (x[0], listener_host, x[1]) for x in ports])
        self.dbg('Listeners: %s' % self.conf['listeners'])

#        # SSL config and keys (et.al.)
#        if getattr(cluster, 'ssl', None) is not None:
#            ssl = cluster.ssl
#            keystore,truststore,_,_ = ssl.create_keystore('broker%s' % self.appid)
#            conf_blob.append('ssl.protocol=TLS')
#            conf_blob.append('ssl.enabled.protocols=TLSv1.2,TLSv1.1,TLSv1')
#            conf_blob.append('ssl.keystore.type = JKS')
#            conf_blob.append('ssl.keystore.location = %s' % keystore)
#            conf_blob.append('ssl.keystore.password = %s ' % ssl.conf.get('ssl_key_pass'))
#            conf_blob.append('ssl.key.password = %s' % ssl.conf.get('ssl_key_pass'))
#            conf_blob.append('ssl.truststore.type = JKS')
#            conf_blob.append('ssl.truststore.location = %s' % truststore)
#            conf_blob.append('ssl.truststore.password = %s' % ssl.conf.get('ssl_key_pass'))
#            conf_blob.append('ssl.client.auth = %s' % self.conf.get('ssl_client_auth', 'required'))
#
#
        # Generate config file
        self.conf['conf_file'] = self.create_file_from_template('server.properties',
                                                                self.conf,
                                                                append_data='\n'.join(conf_blob))

        self.conf['start_cmd'] = 'docker run ' + \
        '--net=confluent --rm confluentinc/cp-schema-registry:4.1.1 ' + \
        '-e SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL={} '.format(self.conf.get('zk_connect')) + \
        '-e SCHEMA_REGISTRY_HOST_NAME=schema-registry ' + \
        '-e SCHEMA_REGISTRY_LISTENERS={} '.format(self.conf.get('listeners')) + \
        'confluentinc/cp-schema-registry:{}'.format(self.conf.get('version'))

        self.conf['stop_cmd'] = None # Ctrl-C

    def operational (self):
        self.dbg('Checking if operational')
        return True
        addr, port = self.get('address').split(':')
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            return s.connect_ex((addr, int(port))) == 0

