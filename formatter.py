from html import HTML


class HtmlFormatter(object):

    def __init__(self):
        self._html = HTML()

    @staticmethod
    def setup_colgroup(table):
        with table.colgroup(newlines=True) as c:
            c.col(style="width:23.4346%")
            c.col(style="width:28.3323%")
            c.col(style="width:28.6423%")
            c.col(style="width:19.5908%")

    @staticmethod
    def setup_thead(table):
        keys = ('NODE', 'VMs', 'RESOURCES', 'PROJECT')
        with table.thead(newlines=True) as thead:
            with thead.tr(newlines=True) as tr:
                for key in keys:
                    th = tr.th(newlines=True, scope="col",
                               style="text-align:center")
                    th.div(key)

    @staticmethod
    def node_as_str(node):
        ram_str = '{}GB/{}GB\n'.format(node.mem_used,
                                     node.mem_total)
        hdd_str = '{}GB/{}GB\n'.format(node.hdd_used,
                                     node.hdd_total)

        return 'Name: <strong>{}</strong><br>\nCPU: {}<br>\nRAM: {}<br>\n' \
               'HDD: {}\n'.format(node.name, node.cpu, ram_str, hdd_str)

    @staticmethod
    def resources_as_str(vm):
        return '{}CPU/{}GB/{}GB\n'.format(vm.cpu, vm.mem, vm.hdd)

    @staticmethod
    def vm_as_str(vm):
        return '{} ({})\n'.format(vm.vmid, vm.name)

    def make_tbody(self, table, nodes):
        with table.tbody(newlines=True) as tbody:
            for node_name, data in nodes.items():
                with tbody.tr(newlines=True) as tr:
                    node = self.node_as_str(data['stats'])
                    vms = [self.vm_as_str(vm) for vm in data['vms']]
                    resources = [self.resources_as_str(vm) for vm in data['vms']]
                    vms = '<br>'.join(vms)
                    resources = '<br>'.join(resources)

                    tr.td(node, newlines=True, escape=False)
                    tr.td(vms, newlines=True, escape=False)
                    tr.td(resources, newlines=True, escape=False)
                    tr.td('None', newlines=True, escape=False)

    def get_table(self, vms):
        with self._html.table(style="width:88.4384%;"
                              "padding:0px") as table:
            self.setup_colgroup(table)
            self.setup_thead(table)
            self.make_tbody(table, vms)

        return table
