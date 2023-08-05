# coding=utf-8
import logging
import os

from .ovs import bridge as ovs_bridge


class OvsCtl:
    logging.getLogger(__name__)
    address = None  # type: str
    ovs = None  # type: ovs_bridge.OVSBridge

    @staticmethod
    def get_instance():
        """ Static access method.
        :rtype: OvsCtl
        :return: OvsCtl instance
        """
        OVSDB_ADDR = 'tcp:{}:{}'.format(os.environ.get('SW4IOT_OVS_HOST', '127.0.0.1'),
                                        os.environ.get('SW4IOT_OVS_PORT', 6640))
        return OvsCtl(host=OVSDB_ADDR)

    def __init__(self, host):
        # OVSBridge instance instantiated later
        self.ovs = None
        self.address = host

    def _ovsdb_connection(self, br_name):
        """

        :param br_name:
        :rtype: ovs_bridge.OVSBridge
        :return: ovs_bridge
        """
        try:
            self.ovs = ovs_bridge.OVSBridge(self.address, br_name)
        except Exception as e:
            logging.exception('Cannot initiate OVSDB connection: %s', e)
            return None

        return self.ovs

    def add_patch(self, br_name, patch0, patch1):
        """
        For all new switch the patch(ligação) will connect then on ovsbr0
        """
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        ovs.add_patch(patch0, patch1)

    def add_bridge(self, br_name):
        """
        TODO: desc.
        """
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        ovs.add_bridge()

    def get_port_name_list(self, br_name):
        """
        TODO: desc.
        """
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        return ovs.get_port_name_list()

    def del_bridge(self, br_name):
        """
        TODO: desc.
        """
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        ovs.del_bridge()

    def add_port(self, br_name, port):
        """
        TODO: desc.
        """
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        ovs.add_port(port)

    def del_port(self, br_name, port):
        """
        TODO: desc.
        """
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        ovs.del_port(port)

    def del_patch(self, br_name, patch):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None
        ovs.del_port(patch)

    def get_port_list(self, br_name):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return []

        return ovs.get_port_name_list()

    def get_ovs_bridge(self, br_name=None, dpid=None):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        try:
            return ovs.get_bridge_name(dpid)
        except Exception as e:
            return None

    def get_dpid(self, br_name):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        return ovs.get_datapath_id()

    def add_vlan(self, br_name, port, vlan_id):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None

        return ovs.add_vlan(port, vlan_id)

    def set_protocol(self, br_name, ofproto):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None
        return ovs.add_protocol(ofproto)

    def set_controller(self, br_name, ip, port):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None
        controller = "tcp:%s:%s" % (ip, port)
        return ovs.set_controller([controller, ])

    def get_ofport(self, br_name, port_name):
        ovs = self._ovsdb_connection(br_name)
        if ovs is None:
            return None
        return ovs.get_ofport(port_name)
