from __future__ import print_function
from html import HTML
from proxmoxer import ProxmoxAPI
import settings


def get_proxmox_conn():
    return ProxmoxAPI(host=settings.PROXMOX_HOST,
                      user='{}@pam'.format(settings.PROXMOX_USER),
                      password=settings.PROXMOX_PASS,
                      verify_ssl=False)


def get_vm(vm):
    if vm.get('name'):
        return {
            'maxdisk': vm.get('maxdisk', 0),
            'maxmem': vm.get('maxmem', 0),
            'maxcpu': vm.get('maxcpu', 0),
            'name': vm['name'],
            'status': vm['status'],
            'type': vm.get('type')
        }


def get_vms(proxmox):
    results = {}
    vms = proxmox.cluster.resources.get(type='vm')
    for vm in vms:
        node = vm['node']
        results.setdefault(node, [])
        vm = get_vm(vm)
        if vm:
            results[node].append(vm)

    return results


def get_table(vms):
    html = HTML()
    table = html.table(border='1')
    b = table.tbody(newlines=True)
    for vm in vms:
        r = b.tr(newlines=True)
        r.td('column 1')
        r.td('column 2')
    print(table)


if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    proxmox = get_proxmox_conn()
    vms = get_vms(proxmox)
    pp.pprint(vms)
    get_table(vms['kraken'])

