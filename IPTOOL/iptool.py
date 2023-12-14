from netaddr import IPNetwork,IPAddress,iprange_to_cidrs
import re

def ip_to_subnetlist(ip_str):
    # subnetlist = [prefix_len,mask,host_mask,iprange,subnet_id,broadcast_ip,size]
    subnetlist = []
    in_ip = IPNetwork(ip_str)
    for i in range(32,0,-1):
        ip_network = IPNetwork(ip_str+"/"+str(i))
        # 掩码
        mask = str(ip_network.netmask)
        # 反掩码
        host_mask = str(ip_network.hostmask)
        iprange = str(IPAddress(ip_network.first)) + "-" + str(IPAddress(ip_network.last))
        subnet_id = str(ip_network.network)
        broadcast_ip = str(ip_network.broadcast)
        network_size = ip_network.size
        subnetlist.append([str(i),mask,host_mask,iprange,subnet_id,broadcast_ip,str(network_size)])
    return subnetlist


# 允许的IP格式：
## 10.1.1.2
## 10.1.1.2-3
## 10.1.1.2～3
## 10.1.1.2-10.1.1.3
## 10.1.1.2～10.1.1.3
## 10.1.1.2/31



def if_input_right(ip):
    pattern = re.compile(r'(^(\d+\.){3}\d+$)|(^(\d+\.){3}\d+(\-|~)\d+$)|(^(\d+\.){3}\d+(\-|~)(\d+\.){3}\d+$)|(^(\d+\.){3}\d+/([0-2]\d?|3[0-2])$)')
    return re.match(pattern,ip)

# 输入ip地址范围
def iprangeStr_To_cidrStr(iprangeStr):
    iprange = re.split(r'[^\d\.\-~/]',iprangeStr)
    for i in iprange:
        if if_input_right(i):
            pass
        else:
            raise ValueError("错误的IP地址格式: {}".format(i))


def cidrStr_To_iprangeStr(cidr):
    pass

def subnets_and(subnets_a,subnets_b):
    pass

def subnets_or(subnets_a,subnets_b):
    pass

def subnets_not(subnets_a,subnets_b):
    pass

try:
    iprangeStr_To_cidrStr("192.168.192.1-192.168.192.9,192.168.192.123-129\n192.168.192.0/33,192.168.192.25~192.168.192.28,100.100.1.1~100")
except ValueError as v:
    print(v)