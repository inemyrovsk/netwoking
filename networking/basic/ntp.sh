export ANSIBLE_HOST_KEY_CHECKING=False
echo [lab] > hosts
echo 10.10.20.17[5:8] >> hosts
echo [all:vars] >> hosts
echo ansible_user=cisco >> hosts
echo ansible_ssh_pass=cisco >> hosts
echo ansible_network_os=ios >> hosts
echo ansible_connection=network_cli >> hosts
echo "Host file configuration done"
echo --- > config.yaml
echo "- hosts: lab" >> config.yaml
echo "  gather_facts: false" >> config.yaml
echo "  tasks:" >> config.yaml
echo "    - name: Configure NTP" >> config.yaml
echo "      ios_config:" >> config.yaml
echo "        lines:" >> config.yaml
echo "          - ntp server 91.236.251.5" >> config.yaml
echo "        save_when: modified" >> config.yaml
echo "Config for playbook created"
ansible-playbook config.yaml -i hosts
echo "TASKS COMPLETED"
