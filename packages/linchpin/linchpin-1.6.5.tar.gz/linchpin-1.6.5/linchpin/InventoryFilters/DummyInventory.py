#!/usr/bin/env python

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .InventoryFilter import InventoryFilter


class DummyInventory(InventoryFilter):
    def get_host_data(self, topo, cfgs={}):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

        By default, the hostname will be the system field returned by dummy

        :param topo:
            linchpin Dummy resource data

        :param cfgs:
            map of config options from PinFile
        """

        host_data = {}
        var_data = cfgs.get('dummy', {})
        if var_data is None:
            var_data = {}
            var_data['__IP__'] = '__SELF__'
        for group in topo.get('dummy_res', []):
            for host in group['hosts']:
                host_data[host] = {}
                self.set_config_values(host_data[host], host, group, var_data)
        return host_data

    def get_host_ips(self, host_data):
        return host_data.keys()

    def get_inventory(self, topo, layout, config):
        if len(topo['dummy_res']) == 0:
            return ""
        host_data = self.get_host_data(topo, config)
        inven_hosts = self.get_host_ips(host_data)
        # adding sections to respective host groups
        host_groups = self.get_layout_host_groups(layout)
        self.add_sections(host_groups)
        # set children for each host group
        self.set_children(layout)
        # set vars for each host group
        self.set_vars(layout)
        # add ip addresses to each host
        self.add_ips_to_groups(inven_hosts, layout)
        self.add_common_vars(host_groups, layout)
        output = StringIO()
        self.config.write(output)
        return output.getvalue()

    def set_config_values(self, host_data, host, instance, cfgs={}):
        """
        """
        if cfgs is None:
            return
        if 'hostname' not in cfgs.keys():
            cfgs['hostname'] = '__IP__'
        for var in cfgs.keys():
            if var == 'hostname' and cfgs[var] == '__IP__':
                host_data[cfgs[var]] = host
            else:
                host_data[var] = self.config_value_helper(instance, cfgs[var])
