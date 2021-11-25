import netmiko

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.175',
        'type': 'ios',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
        'node': 'dist-rtr01'
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.176',
        'type': 'ios',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
        'node': 'dist-rtr02'
    },
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


def show_sw_info():
    for device in devices:
        if device['host'].endswith('7') or device['host'].endswith('8'):
            connection = netmiko.ConnectHandler(ip=device['host'], device_type="cisco_ios", username='cisco',
                                                password="cisco")
            connection.enable()
            serial_info = []
            version_info = []
            cpu_info = []
            memory_info = []
            device_name = device['node']
            hardware = connection.send_command('show hardware')
            list_hardware = hardware.split()
            for i in list_hardware:
                if i == 'Serial':
                    serial = list_hardware.index(i) + 3
                    serial_info.append(str(list_hardware[serial]))
                    print("Serial: " + serial_info[0])
                    break
            for i in list_hardware:
                if i == 'NXOS:':
                    version = list_hardware.index(i) + 2
                    version_info.append(str(list_hardware[version]))
                    print("Software version: " + version_info[0])
                    break
            for i in list_hardware:
                if i == 'Processor':
                    cpu = list_hardware.index(i) - 12
                    cpu_info.append((" ".join(list_hardware[cpu:105])))
                    print("CPU: " + cpu_info[0])
            for i in list_hardware:
                if i == 'bootflash:':
                    memory = list_hardware.index(i) + 1
                    memory_info.append(" ".join(list_hardware[memory:120]))
                    print("Memory: " + memory_info[0])

            return [serial_info[0], version_info[0], cpu_info[0], memory_info[0], device_name]


def show_rtr_info():
    connection = netmiko.ConnectHandler(ip="10.10.20.175", device_type="cisco_ios", username='cisco',
                                        password="cisco")
    connection.enable()
    data = connection.send_command('show version').split("\n")
    rtr_device_name ="dist-rtr01"
    software_version_list = data[0].split(" ")
    software_version = software_version_list[5]
    uptime_list = data[21].split('is')
    uptime = uptime_list[2]
    processor_info_list = data[52].split(" ")
    processor_info = processor_info_list[1]
    processor_id_list = data[53].split(" ")
    processor_id = processor_id_list[3]
    memory_list = data[57].split(" ")[0].replace("K", "")
    memory_mb = str(int(memory_list) * 0.001) + " mb"

    print("device: dist-rtr01")
    print("Cisco IOS XE Software: Version " + software_version)
    print("Uptime for this control processor is " + uptime)
    print("CPU name: " + processor_info + " " + "CPU ID " + processor_id)
    print(memory_mb + "MB physical memory.")
    connection.disconnect()
    return [rtr_device_name, software_version, uptime, processor_info, processor_id, memory_mb]


if __name__ == '__main__':
    show_sw_info()
    show_rtr_info()