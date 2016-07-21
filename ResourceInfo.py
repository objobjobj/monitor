# -*- coding:utf-8 -*-
from kazoo.client import KazooClient
import json
import time


class ResourceInfo:
    def __init__(self):
        self.SERVER_IP_AND_PORT = "172.18.229.251:2181"
        self.zk = None
        self.server_dynamic_node = "/monitorDataServer"
        self.vms_static_node = "/monitorDataJustOneTime"
        self.vms_dynamic_node = "/monitorData"
        self.slash = "/"
        self.base_divider = [1, 1024, 1048576, 1073741824]

    def start_zk(self):
        self.zk = KazooClient(hosts=self.SERVER_IP_AND_PORT)
        self.zk.start()
        print 'ZooKeeper Client Starting...'

    def stop_zk(self):
        self.zk.stop()
        print 'ZooKeeper Client Stopped.'

    def restart_zk(self):
        self.zk.restart()
        print 'ZooKeeper Client Restarting...'

    def _get_children_nodes(self, parent_node):
        """Get all the children nodes of parent_node.

        ParentNode: monitorData and monitorDataJustOneTime

        """
        children_nodes = self.zk.get_children(parent_node)
        return children_nodes

    def _get_node_info(self, node_path):
        """Get the node info of the given node_path"""
        node_info, stat = self.zk.get(node_path)
        return node_info

    def _get_str_between(self, whole_str, begin_str, end_str):
        """Get string from str between begin_str and end_str"""
        index1 = whole_str.index(begin_str) + len(begin_str)
        index2 = whole_str.index(end_str)
        # print type(index1), index2
        return whole_str[index1:index2]

    def _get_converted_value(self, val, base = 1, digit = 1):
        """Convert the given value into the expected base."""
        return round(1.0 * long(val) / self.base_divider[base], digit)

    def get_server_info(self):
        """Get the info of the server node"""
        server_info = self._get_node_info(self.server_dynamic_node)
        return server_info

    def get_total_info_of(self, ip):
        """Get the total resource info of the machine of the given ip"""
        node_path = self.vms_dynamic_node + self.slash + str(ip)
        total_info = self._get_node_info(node_path)
        return json.loads(total_info)

    def _calculate_speed(self, dict1, dict2):
        time1 = 0
        time2 = 0
        quantity1 = 0
        quantity2 = 0
        for i in dict1:
            time1 = float(i)
            quantity1 = float(dict1[i])
            pass

        for i in dict2:
            time2 = float(i)
            quantity2 = float(dict2[i])
            pass

        time_diff = time2 - time1
        quantity_diff =quantity2 - quantity1
        if time_diff > 0:
            if quantity_diff >= 0:
                return self._get_converted_value(1.0 * quantity_diff / time_diff, 0, 1)
            else:
                return 0.0
        else:
            return 0.0


    def get_vms_static_info(self):
        """Get the static general info of all the virtual machines"""
        parent_node = self.vms_static_node
        children_nodes = self._get_children_nodes(parent_node)
        res = dict()
        for node in children_nodes:
            node_path = parent_node + self.slash + str(node)
            node_info = self._get_node_info(node_path)
            node_info_decode = json.loads(node_info)
            # print node_info_decode
            node_info_encode = {}

            disk_usage = self._get_str_between(node_info_decode["disk_usage"], "total=", ", used")
            node_info_encode["disk_total"] = self._get_converted_value(disk_usage, 3)

            virtual_memory = self._get_str_between(node_info_decode["virtual_memory"], "total=", ", available=")
            node_info_encode["virtual_memory"] = self._get_converted_value(virtual_memory, 3)

            node_info_encode["cpu_count"] = int(node_info_decode["cpu_count"])

            user = self._get_str_between(node_info_decode["users"], "name='", "', terminal=")
            node_info_encode["user"] = user.encode("utf-8")

            node_info_encode["ip"] = node.encode("utf-8")

            res[node.encode("utf-8")] = json.dumps(node_info_encode)

            dynamic_node_path_info = self.get_total_info_of(node)
            cpu_percent = dynamic_node_path_info["cpu_percent"]
            for i in cpu_percent:
                if (time.time() - float(i)) < 10:
                    node_info_encode["status"] = "active"
                    pass
                else:
                    node_info_encode["status"] = "negative"
                    pass

            res[node.encode("utf-8")] = json.dumps(node_info_encode)

        print json.dumps(res)
        return json.dumps(res)

    def get_general_dynamic_info(self):
        """Get the dynamic general info of all the virtual machines and the server machine"""
        res = {}
        # For the virtual machines
        vms_parent_node = self.vms_dynamic_node
        vms_children_nodes = self._get_children_nodes(vms_parent_node)

        for node in vms_children_nodes:
            node_path = vms_parent_node + self.slash + str(node)
            node_info = self._get_node_info(node_path)
            node_info_decode = json.loads(node_info)
            node_info_encode = {}

            cpu_percent_average = node_info_decode["cpu_percent_average"]
            virtual_memeory = node_info_decode["virtual_memory"]
            disk_usage = node_info_decode["disk_usage"]
            net_io_sent = node_info_decode["net_io_sent"]
            net_io_recv = node_info_decode["net_io_recv"]

            for i in cpu_percent_average:
                if (time.time() - float(i)) < 10:
                    node_info_encode["status"] = "active"
                else:
                    node_info_encode["status"] = "negative"
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i)))
                node_info_encode["time"] = time_str.encode("utf-8")
                node_info_encode["cpu_percent_average"] = cpu_percent_average[i].encode("utf-8")

            for i in virtual_memeory:
                node_info_encode["memory_percent"] = self._get_str_between(virtual_memeory[i], "percent=", ", used=").encode("utf-8")

            for i in disk_usage:
                node_info_encode["disk_percent"] = self._get_str_between(disk_usage[i], "percent=", ")").encode("utf-8")

            node_info_encode["net_io_sent"] = self._calculate_speed(net_io_sent[0], net_io_sent[1])

            node_info_encode["net_io_recv"] = self._calculate_speed(net_io_recv[0], net_io_recv[1])

            node_info_encode["ip"] = node.encode("utf-8")
            node_info_encode["type"] = "virtual machine".encode("utf-8")

            res[node.encode("utf-8")] = json.dumps(node_info_encode)
            # print node_info_encode

        # For the server machine
        sv_parent_node = self.server_dynamic_node
        sv_children_nodes = self._get_children_nodes(sv_parent_node)
        for node in sv_children_nodes:
            node_path = sv_parent_node + self.slash + str(node)
            node_info = self._get_node_info(node_path)
            node_info_decode = json.loads(node_info)
            node_info_encode = {}

            cpu_percent_average = node_info_decode["cpu_percent_average"]
            virtual_memeory = node_info_decode["virtual_memory"]
            disk_usage = node_info_decode["disk_usage"]
            net_io_sent = node_info_decode["net_io_sent"]
            net_io_recv = node_info_decode["net_io_recv"]

            for i in cpu_percent_average:
                if (time.time() - float(i)) < 10:
                    node_info_encode["status"] = "active"
                else:
                    node_info_encode["status"] = "negative"
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i)))
                node_info_encode["time"] = time_str.encode("utf-8")
                node_info_encode["cpu_percent_average"] = cpu_percent_average[i].encode("utf-8")

            for i in virtual_memeory:
                node_info_encode["memory_percent"] = self._get_str_between(virtual_memeory[i], "percent=",
                                                                           ", used=").encode("utf-8")

            for i in disk_usage:
                node_info_encode["disk_percent"] = self._get_str_between(disk_usage[i], "percent=", ")").encode("utf-8")

            node_info_encode["net_io_sent"] = self._calculate_speed(net_io_sent[0], net_io_sent[1])

            node_info_encode["net_io_recv"] = self._calculate_speed(net_io_recv[0], net_io_recv[1])

            node_info_encode["ip"] = node.encode("utf-8")
            node_info_encode["type"] = "server".encode("utf-8")

            res[node.encode("utf-8")] = json.dumps(node_info_encode)

        print json.dumps(res)
        return json.dumps(res)

    def get_cpu_info_of(self, ip):
        """Get the CPU info of the virtual machine of the given ip"""
        res_cpu = dict()
        res_cpu["ip"] = ip.encode("utf-8")
        total_info = self.get_total_info_of(ip)
        cpu_percent = total_info["cpu_percent"]
        cpu_times_percent = total_info["cpu_times_percent"]
        cpu_percent_average = total_info["cpu_percent_average"]

        for i in cpu_percent:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i)))
            res_cpu["time"] = time_str.encode("utf-8")
            res_cpu["each_cpu_percent"] = cpu_percent[i].encode("utf-8")

        for i in cpu_percent_average:
            res_cpu["average_cpu_percent"] = cpu_percent_average[i].encode("utf-8")

        for i in cpu_times_percent:
            i_cpu_info = cpu_times_percent[i]
            i_user = self._get_str_between(i_cpu_info, "user=", ", nice")
            i_system = self._get_str_between(i_cpu_info, "system=", ", idle")
            i_nice = self._get_str_between(i_cpu_info, "nice=", ", system")
            i_idle = self._get_str_between(i_cpu_info, "idle=", ", iowait")
            # print i_user, i_system, i_nice, i_idle
            res_cpu["user"] = i_user.encode("utf-8")
            res_cpu["system"] = i_system.encode("utf-8")
            res_cpu["nice"] = i_nice.encode("utf-8")
            res_cpu["idle"] = i_idle.encode("utf-8")

        print json.dumps(res_cpu)
        return json.dumps(res_cpu)

    def get_memory_info_of(self, ip):
        """Get the CPU info of the machine of the given ip"""
        res_mem = dict()
        total_info = self.get_total_info_of(ip)
        swap_memory = total_info["swap_memory"]
        virtual_memory = total_info["virtual_memory"]
        # print swap_memory
        # print virtual_memory
        for i in virtual_memory:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i)))
            res_mem["time"] = time_str.encode("utf-8")
            i_vmem_info = virtual_memory[i]
            # print i_vmem_info
            i_vmem_total = self._get_str_between(i_vmem_info, "total=", ", available")
            i_vmem_available = self._get_str_between(i_vmem_info, "available=", ", percent")
            i_vmem_percent = self._get_str_between(i_vmem_info, "percent=", ", used")
            i_vmem_used = self._get_str_between(i_vmem_info, "used=", ", free")
            i_vmem_free = self._get_str_between(i_vmem_info, "free=", ", active")

            res_mem["vmem_total"] = self._get_converted_value(i_vmem_total, 3)
            res_mem["vmem_available"] = self._get_converted_value(i_vmem_available, 3)
            res_mem["vmem_percent"] = i_vmem_percent.encode("utf-8")
            res_mem["vmem_used"] = self._get_converted_value(i_vmem_used, 3)
            res_mem["vmem_free"] = self._get_converted_value(i_vmem_free, 3)

        for i in swap_memory:
            i_swap_info = swap_memory[i]
            # print i_swap_info
            i_swap_total = self._get_str_between(i_swap_info, "total=", ", used")
            i_swap_used = self._get_str_between(i_swap_info, "used=", ", free")
            i_swap_free = self._get_str_between(i_swap_info, "free=", ", percent")
            i_swap_percent = self._get_str_between(i_swap_info, "percent=", ", sin")

            res_mem["swap_total"] = self._get_converted_value(i_swap_total, 3)
            res_mem["swap_used"] = self._get_converted_value(i_swap_used, 3)
            res_mem["swap_free"] = self._get_converted_value(i_swap_free, 3)
            res_mem["swap_percent"] = i_swap_percent.encode("utf-8")

          # print res_mem

        print json.dumps(res_mem)
        return json.dumps(res_mem)

    def get_disk_info_of(self, ip):
        """Get the Disk info of the machine of the given ip"""
        res_disk = dict()
        total_info = self.get_total_info_of(ip)
        for i in total_info:
            print i

if __name__ == "__main__":
    gi = ResourceInfo()
    gi.start_zk()
    # gi.get_vms_static_info()
    gi.get_general_dynamic_info()
    # gi.get_memory_info_of("192.168.231.142")
    # gi.get_disk_info_of("192.168.231.142")

