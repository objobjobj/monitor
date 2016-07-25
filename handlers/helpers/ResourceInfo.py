#!/usr/bin/env python
# -*- coding:utf-8 -*-
from kazoo.client import KazooClient
from kazoo.exceptions import KazooException
import json
import time


class ResourceInfo(object):
    def __init__(self):
        self.SERVER_IP_AND_PORT = "172.18.229.251:2181"
        self.zk = None
        self.vms_daemon_node = "/monitorDataProcessInfo"
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
        try:
            total_info = self._get_node_info(node_path)
        except KazooException:
            return dict()
        return json.loads(total_info)

    def _calculate_net_speed(self, dict1, dict2):
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

    def _calculate_disk_speed(self, dict1, dict2):
        time1 = 0
        time2 = 0
        read1 = 0
        write1 = 0
        read2 = 0
        write2 = 0
        for i in dict1:
            time1 = float(i)
            read1 = float(self._get_str_between(dict1[i], "read_bytes=", ", write_bytes"))
            write1 = float(self._get_str_between(dict1[i], "write_bytes=", ", read_time"))

        for i in dict2:
            time2 = float(i)
            read2 = float(self._get_str_between(dict2[i], "read_bytes=", ", write_bytes"))
            write2 = float(self._get_str_between(dict2[i], "write_bytes=", ", read_time"))

        time_diff = time2 - time1
        read_diff = read2 - read1
        write_diff = write2 - write1
        # print read_diff, write_diff
        if time_diff > 0:
            if read_diff >= 0 and write_diff >= 0:
                return self._get_converted_value(1.0 * read_diff / time_diff, 0, 1), self._get_converted_value(1.0 * write_diff / time_diff, 0, 1)
            else:
                return 0.0, 0.0
        else:
            return 0.0, 0.0

    def _get_total_cpu_count(self):
        """Calculate the total count of cpus in the virtual machines"""
        parent_node = self.vms_static_node
        children_nodes = self._get_children_nodes(parent_node)
        count = 0
        for node in children_nodes:
            node_path = parent_node + self.slash + str(node)
            node_info = self._get_node_info(node_path)
            node_info_decode = json.loads(node_info)

            is_server = node_info_decode["is_server"]
            if not is_server:
                count += int(node_info_decode["cpu_count"])
        return count

    def get_vms_static_info(self):
        """Get the static general info of all the virtual machines"""
        parent_node = self.vms_static_node
        children_nodes = self._get_children_nodes(parent_node)
        res = dict()
        for node in children_nodes:
            node_path = parent_node + self.slash + str(node)
            node_info = self._get_node_info(node_path)
            node_info_decode = json.loads(node_info)
            # print node_info_decode["disk_usage"]
            # print node_info_decode["virtual_memory"]
            node_info_encode = {}

            is_server = node_info_decode["is_server"]
            if is_server:
                count = self._get_total_cpu_count()
                node_info_encode["cpu_count_used"] = count
                node_info_encode["instance_count"] = len(children_nodes) - 1
            else:
                node_info_encode["cpu_count_used"] = int(node_info_decode["cpu_count"])
            node_info_encode["is_server"] = str(is_server)

            disk_total = self._get_str_between(node_info_decode["disk_usage"], "total=", ", used")
            node_info_encode["disk_total"] = self._get_converted_value(disk_total, 3)

            disk_used = self._get_str_between(node_info_decode["disk_usage"], "used=", ", free")
            node_info_encode["disk_used"] = self._get_converted_value(disk_used, 3)

            virtual_memory_used = self._get_str_between(node_info_decode["virtual_memory"], "used=", ", free=")
            node_info_encode["virtual_memory_used"] = self._get_converted_value(virtual_memory_used, 3)

            virtual_memory_total = self._get_str_between(node_info_decode["virtual_memory"], "total=", ", available=")
            node_info_encode["virtual_memory_total"] = self._get_converted_value(virtual_memory_total, 3)

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

        # print json.dumps(res)
        return json.dumps(res)

    def get_general_dynamic_info(self):
        """Get the dynamic general info of all the virtual machines and the server machine"""
        res = {}

        # For the machines
        vms_parent_node = self.vms_dynamic_node
        try:
            vms_children_nodes = self._get_children_nodes(vms_parent_node)

            if vms_children_nodes:
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
                    remote_desktop_count = node_info_decode["remote_desktop_count"]
                    # print remote_desktop_count
                    for i in remote_desktop_count:
                        node_info_encode["remote_desktop_count"] = str(remote_desktop_count[i])

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
                        node_info_encode["disk_percent"] = self._get_str_between(disk_usage[i], "percent=", ")").encode(
                            "utf-8")

                    node_info_encode["net_io_sent"] = self._calculate_net_speed(net_io_sent[0], net_io_sent[1])

                    node_info_encode["net_io_recv"] = self._calculate_net_speed(net_io_recv[0], net_io_recv[1])

                    node_info_encode["ip"] = node.encode("utf-8")
                    is_server = node_info_decode["is_server"]
                    for i in is_server:
                        node_info_encode["is_server"] = str(is_server[i])

                    res[node.encode("utf-8")] = json.dumps(node_info_encode)
                    # print node_info_encode
        except KazooException:
            print "No Children Node for the Machine!"

        # print json.dumps(res)
        return json.dumps(res)

    def get_cpu_info_of(self, ip):
        """Get the CPU info of the virtual machine of the given ip"""
        res_cpu = dict()
        total_info = self.get_total_info_of(ip)
        # print total_info
        if total_info:
            res_cpu["ip"] = ip.encode("utf-8")
            cpu_percent = total_info["cpu_percent"]
            cpu_times_percent = total_info["cpu_times_percent"]
            cpu_percent_average = total_info["cpu_percent_average"]
            is_server = total_info["is_server"]

            for i in is_server:
                res_cpu["is_server"] = str(is_server[i])

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

        # print json.dumps(res_cpu)
        return json.dumps(res_cpu)

    def get_memory_info_of(self, ip):
        """Get the CPU info of the machine of the given ip"""
        res_mem = dict()
        total_info = self.get_total_info_of(ip)
        if total_info:
            res_mem["ip"] = ip.encode("utf-8")
            swap_memory = total_info["swap_memory"]
            virtual_memory = total_info["virtual_memory"]
            is_server = total_info["is_server"]

            # print swap_memory
            # print virtual_memory

            for i in is_server:
                res_mem["is_server"] = str(is_server[i])

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

        # print json.dumps(res_mem)
        return json.dumps(res_mem)

    def get_disk_info_of(self, ip):
        """Get the Disk info of the machine of the given ip"""
        res_disk = dict()
        total_info = self.get_total_info_of(ip)
        if total_info:
            res_disk["ip"] = ip.encode("utf-8")
            disk_usage = total_info["disk_usage"]
            disk_io = total_info["disk_io"]
            is_server = total_info["is_server"]
            # print disk_usage
            # print disk_io

            for i in is_server:
                res_disk["is_server"] = str(is_server[i])

            for i in disk_io[1]:
                res_disk["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i))).encode("utf-8")

            for i in disk_usage:
                i_total = self._get_str_between(disk_usage[i], "total=", ", used")
                i_used = self._get_str_between(disk_usage[i], "used=", ", free")
                i_free = self._get_str_between(disk_usage[i], "free=", ", percent")
                i_percent = self._get_str_between(disk_usage[i], "percent=", ")")

                res_disk["disk_total"] = self._get_converted_value(i_total, 3)
                res_disk["disk_used"] = self._get_converted_value(i_used, 3)
                res_disk["disk_free"] = self._get_converted_value(i_free, 3)
                res_disk["disk_percent"] = i_percent.encode("utf-8")

            res_disk["disk_read_speed"], res_disk["disk_write_speed"] = self._calculate_disk_speed(disk_io[0], disk_io[1])
            # print res_disk

        return json.dumps(res_disk)

    def get_net_info_of(self, ip):
        """Get the Net info of the machine of the given ip"""
        res_net = dict()
        total_info = self.get_total_info_of(ip)
        if total_info:
            res_net["ip"] = ip.encode("utf-8")
            net_io_sent = total_info["net_io_sent"]
            net_io_recv = total_info["net_io_recv"]
            is_server = total_info["is_server"]
            # print net_io_sent
            # print net_io_recv

            for i in is_server:
                res_net["is_server"] = str(is_server[i])

            for i in net_io_sent[1]:
                res_net["net_total_sent"] = net_io_sent[1][i].encode("utf-8")
                res_net["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i))).encode("utf-8")

            for i in net_io_recv[1]:
                res_net["net_total_recv"] = net_io_recv[1][i].encode("utf-8")

            res_net["net_sent_speed"] = self._calculate_net_speed(net_io_sent[0], net_io_sent[1])
            res_net["net_recv_speed"] = self._calculate_net_speed(net_io_recv[0], net_io_recv[1])

            # print res_net

        return json.dumps(res_net)

    def get_daemon_info_of(self, ip):
        """Get the Daemon info of the machine of the given ip"""
        res_daemon = dict()
        node_path = self.vms_daemon_node + self.slash + str(ip)
        try:
            total_info = self._get_node_info(node_path)
            # print total_info
            return total_info

        except KazooException:
            return json.dumps(res_daemon)


if __name__ == "__main__":
    gi = ResourceInfo()
    gi.start_zk()
    # gi.get_vms_static_info()
    gi.get_general_dynamic_info()
    # gi.get_cpu_info_of("172.18.229.251")
    # gi.get_memory_info_of("172.18.229.251")
    # gi.get_disk_info_of("172.18.229.251")
    # gi.get_net_info_of("192.168.231.142")
    # gi.get_daemon_info_of("172.18.229.251")
    # a = gi.get_total_cpu_count()
    # print a

    # gi.get_daemon_info_of("192.168.231.142")

