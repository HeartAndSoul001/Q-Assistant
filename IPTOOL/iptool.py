from netaddr import IPNetwork,IPAddress,IPRange,IPSet,cidr_merge,iprange_to_cidrs
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

# 输入ip地址范围
def iprangeStr_To_cidrStr(iprangeStr):
    iprange = re.split(r'[^\d\.\-~/]',iprangeStr)
    
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
    
    result_cidrList = []
    
    for i in iprange:
        print(i)
        if re.match(ip_pattern,i):
            result_cidrList.append(IPNetwork(i+"/32"))
            print("0")
        elif re.match(ip_cidr_pattern,i):
            result_cidrList.append(IPNetwork(i))
            print("1")
        elif re.match(ip_range_pattern1,i):
            tempStr1 = re.split(r'[~\-]',i)
            ip_to_cidrList2 = iprange_to_cidrs(IPAddress(tempStr1[0]),IPAddress(tempStr1[1]))
            result_cidrList += ip_to_cidrList2
                       
        elif re.match(ip_range_pattern2,i):
            tempStr2 = re.split(r'[\-~\.]',i)
            iprange_start = ".".join(tempStr2[0:4])
            iprange_end = ".".join(tempStr2[0:3]+[tempStr2[-1]])
            ip_to_cidrList1 = iprange_to_cidrs(IPAddress(iprange_start),IPAddress(iprange_end))
            result_cidrList += ip_to_cidrList1
        else:
            print("4")
            raise ValueError("错误的IP地址格式: {}".format(i))
        print("\n")
    result_cidrListStr = "\n".join([str(k) for k in cidr_merge(result_cidrList)])
    return result_cidrListStr


def cidrStr_To_iprangeStr(cidr):
    ip_cidr = re.split(r'[^\d\.\-~/]',cidr)
    
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
    
    result_ipSet = IPSet()
    
    for i in ip_cidr:
        if re.match(ip_pattern,i):
            result_ipSet.append(IPAddress(i))
        elif re.match(ip_cidr_pattern,i):
            result_ipSet.append(IPNetwork(i))
        elif re.match(ip_range_pattern1,i):
            pass
            # tempStr1 = re.split(r'[\-~\.]',i)
            # iprange_start = ".".join(tempStr1[0:4])
            # iprange_end = ".".join(tempStr1[0:3]+[tempStr1[-1]])
            # ip_to_cidrList1 = iprange_to_cidrs(IPAddress(iprange_start),IPAddress(iprange_end))
            # result_cidrList += ip_to_cidrList1
                       
        elif re.match(ip_range_pattern2,i):
            pass
            # tempStr2 = re.split(r'[~\-]',i)
            # ip_to_cidrList2 = iprange_to_cidrs(IPAddress(tempStr2[0]),IPAddress(tempStr2[1]))
            # result_cidrList += ip_to_cidrList2
        else:
            raise ValueError("错误的IP地址格式: {}".format(i))
    
    
    

def subnets_and(subnets_a,subnets_b):
    pass

def subnets_or(subnets_a,subnets_b):
    pass

def subnets_not(subnets_a,subnets_b):
    pass

try:
    iprangeStr_To_cidrStr("192.168.192.1-192.168.192.9,192.168.192.123-129\n192.168.192.0/22,192.168.192.25~192.168.192.28,100.100.1.1~100 192.168.1.1 1.1.1.1/32")
except ValueError as v:
    print(v)