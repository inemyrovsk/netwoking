import netmiko
# commands=['configure terminal', 'dist-rtr01', 'enable secret class', 'line console 0',
#           'password cisco', 'login', 'exit', 'line vty 0 4', 'password cisco', 'login', 'exit',
#           'service password-encryption', 'banner motd $ Authorized Access Only! $', 'end', 'copy running-config startup-config']

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.175',
        'type': 'ios',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
        'node': 'dist-rtr01',
        'loopback_name': 'Loopback0',
        'loopback_ip': '10.0.0.1'
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.176',
        'type': 'ios',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
        'node': 'dist-rtr02',
        'loopback_name': 'Loopback1',
        'loopback_ip': '10.0.0.2'
    },
    # {
    #     'device_type': 'cisco_ios',
    #     'host': '10.10.20.177',
    #     'type': 'nxos',
    #     'username': 'cisco',
    #     'password': 'cisco',
    #     'secret': 'cisco',
    #     'port': 22,
    #     'node': 'dist-sw01',
    #     'loopback_name': 'Loopback2',
    #     'loopback_ip': '10.0.0.3'
    # },
    # {
    #     'device_type': 'cisco_ios',
    #     'host': '10.10.20.178',
    #     'type': 'nxos',
    #     'username': 'cisco',
    #     'password': 'cisco',
    #     'secret': 'cisco',
    #     'port': 22,
    #     'node': 'dist-sw02',
    #     'loopback_name': 'Loopback3',
    #     'loopback_ip': '10.0.0.4'
    # }
]


def conf_int():
    loopback_name = []
    loopback_ip = []
    loopback_status = []
    for device in devices:
        connection = netmiko.ConnectHandler(ip=device["host"], device_type="cisco_ios", username='cisco',
                                            password="cisco")
        connection.enable()
        connection.config_mode()
        commands = ['configure terminal', f'interface {device["loopback_name"]}',
                    f'ip address {device["loopback_ip"]} 255.255.255.0', 'exit']
        connection.send_config_set(commands)
        int_loopback = connection.send_command(f'show ip int brief | include {device["loopback_name"]}').split()
        print(int_loopback)
        loopback_name.append(int_loopback[0])
        loopback_ip.append(int_loopback[1])
        loopback_status.append(" ".join(int_loopback[2:6]))
        connection.disconnect()
    print(loopback_name)
    print(loopback_ip)
    print(loopback_status)
    iterations = len(loopback_name)
    print(iterations)
    return [loopback_name, loopback_ip, loopback_status, iterations]


# conf int
# no interface loopback 1

if __name__ == '__main__':
    conf_int()
