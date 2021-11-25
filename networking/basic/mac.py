import netmiko

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.177',
        'type': 'nxos',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
        'node': 'dist-sw01'
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.178',
        'type': 'nxos',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
        'node': 'dist-sw02'
    }]

try:
    for device in devices:
        connection = netmiko.ConnectHandler(ip=device['host'], device_type="cisco_ios", username='cisco',
                                            password="cisco")
        connection.enable()
        mac_address_table = connection.send_command("show mac address")
        print(mac_address_table)
        connection.disconnect()
except EOFError:
    print('Can not connect to device')

