
from ucsmsdk.ucshandle import UcsHandle, UcsException
from ucsmsdk import mometa
from pycrypt.encryption import AESCipher
from pyucs.ucs.vlan.comparison import ListComparison, ComparisonObject
from pyucs.statsd.portstats import EthPortStat, EthPortChannelStat, FcPortStat, FcPortChannelStat


class Ucs(UcsHandle):
    """
        This is a custom UCS class that is used to simplify some of the methods and processes
        with ucsmsdk into a single class class with simple method calls. The ucsmsdk lacks
        a lot of built-in 'functionality' and really only provides raw data returned via
        query_dn and query_classid. These are the only two meaningful methods of ucsmsdk
        and this class is an attempt to bring some simplified method calls to ucsmsdk.
        This class also encrypts the password so that it is not stored in clear text in memory.
    """

    def __init__(self, ip, username, password, port=None, secure=None,
                 proxy=None, timeout=None, query_classids=None):
        super().__init__(ip, username, password, port=port, secure=secure, proxy=proxy, timeout=timeout)
        self.cipher = AESCipher()
        self._password = self.cipher.encrypt(self._UcsSession__password)
        self._UcsSession__password = None
        self._connected = False
        # define default classids in which the Ucs object will by default
        # have properties for. Since these are default we assign immutable
        # and hidden Tuple object here.
        self._default_classids = ('OrgOrg',
                                  'FabricChassisEp',
                                  'FabricVlan',
                                  'ComputeBlade',
                                  'VnicLanConnTempl',
                                  'LsServer')
        self._query_classids = list(self._default_classids)
        # allow at initialization the option to add to the 'default' property list of managed objects
        if query_classids:
            self._query_classids.append(query_classids)
        # make the _query_classids property an immutable object after initialization
        self._query_classids = tuple(self._query_classids)

    def login(self, **kwargs):
        self.connect(**kwargs)

    def connect(self, **kwargs):
        """
        Connect method so that the password can be decrypted for the connection
        as well as to populate the default properties of the Ucs object
        :param kwargs:
        :return:
        """
        self._UcsSession__password = self.cipher.decrypt(self._password, self.cipher.AES_KEY)
        self._connected = self._login(**kwargs)
        self._UcsSession__password = None
        self.refresh_inventory()

    def logout(self, **kwargs):
        self.disconnect(**kwargs)

    def disconnect(self, **kwargs):
        self._logout(**kwargs)
        self._connected = False

    def refresh_inventory(self):
        self._is_connected()
        q = self.query_classids(*self._query_classids)
        for k in q.keys():
            setattr(self, k, q[k])

    def clear_default_properties(self):
        self._is_connected()
        q = self.query_classids(*self._query_classids)
        for k in q.keys():
            delattr(self, k)

    def _is_connected(self):
        """
        method to check if there is a connection to ucsm
        and raise an exception if not.
        This is used as a check prior to running any other
        methods.
        """
        if self._connected:
            return True
        else:
            raise UcsException(error_code=1,
                               error_descr='Not currently logged in. Please connect to a UCS domain first')

    def query_rn(self, rn, class_id):
        """
        Added a missing method that Cisco should add in the ability to query the relative_name (rn)
        of a managed object
        :param rn:
        :param class_id:
        :return:
        """
        return self.query_classid(class_id=class_id,
                                  filter_str='(rn, "{}")'.format(rn)
                                  )

    def _query_mo(self, class_id, chassis=None, slot=None, vlan_id=None, name=None,
                  service_profile=None, org=None, fabric=None, port=None, portchannel=None,
                  dn=None, rn=None):
        """
        This is a beast of a method and really the brains of the operation of all the
        availbel methods in this class.
        :param class_id: Required parameter
        :param chassis: required for chassis query
        :param slot: required for chassis/blade query
        :param vlan_id: required for vlan query
        :param name:
        :param service_profile: required for service_profile query
        :param org: required for org query
        :param dn: required for dn query
        :param rn: required for rn query
        :return: one or more managedObjects
        """
        self._is_connected()

        # The below is fairly self explanatory and won't be commented
        # built-in query_dn method
        if dn:
            return self.query_dn(dn=dn)

        # custom query_rn method with an optional org search filter
        if rn:
            if org:
                return self.query_classid(class_id=class_id,
                                          filter_str='((rn, "{}") and (dn, "{}"))'.format(rn, org))
            return self.query_rn(rn=rn, class_id=class_id)

        # vlan_id and optionally adding the name of the vlan
        if vlan_id:
            if name:
                return self.query_classid(class_id=class_id,
                                          filter_str='((id, "{}") and (name, "{}"))'.format(vlan_id, name))
            return self.query_classid(class_id=class_id,
                                      filter_str='(id, "{}")'.format(vlan_id))
        # search for anything with a name parameter and optionally use an org search filter
        if name:
            if org:
                return self.query_classid(class_id=class_id,
                                          filter_str='((name, "{}") and (dn, "{}"))'.format(name, org))
            return self.query_rn(rn=name, class_id=class_id)

        # chassis ID and optionally a blade slot id
        if chassis:
            if slot:
                return self.query_classid(class_id=class_id,
                                          filter_str='((chassis_id, "{}") and (slot_id, "{}"))'.format(chassis, slot))
            return self.query_classid(class_id=class_id,
                                      filter_str='(chassis_id, "{}")'.format(chassis))

        # all chassis blade slots with slot id
        if slot:
            return self.query_classid(class_id=class_id,
                                      filter_str='((slot_id, "{}"))'.format(slot))

        # service profile managedobject
        if service_profile:
            return self.query_classid(class_id=class_id,
                                      filter_str='((dn, "{}"))'.format(service_profile.dn)
                                      )

        if fabric:
            return self.query_classid(class_id=class_id,
                                      filter_str='((dn, "{}"))'.format(fabric.dn)
                                      )

        # by default return all managedObjects from classid
        return self.query_classid(class_id=class_id)

    def get_vnic_template(self, vnic=None, name=None, org=None, dn=None, rn=None):
        self._is_connected()

        if vnic and isinstance(vnic, list):
            tmp = []
            for v in vnic:
                if v.oper_nw_templ_name:
                    tmp.append(self._query_mo(class_id='VnicLanConnTempl', dn=v.oper_nw_templ_name))
            return tmp

        return self._query_mo(class_id='VnicLanConnTempl',
                              name=name,
                              org=org,
                              dn=dn,
                              rn=rn
                              )

    def get_vnic(self, service_profile=None, dn=None):
        self._is_connected()

        if service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
            return self._query_mo(class_id='VnicEther',
                                  service_profile=service_profile,
                                  dn=dn
                                  )
        elif service_profile and isinstance(service_profile, list):
            tmp = []
            for s in service_profile:
                tmp = tmp.__add__(self._query_mo(class_id='VnicEther',
                                                 service_profile=s
                                                 ))
            return tmp
        elif service_profile and isinstance(service_profile, str):
            raise UcsException(
                "InvalidType: Parameter 'service_profile' expected type "
                "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

        elif dn:
            self._query_mo(class_id='VnicEther',
                           dn=dn
                           )
        return self._query_mo(class_id='VnicEther')

    def get_vnic_vlans(self, vnic=None, vnic_template=None, service_profile=None, dn=None):
        self._is_connected()

        if vnic and isinstance(vnic, mometa.vnic.VnicEther.VnicEther):
            return self.query_classid('VnicEtherIf',
                                      filter_str='(dn, "{}")'.format(vnic.dn))

        elif vnic and isinstance(vnic, list):
            tmp = []
            for v in vnic:
                tmp.append(self.query_classid('VnicEtherIf',
                                              filter_str='(dn, "{}")'.format(v.dn)))
            return tmp

        elif vnic_template and isinstance(vnic_template, mometa.vnic.VnicLanConnTempl.VnicLanConnTempl):
            return self.query_classid('VnicEtherIf',
                                      filter_str='(dn, "{}")'.format(vnic_template.dn))
        elif vnic_template and isinstance(vnic_template, list):
            tmp = []
            for v in vnic_template:
                tmp.append(self.query_classid('VnicEtherIf',
                                              filter_str='(dn, "{}")'.format(v.dn)))
            return tmp

        elif vnic and isinstance(vnic, str):
            raise UcsException(
                "InvalidType: Parameter 'vnic' expected type "
                "'ucsmsdk.mometa.vnic.VnicEther.VnicEther' and recieved 'str'")

        elif service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
            return self._query_mo(class_id='VnicEtherIf',
                                  service_profile=service_profile,
                                  dn=dn
                                  )
        elif service_profile and isinstance(service_profile, str):
            raise UcsException(
                "InvalidType: Parameter 'service_profile' expected type "
                "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

        elif dn:
            self._query_mo(class_id='VnicEther',
                           dn=dn
                           )
        return self._query_mo(class_id='VnicEther')

    def get_vhba(self, service_profile=None, dn=None):
        self._is_connected()

        if service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
            return self._query_mo(class_id='VnicFc',
                                  service_profile=service_profile,
                                  dn=dn
                                  )
        elif service_profile and isinstance(service_profile, str):
            raise UcsException(
                "InvalidType: Parameter 'service_profile' expected type "
                "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

        elif dn:
            self._query_mo(class_id='VnicFc',
                           dn=dn
                           )
        return self._query_mo(class_id='VnicFc')

    def get_org(self, name=None, org=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='OrgOrg',
                              name=name,
                              org=org,
                              dn=dn,
                              rn=rn
                              )

    def get_vlan(self, name=None, vlan_id=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='FabricVlan',
                              name=name,
                              vlan_id=vlan_id,
                              dn=dn,
                              rn=rn
                              )

    def get_service_profile(self, name=None, org=None, dn=None, rn=None, only_active=False):
        self._is_connected()
        tmp = self._query_mo(class_id='LsServer',
                             name=name,
                             org=org,
                             dn=dn,
                             rn=rn
                             )
        if only_active:
            tmp = [s for s in tmp if s.assoc_state == 'associated']

        return tmp

    def get_chassis(self, name=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='FabricChassisEp',
                              name=name,
                              dn=dn,
                              rn=rn
                              )

    def get_blade(self, chassis=None, slot=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='ComputeBlade',
                              chassis=chassis,
                              slot=slot,
                              dn=dn,
                              rn=rn
                              )

    def get_switch_fabric(self, name=None, dn=None):
        self._is_connected()
        return self._query_mo(class_id='NetworkElement',
                              name=name,
                              dn=dn
                              )

    def get_fabric_etherport(self, dn=None, rn=None):
        self._is_connected()

        if dn:
            return self._query_mo(class_id='EtherPIo',
                                  dn=dn
                                  )
        return self._query_mo(class_id='EtherPIo')

    def get_fabric_fcport(self, dn=None, rn=None):
        self._is_connected()

        if dn:
            return self._query_mo(class_id='FcPIo',
                                  dn=dn
                                  )
        return self._query_mo(class_id='FcPIo')

    def get_port_channel(self, port_type=None, dn=None, rn=None):
        self._is_connected()

        if dn:
            if dn.find('fabric/lan') >= 0:
                return self._query_mo(class_id='FabricEthLanPc',
                                      dn=dn
                                      )
            if dn.find('fabric/san') >= 0:
                return self._query_mo(class_id='FabricFcSanPc',
                                      dn=dn
                                      )
        elif port_type == 'Ethernet':
            return self._query_mo(class_id='FabricEthLanPc')

        elif port_type == 'Fc':
            return self._query_mo(class_id='FabricFcSanPc')

        tmp = []
        tmp.append(self._query_mo(class_id='FabricEthLanPc'))
        tmp.append(self._query_mo(class_id='FabricFcSanPc'))
        return tmp

    def get_system_storage(self, fabric=None, dn=None):
        self._is_connected()

        if fabric and isinstance(fabric, mometa.network.NetworkElement.NetworkElement):
            return self._query_mo(class_id='StorageItem',
                                  fabric=fabric,
                                  dn=dn
                                  )
        elif fabric and isinstance(fabric, str):
            raise UcsException(
                "InvalidType: Parameter 'fabric' expected type "
                "'mometa.network.NetworkElement.NetworkElement' and recieved 'str'")

        elif dn:
            return self._query_mo(class_id='StorageItem',
                                  dn=dn
                                  )
        return self._query_mo(class_id='StorageItem')

    def get_vnic_stats(self, vnic=None, service_profile=None, ignore_error=False):
        self._is_connected()

        # check if a service profile was provided as a way to reduce returned results
        if isinstance(service_profile, mometa.ls.LsServer.LsServer):
            stats = self.get_vnic_stats(vnic=self.get_vnic(service_profile=service_profile), ignore_error=ignore_error)
            if stats:
                return stats

        # check if the vnic parameter is a managedobject
        if isinstance(vnic, mometa.vnic.VnicEther.VnicEther):
            if vnic.equipment_dn:
                return self.query_dn("{}/vnic-stats".format(vnic.equipment_dn))

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(vnic, list) or isinstance(vnic, tuple):
            tmp = []
            for v in vnic:
                if v.equipment_dn:
                    tmp.append(self.get_vnic_stats(v, ignore_error=ignore_error))
            return tmp
        if not ignore_error:
            raise UcsException("InvalidType: Unexpected type with parameter 'vnic'."
                               "Use type VnicEther or list/tuple of VnicEther")

    def get_vhba_stats(self, vhba=None, service_profile=None, ignore_error=False):
        self._is_connected()

        # check if a service profile was provided as a way to reduce returned results
        if isinstance(service_profile, mometa.ls.LsServer.LsServer):
            stats = self.get_vhba_stats(vhba=self.get_vnic(service_profile=service_profile), ignore_error=ignore_error)
            if stats:
                return stats

        # check if the vnic parameter is a managedobject
        if isinstance(vhba, mometa.vnic.VnicFc.VnicFc):
            if vhba.equipment_dn:
                return self.query_dn("{}/vnic-stats".format(vhba.equipment_dn))

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(vhba, list) or isinstance(vhba, tuple):
            tmp = []
            for v in vhba:
                if v.equipment_dn:
                    tmp.append(self.get_vhba_stats(v, ignore_error=ignore_error))
            return tmp

        if not ignore_error:
            raise UcsException("InvalidType: Unexpected type with parameter 'vhba'."
                               "Use type VnicFc or list/tuple of VnicFc")

    def get_fabric_etherport_stats(self, port=None, ignore_error=False):
        self._is_connected()

        # check if the vnic parameter is a managedobject
        if isinstance(port, mometa.ether.EtherPIo.EtherPIo):
            port_stats = None
            if port.oper_state == 'up':
                port_stats = EthPortStat()
                port_stats.pop_base_params(port)
                port_stats.pause_stats(self.query_dn("{}/pause-stats".format(port.dn)))
                port_stats.loss_stats(self.query_dn("{}/loss-stats".format(port.dn)))
                port_stats.err_stats(self.query_dn("{}/err-stats".format(port.dn)))
                port_stats.rx_stats(self.query_dn("{}/rx-stats".format(port.dn)))
                port_stats.tx_stats(self.query_dn("{}/tx-stats".format(port.dn)))

            return port_stats

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(port, list) or isinstance(port, tuple):
            tmp = []
            for p in port:
                if p.oper_state == 'up':
                    port_stats = EthPortStat()
                    port_stats.pop_base_params(p)
                    port_stats.pause_stats(self.query_dn("{}/pause-stats".format(p.dn)))
                    port_stats.loss_stats(self.query_dn("{}/loss-stats".format(p.dn)))
                    port_stats.err_stats(self.query_dn("{}/err-stats".format(p.dn)))
                    port_stats.rx_stats(self.query_dn("{}/rx-stats".format(p.dn)))
                    port_stats.tx_stats(self.query_dn("{}/tx-stats".format(p.dn)))
                    tmp.append(port_stats)
            return tmp
        if not ignore_error:
            raise UcsException(99,
                "InvalidType: Unexpected type with parameter 'port'.Use type EtherPIo or list/tuple of EtherPIo")

    def get_fabric_fcport_stats(self, port=None, ignore_error=False):
        self._is_connected()

        # check if the vnic parameter is a managedobject
        if isinstance(port, mometa.fc.FcPIo.FcPIo):
            port_stats = None
            if port.oper_state == 'up':
                port_stats = FcPortStat()
                port_stats.pop_base_params(port)
                port_stats.stats(self.query_dn("{}/stats".format(port.dn)))
                port_stats.err_stats(self.query_dn("{}/err-stats".format(port.dn)))

            return port_stats

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(port, list) or isinstance(port, tuple):
            tmp = []
            for p in port:
                if p.oper_state == 'up':
                    port_stats = FcPortStat()
                    port_stats.pop_base_params(p)
                    port_stats.err_stats(self.query_dn("{}/err-stats".format(p.dn)))
                    port_stats.stats(self.query_dn("{}/stats".format(p.dn)))
                    tmp.append(port_stats)
            return tmp
        if not ignore_error:
            raise UcsException(99,
                "InvalidType: Unexpected type with parameter 'port'.Use type FcPIo or list/tuple of FcPIo")

    def get_fabric_etherportchannel_stats(self, portchannel=None, ignore_error=False):
        self._is_connected()

        # check if the vnic parameter is a managedobject
        if isinstance(portchannel, mometa.fabric.FabricEthLanPc.FabricEthLanPc):
            port_stats = None
            if portchannel.oper_state == 'up':
                port_stats = EthPortChannelStat()
                port_stats.pop_base_params(portchannel)
                port_stats.pause_stats(self.query_dn("{}/pause-stats".format(portchannel.dn)))
                port_stats.loss_stats(self.query_dn("{}/loss-stats".format(portchannel.dn)))
                port_stats.err_stats(self.query_dn("{}/err-stats".format(portchannel.dn)))
                port_stats.rx_stats(self.query_dn("{}/rx-stats".format(portchannel.dn)))
                port_stats.tx_stats(self.query_dn("{}/tx-stats".format(portchannel.dn)))

            return port_stats

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(portchannel, list) or isinstance(portchannel, tuple):
            tmp = []
            for p in portchannel:
                if p.oper_state == 'up':
                    port_stats = EthPortChannelStat()
                    port_stats.pop_base_params(p)
                    port_stats.pause_stats(self.query_dn("{}/pause-stats".format(p.dn)))
                    port_stats.loss_stats(self.query_dn("{}/loss-stats".format(p.dn)))
                    port_stats.err_stats(self.query_dn("{}/err-stats".format(p.dn)))
                    port_stats.rx_stats(self.query_dn("{}/rx-stats".format(p.dn)))
                    port_stats.tx_stats(self.query_dn("{}/tx-stats".format(p.dn)))
                    tmp.append(port_stats)
            return tmp
        if not ignore_error:
            raise UcsException(99,
                "InvalidType: Unexpected type with parameter 'portchannel'.Use type EtherPIo or list/tuple of EtherPIo")

    def get_fabric_fcportchannel_stats(self, portchannel=None, ignore_error=False):
        self._is_connected()

        # check if the vnic parameter is a managedobject
        if isinstance(portchannel, mometa.fabric.FabricFcSanPc.FabricFcSanPc):
            port_stats = None
            if portchannel.oper_state == 'up':
                port_stats = FcPortChannelStat()
                port_stats.pop_base_params(portchannel)
                port_stats.stats(self.query_dn("{}/stats".format(portchannel.dn)))
                port_stats.err_stats(self.query_dn("{}/err-stats".format(portchannel.dn)))

            return port_stats

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(portchannel, list) or isinstance(portchannel, tuple):
            tmp = []
            for p in portchannel:
                if p.oper_state == 'up':
                    port_stats = FcPortChannelStat()
                    port_stats.pop_base_params(p)
                    port_stats.err_stats(self.query_dn("{}/err-stats".format(p.dn)))
                    port_stats.stats(self.query_dn("{}/stats".format(p.dn)))
                    tmp.append(port_stats)
            return tmp
        if not ignore_error:
            raise UcsException(99,
                "InvalidType: Unexpected type with parameter 'portchannel'.Use type FcPIo or list/tuple of FcPIo")

    def get_system_storage_stats(self, storageitem=None, ignore_error=False):
        self._is_connected()
        if isinstance(storageitem, mometa.storage.StorageItem.StorageItem):
            return storageitem

        if isinstance(storageitem, list) or isinstance(storageitem, tuple):
            tmp = []
            for s in storageitem:
                if isinstance(storageitem, mometa.storage.StorageItem.StorageItem):
                    tmp.append(storageitem)

            return tmp

        return self.query_classid('StorageItem')

    def get_system_stats(self, ignore_error=False):
        self._is_connected()
        try:
            tmp = self.query_classid('SWSystemStatsHist')
            return tmp
        except BaseException as e:
            if not ignore_error:
                raise UcsException(e)

    def assign_vlan_to_vnic(self, mo, vlan_name):
        from ucsmsdk.mometa.vnic.VnicEther import VnicEther
        from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
        from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
        if isinstance(mo, str):
            # assume this is a dn value
            mo = self.query_dn(mo)
        if isinstance(mo, VnicEther) or isinstance(mo, VnicLanConnTempl):

            vnic_vlan = VnicEtherIf(parent_mo_or_dn=mo,
                                    name=vlan_name)
            self.add_mo(vnic_vlan)
            self.commit()
            return self.query_dn(vnic_vlan.dn)
        else:
            raise UcsException("ManagedObject Invalid Type")

    def create_vlan_global(self, vlan_name, vlan_id):
        vlan_mo = mometa.fabric.FabricVlan.FabricVlan(parent_mo_or_dn='fabric/lan',
                                                      sharing='none',
                                                      name=vlan_name,
                                                      id=vlan_id,
                                                      mcast_policy_name='',
                                                      policy_owner='local',
                                                      default_net='no',
                                                      pub_nw_name='',
                                                      compression_type='included'
                                                      )
        self.add_mo(vlan_mo)
        self.commit()
        return self.get_vlan(name=vlan_name, vlan_id=vlan_id)

    @staticmethod
    def audit_vnic_vlans(ucs, vnic_vlans, ignore_same=False):
        """
        Takes a list of vnic_vlans and compares them to each other. vnic_vlans must have len >= 2
        :param vnic_vlans: [[vnic1_vlans],[vnic2_vlans],[vnic3_vlans],[vnicN_vlans]]
        :param ignore_same: [BOOL] Output the items that are different or output everything including items that are the same
        :return: comparison_obj
        """

        from operator import attrgetter
        meta = {}  # structure will be { vnic.dn: [vlan_id_list] }
        if vnic_vlans and isinstance(vnic_vlans, list) and len(vnic_vlans) >= 2:
            for vlans in vnic_vlans:
                vlans.sort(key=lambda x: x.rn)
                tmp_dict = {
                    vlans[0]._ManagedObject__parent_dn: list(map(attrgetter('rn'), vlans))
                }
                meta.update(tmp_dict)

            max_index = len(list(meta.keys())) - 1
            comparison_list = []
            for i in range(0, max_index+1):
                if not i == max_index:
                    for x in range(i+1, max_index+1):
                        ref = list(meta.keys())[i]
                        dif = list(meta.keys())[x]
                        comparison_list.append(
                            ListComparison(reference_dict={ref: meta[ref]},
                                           difference_dict={dif: meta[dif]},
                                           ucs=ucs)
                        )
            results = []
            for l in comparison_list:
                tmp = l.compare(ignore_same=ignore_same)
                if tmp:
                    results.append(tmp)

            if len(results) > 0:
                return results
            return None

    def remediate_vnic_vlan_audit(self, vnic_audit):
        if isinstance(vnic_audit, ComparisonObject):
            if vnic_audit.ucs == self.ucs:
                if vnic_audit.operator == '=>':
                    self.assign_vlan_to_vnic(vnic_audit.reference, vnic_audit.value.replace('if-', ''))
                elif vnic_audit.operator == '<=':
                    self.assign_vlan_to_vnic(vnic_audit.difference, vnic_audit.value.replace('if-', ''))
        elif isinstance(vnic_audit, list):
            for audit in vnic_audit:
                if isinstance(audit, ComparisonObject):
                    if audit.ucs == self.ucs:
                        if audit.operator == '=>':
                            self.assign_vlan_to_vnic(audit.reference, audit.value.replace('if-', ''))
                        elif audit.operator == '<=':
                            self.assign_vlan_to_vnic(audit.difference, audit.value.replace('if-', ''))
                else:
                    raise UcsException(
                        "Invalid Paramter Type: Expected type 'ComparisonObject' or 'list' of 'ComparisonObject'")
        else:
            raise UcsException("Invalid Paramter Type: Expected type 'ComparisonObject' or 'list' of 'ComparisonObject'")
