import logging
from collections import namedtuple

from requests import ConnectionError
from pipelines import WikiPipeline as Pipe
from proxmoxer import ProxmoxAPI
from settings import PROXMOX_HOST, PROXMOX_USER, PROXMOX_PASS


logger = logging.getLogger(__name__)

# nodes and VMs models
Node = namedtuple('Node', ['mem_used', 'mem_total', 'cpu',
                           'hdd_used', 'hdd_total', 'name'])

VM = namedtuple('VM', ['mem', 'hdd', 'cpu', 'name',
                       'status', 'vmid', 'node'])


class Proxmox(object):

    # proxmox connection
    _conn = None

    # json pipe
    _pipe = Pipe()

    def __init__(self):
        # trying to setup connection
        self.setup_conn()

    def setup_conn(self):
        if self._conn is None:
            try:
                self._conn = ProxmoxAPI(host=PROXMOX_HOST,
                                        user='{}@pam'.format(PROXMOX_USER),
                                        password=PROXMOX_PASS,
                                        verify_ssl=False)
                logger.debug('connected to the "{}"'.format(PROXMOX_HOST))

            except ConnectionError as e:
                logger.critical('"{}" while connecting to the proxmox'.format(e))

    def _get_vm(self, vm):
        """combine VM model structure"""

        if vm.get('name'):
            hdd = self._bytes_to_gb(
                vm.get('maxdisk', 0))
            mem = self._bytes_to_gb(
                vm.get('maxmem', 0))
            return VM(name=vm['name'],
                      hdd=hdd,
                      mem=mem,
                      cpu=vm.get('maxcpu', 0),
                      vmid=vm['vmid'],
                      node=vm['node'],
                      status=vm['status'])

    def _get_node(self, node):
        """combine Node model structure"""

        # get values in GB
        mem_used = self._bytes_to_gb(
            node.get('mem', 0))
        mem_total = self._bytes_to_gb(
            node.get('maxmem', 0))
        hdd_used = self._bytes_to_gb(
            node.get('disk', 0))
        hdd_total = self._bytes_to_gb(
            node.get('maxdisk', 0))

        return Node(name=node['node'],
                    mem_used=mem_used,
                    mem_total=mem_total,
                    hdd_used=hdd_used,
                    hdd_total=hdd_total,
                    cpu=node.get('maxcpu', 0))

    @staticmethod
    def _bytes_to_gb(bytes_val):
        try:
            # 1073741824 bytes in 1 GB
            return round(
                int(bytes_val) / 1073741824, 2
            )
        except TypeError:
            return 0

    def _get_resources(self):
        try:
            return self._conn.cluster.resources.get()
        except Exception as e:
            logger.error('"{}" while getting resources'.format(e))

    def get_stats(self):
        """get stats (VMs and nodes resources)"""
        results = {}
        # check proxmox connection
        if self._conn is None:
            logger.error('no connection found; exiting..')
            return

        # get cluster resources
        resources = self._get_resources()
        if not resources:
            logger.error('no resources found')

        # extract nodes and VMs from list of resources
        for item in resources or []:
            if item.get('vmid'):  # VM found (let's assume that only VM has 'vmid' attribute)
                vm = self._get_vm(item)
                if vm:
                    logger.debug('found "{}" VM from "{}" node'.format(vm.name, vm.node))
                    results.setdefault(vm.node, {})
                    results[vm.node].setdefault('vms', [])
                    results[vm.node]['vms'].append(vm)

            elif item.get('type') == 'node':  # node found
                node = self._get_node(item)
                if node:
                    logger.debug('found node: "{}"'.format(node.name))
                    results.setdefault(node.name, {})
                    results[node.name]['node_resources'] = node

        return self._pipe.process_items(results)

