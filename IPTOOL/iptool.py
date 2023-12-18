from netaddr import IPNetwork,IPAddress,IPRange,IPSet
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

def ipParse(ipStr):
    ipList = re.split(r'[^\d\.\-~/]',ipStr)
    
    # 四种ip地址输入格式
    # IP地址
    ## 10.1.1.2
    ip_pattern =re.compile(r'^(((25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d))$')
    # IP掩码
    ## 10.1.1.2/31
    ip_cidr_pattern = re.compile(r'^(((25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)/(3[0-2]|[12]?\d))$')
    # IP范围1
    ## 10.1.1.2-10.1.1.3   10.1.1.2～10.1.1.3
    ip_range_pattern1 = re.compile(r'^(((25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)(\-|~)((25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d))$')
    # IP范围2 10.1.1.2～3   10.1.1.2-3
    ip_range_pattern2 = re.compile(r'^(((25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)(\-|~)(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d))$')
    
    ip_set = IPSet()
    
    for i in ipList:
        if re.match(ip_pattern,i):
            ip_set.add(IPNetwork(i+"/32"))
        elif re.match(ip_cidr_pattern,i):
            ip_set.add(IPNetwork(i))
        elif re.match(ip_range_pattern1,i):
            tempStr1 = re.split(r'[~\-]',i)
            ip_range = IPRange(tempStr1[0],tempStr1[1])
            ip_set.add(ip_range)               
        elif re.match(ip_range_pattern2,i):
            tempStr2 = re.split(r'[\-~\.]',i)
            ip_range = IPRange(".".join(tempStr2[0:4]),".".join(tempStr2[0:3]+[tempStr2[-1]]))
            ip_set.add(ip_range)
        else:
            raise ValueError("错误的IP地址格式: {}".format(i))
    
    return ip_set


# 输入ip地址范围
def iprangeStr_To_cidrStr(ipStr):
    try:
        ip_set = ipParse(ipStr)
    except ValueError as v:
        raise ValueError(v)
    
    return ','.join(str(i) for i in ip_set.iter_cidrs())
    


def cidrStr_To_iprangeStr(ipStr):
    try:
        ip_set = ipParse(ipStr)
    except ValueError as v:
        raise ValueError(v)
    
    return ','.join(str(i) for i in ip_set.iter_ipranges())
    
def ipsetStr_and(ipsetStr_a,ipsetStr_b):
    try:
        ip_set_a = ipParse(ipsetStr_a)
        ip_set_b = ipParse(ipsetStr_b)
    except ValueError as v:
        raise ValueError(v)
    
    return ','.join([str(i) for i in (ip_set_a & ip_set_b).iter_cidrs()])


def ipsetStr_or(ipsetStr_a,ipsetStr_b):
    try:
        ip_set_a = ipParse(ipsetStr_a)
        ip_set_b = ipParse(ipsetStr_b)
    except ValueError as v:
        raise ValueError(v)
    
    return ','.join([str(i) for i in (ip_set_a | ip_set_b).iter_cidrs()])
    
    

def ipsetStr_not(ipsetStr_a,ipsetStr_b):
    try:
        ip_set_a = ipParse(ipsetStr_a)
        ip_set_b = ipParse(ipsetStr_b)
    except ValueError as v:
        raise ValueError(v)
    
    return ','.join([str(i) for i in (ip_set_a - ip_set_b).iter_cidrs()])


# print(subnets_not("192.168.1.10-99","192.168.1.20-192.168.1.199"))
# print(ipsetStr_not("192.168.1.1,192.168.1.4/31 10.1.1.1-9;10.1.1.13-10.1.1.23\n1.1.1.1,1.1.1.2/30,178.1.244.1","10.1.1.13-10.1.1.23"))