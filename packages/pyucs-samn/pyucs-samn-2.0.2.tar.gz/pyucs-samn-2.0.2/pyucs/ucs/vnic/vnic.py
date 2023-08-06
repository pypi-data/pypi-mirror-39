
class VnicVlanList:

    def __init__(self):
        self.ucs = None
        self.vnic = None
        self.vlan_list = None

    def set_attr(self, vnic, vlan_list):
        self.vnic = vnic
        self.vlan_list = vlan_list
        self.ucs = self.vnic._handle.ucs
