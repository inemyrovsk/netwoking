from flask import Flask, request, render_template
import netmiko
from networking.basic.gather import *
from networking.basic.interfaces import conf_int

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


def connect_to_sw():
    for device in devices:
        if device['host'].endswith('7') or device['host'].endswith('8'):
            connection = netmiko.ConnectHandler(ip=device['host'], device_type="cisco_ios", username='cisco',
                                                password="cisco")
            connection.enable()
            return [connection, device['node']]


def gather_mac_info():
    connect_to_sw()[0].send_command('enable')
    mac_address_table = connect_to_sw()[0].send_command("show mac address")
    list_table = mac_address_table.split('\n')
    mac_table = []
    vlan = []
    mac_address = []
    age = []
    mac_type = []
    secure = []
    ntfy = []
    ports = []
    for i in list_table:
        if 'G' in i and 'F' in i:
            print(i)
            mac_table.append(i)
    for element in mac_table:
        vlan.append(element.split()[1])
        mac_address.append(element.split()[2])
        mac_type.append(element.split()[3])
        age.append(element.split()[4])
        secure.append(element.split()[5])
        ntfy.append(element.split()[6])
        ports.append(element.split()[7])
    iterations = len(vlan)
    connect_to_sw()[0].disconnect()
    return [mac_table, vlan, mac_address, age, mac_type, secure, ntfy, ports, iterations]


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/conf', methods=["GET", "POST"])
def conf_net():
    if request.method == "POST":
        url = request.form.get('url')
        username = request.form.get('username')
        password = request.form.get('password')
        if url == "https://10.10.20.161" and username == 'developer' and password == 'C1sco12345':
            return render_template('switch.html')


@app.route('/show', methods=["POST", "GET"])
def show():
    if request.method == "POST":
        if request.form['mac'] == 'Show MAC table':
            return render_template('mac.html')

    elif request.method == "GET":
        return render_template('switch.html')


@app.route('/mac.html', methods=["GET", "POST"])
def show_mac():
    try:
        mac_info = gather_mac_info()
        mac_table = mac_info[0]
        vlan = mac_info[1]
        mac_address = mac_info[2]
        age = mac_info[3]
        mac_type = mac_info[4]
        secure = mac_info[5]
        ntfy = mac_info[6]
        ports = mac_info[7]
        iterations = mac_info[8]

        return render_template('mac.html', iterations=iterations, mac=mac_table, vlan=vlan, mac_address=mac_address,
                               age=age, mac_type=mac_type, secure=secure, ntfy=ntfy, ports=ports)
    except EOFError:
        print('Can not connect to device')


@app.route('/gather', methods=["POST", "GET"])
def show_device_info():
    try:
        if request.method == "GET":

            sw_data = show_sw_info()
            sw_serial_info = sw_data[0]
            sw_version_info = sw_data[1]
            sw_cpu_info = sw_data[2]
            sw_memory_info = sw_data[3]
            sw_device_name = sw_data[4]

            rtr_data = show_rtr_info()
            rtr_device_name = rtr_data[0]
            rtr_software_version = rtr_data[1]
            rtr_uptime = rtr_data[2]
            rtr_processor_info = rtr_data[3]
            rtr_processor_id = rtr_data[4]
            rtr_memory_mb = rtr_data[5]

            return render_template('gather.html', serial_info=sw_serial_info, version_info=sw_version_info, cpu_info=sw_cpu_info, memory_info=sw_memory_info,
                                   sw_device_name=sw_device_name, rtr_device_name=rtr_device_name, software_version=rtr_software_version,
                                   uptime=rtr_uptime, processor_info=rtr_processor_info, processor_id=rtr_processor_id, memory_mb=rtr_memory_mb)
    except EOFError:
        return render_template("errorpage.html")


@app.route('/loopback', methods=["POST", "GET"])
def show_int_loopback():
    if request.method == "GET":
        loopback_data = conf_int()
        loopback_name = loopback_data[0]
        loopback_ip = loopback_data[1]
        loopback_status = loopback_data[2]
        iterations = loopback_data[3]
        return render_template('loopback.html', loopback_names=loopback_name, loopback_ips=loopback_ip,
                               loopback_statuses=loopback_status, iterations=iterations)


if __name__ == '__main__':
    app.run()
