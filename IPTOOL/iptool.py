from netaddr import IPNetwork,IPAddress

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