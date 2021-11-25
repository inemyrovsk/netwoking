export ANSIBLE_HOST_KEY_CHECKING=False
echo [lab-router] > hosts
echo 10.10.20.17[5:6] >> hosts
echo [lab-sw] >> hosts
echo 10.10.20.17[7:8] >> hosts
echo [all:vars] >> hosts
echo ansible_user=cisco >> hosts
echo ansible_ssh_pass=cisco >> hosts
echo ansible_network_os=ios >> hosts
echo ansible_connection=network_cli >> hosts
echo "Host file configuration done"
echo --- > config.yaml
echo "- hosts: lab-sw" >> config.yaml
echo "  gather_facts: false" >> config.yaml
echo "  tasks:" >> config.yaml
echo "    - name: Configure logging for switches" >> config.yaml
echo "      ios_config:" >> config.yaml
echo "        lines:" >> config.yaml
echo "          - logging server 192.168.90.23" >> config.yaml
echo "          - logging module 4" >> config.yaml
echo "          - logging level aaa 2" >> config.yaml
echo "          - logging timestamp milliseconds" >> config.yaml
echo "          - logging source-interface Loopback0" >> config.yaml
echo "        save_when: modified" >> config.yaml
echo "- hosts: lab-router" >> config.yaml
echo "  gather_facts: false" >> config.yaml
echo "  tasks:" >> config.yaml
echo "    - name: Configure logging for router" >> config.yaml
echo "      ios_config:" >> config.yaml
echo "        lines:" >> config.yaml
echo "          - logging host 192.168.90.23" >> config.yaml
echo "          - logging trap 4" >> config.yaml
echo "          - logging on" >> config.yaml
echo "        save_when: modified" >> config.yaml
echo "Config for playbook created"
ansible-playbook config.yaml -i hosts
echo "Ansible tasks Done"