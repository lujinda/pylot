#coding:utf8
from scapy.all import *
conf.checkIPaddr=False # 因为我们发送给255.255.255.255 ，但是如果我们能收到回复包，回复包中的源地址是其ip地址。由于请求包的目标地址和回复包中的源地址不匹配，所以我们要设置checkIPaddr=False禁用scapy检查。
f,hw=get_if_raw_hwaddr(conf.iface)  # hw等下要做为chaddr，全子网唯一。
p=Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",
        dst="255.255.255.255")/UDP(sport=68,
                dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type",
                    "discover"),"end"])
ans,unans=srp(p,multi=True,timeout=5) # multi=True可以等待更多的回复，如果没有，在接到第一个回复时，就会中止了
for s,r in ans:
    print r[Ether].src,r[IP].src


