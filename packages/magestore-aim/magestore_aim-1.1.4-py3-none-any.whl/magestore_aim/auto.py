# -*- coding: utf-8 -*-

import calendar
import os
import re
import time
from fabric import Connection, Config, transfer
from invoke import UnexpectedExit

MAGENTO_VERSION = ''
SAMPLE_DATA = ''
PHP_VERSION = ''

LOCAL_USER = ''
LOCAL_PASSWORD = ''
LOCAL_SOURCE_PATH = ''
LOCAL_ENV_PATH = ''
LOCAL_CON = ''
LOCAL_SUDO_CON = ''

BACKUP_SOURCE_PATH = ''
BACKUP_ADDRESS = ''
BACKUP_USER = ''
BACKUP_PASSWORD = ''
BACKUP_CON = ''
BACKUP_SUDO_CON = ''

ENV_FOLDER_PATH = ''
ENV_FOLDER_NAME_WITH_TIMESTAMP = ''
DEFAULT_PORT_RANGE = ''


def get_sudo_connection(host, user, su_pass):
    config = Config(overrides={'sudo': {'password': su_pass, "prompt": "[sudo] password: \n"}})
    c = Connection(host, user, connect_kwargs={"password": su_pass}, config=config)
    return c


def prepare_environment_variables(env_params, server_params, git_credential_file):
    global MAGENTO_VERSION, SAMPLE_DATA, PHP_VERSION
    global LOCAL_USER, LOCAL_PASSWORD, LOCAL_SOURCE_PATH, LOCAL_ENV_PATH, LOCAL_CON, LOCAL_SUDO_CON
    global BACKUP_SOURCE_PATH, BACKUP_ADDRESS, BACKUP_USER, BACKUP_PASSWORD, BACKUP_CON, BACKUP_SUDO_CON
    global ENV_FOLDER_PATH, ENV_FOLDER_NAME_WITH_TIMESTAMP, DEFAULT_PORT_RANGE

    MAGENTO_VERSION = env_params.get('MAGENTO_VERSION')
    SAMPLE_DATA = env_params.get('SAMPLE_DATA')
    PHP_VERSION = env_params.get('PHP_VERSION')

    LOCAL_USER = server_params.get('USER')
    LOCAL_PASSWORD = server_params.get('PASSWORD')
    LOCAL_SOURCE_PATH = '/home/%s/magento/sources' % LOCAL_USER
    LOCAL_ENV_PATH = '/home/%s/magento/docker' % LOCAL_USER
    LOCAL_CON = Connection('localhost')
    LOCAL_SUDO_CON = get_sudo_connection('localhost', LOCAL_USER, LOCAL_PASSWORD)

    BACKUP_SOURCE_PATH = server_params.get('BACKUP_SOURCE_PATH')
    BACKUP_ADDRESS = server_params.get('BACKUP_ADDRESS')
    BACKUP_USER = server_params.get('BACKUP_USER')
    BACKUP_PASSWORD = server_params.get('BACKUP_PASSWORD')
    BACKUP_CON = Connection(BACKUP_ADDRESS, BACKUP_USER, connect_kwargs={'password': BACKUP_PASSWORD})
    BACKUP_SUDO_CON = get_sudo_connection(BACKUP_ADDRESS, BACKUP_USER, BACKUP_PASSWORD)

    ENV_FOLDER_PATH, ENV_FOLDER_NAME_WITH_TIMESTAMP = create_docker_compose_folder(git_credential_file)
    DEFAULT_PORT_RANGE = [9100, 9101, 9102]


def current_timestamp():
    return calendar.timegm(time.gmtime())


def docker_components_installed():
    try:
        LOCAL_SUDO_CON.sudo('docker --version')
        LOCAL_SUDO_CON.sudo('docker-compose --version')
        return True
    except Exception as e:
        print(e)
        return False


def install_docker_components():
    if not docker_components_installed():
        bash_script = """
        #!/bin/bash
        apt-get install -y \
           apt-transport-https \
           ca-certificates \
           curl \
           software-properties-common
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        apt-key fingerprint 0EBFCD88
        add-apt-repository \
          "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) \
          stable"
        apt-get update
        apt-get install docker-ce -y
        groupadd docker
        # Install docker-compose
        curl -L \
           "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" \
           -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        """

        bash_file_name = '%s_install_docker.sh' % current_timestamp()
        bash_file = os.path.abspath(bash_file_name)
        with open(bash_file, 'w+') as bf:
            bf.write(bash_script)
        LOCAL_SUDO_CON.sudo('bash %s' % bash_file)
        LOCAL_SUDO_CON.sudo('rm -rf %s' % bash_file)
        LOCAL_SUDO_CON.sudo('usermod -aG docker %s' % LOCAL_USER)


def set_git_credential_command(git_credential_file):
    set_credential_command = "export HOME=/home/%s;git config --global credential.helper 'store --file %s'" % (LOCAL_USER, git_credential_file)
    return set_credential_command


def remove_git_credential():
    LOCAL_CON.local("export HOME=/home/%s;git config --global --unset credential.helper" % LOCAL_USER)


def get_remote_file(remote_path, local_path, remote_con):
    transfer_obj = transfer.Transfer(remote_con)
    transfer_obj.get(remote_path, local_path)
    print('Copied %s from remote server' % local_path)


def get_source_name():
    src_name = '%s_sample_data.tar.gz' if SAMPLE_DATA else '%s.tar.gz'
    return src_name % MAGENTO_VERSION


def get_source_file():
    """
    Prepare magento source file in folder /home/$USER/magento/sources
    :param
    :return: magento source file path
    """
    if not os.path.isdir(LOCAL_SOURCE_PATH):
        LOCAL_CON.local('mkdir -p %s' % LOCAL_SOURCE_PATH)
    source_name = get_source_name()
    local_source_file_path = (LOCAL_SOURCE_PATH + '/' + source_name).replace('//', '/')
    if not os.path.isfile(local_source_file_path):
        backup_source_file_path = (BACKUP_SOURCE_PATH + '/' + source_name).replace('//', '/')
        get_remote_file(backup_source_file_path, local_source_file_path, BACKUP_CON)

    return local_source_file_path


def create_docker_compose_folder(git_credential_file):
    """
    Clone env folder
    :return: local env folder path
    """
    if not os.path.isdir(LOCAL_ENV_PATH):
        LOCAL_CON.local('mkdir -p %s' % LOCAL_ENV_PATH)
    env_folder_name = 'Apache2-Mysql5.7-PHP%s' % PHP_VERSION
    env_folder_name_with_timestamp = '%s-%s' % (env_folder_name, current_timestamp())
    env_folder_path = ('%s/%s' % (LOCAL_ENV_PATH, env_folder_name_with_timestamp)).replace('//', '/')
    set_credential_command = set_git_credential_command(git_credential_file)
    clone_command = 'git clone https://github.com/Magestore/go-environment --depth 1 -b magento2.2.x %s' % env_folder_path
    LOCAL_CON.local(set_credential_command + '&&' + clone_command)
    LOCAL_CON.local('cd %s && git filter-branch --prune-empty --subdirectory-filter %s HEAD' % (env_folder_path, env_folder_name))

    remove_git_credential()

    return env_folder_path, env_folder_name_with_timestamp


def prepare_source_folder():
    source_file_path = get_source_file()
    src_path = ('%s/%s' % (ENV_FOLDER_PATH, 'src')).replace('//', '/')
    LOCAL_CON.local('mkdir -p %s' % src_path)
    LOCAL_CON.local('tar -xf %s -C %s' % (source_file_path, src_path))
    LOCAL_SUDO_CON.sudo('chown -R 1000:1000 %s' % src_path)
    LOCAL_SUDO_CON.sudo('chmod +x %s/bin/magento' % src_path)

    return src_path


def check_available_port_range(list_ports):
    try:
        command = 'netstat -anp tcp| grep LISTEN | grep -c ' + ' '.join(['-e ' + str(x) for x in list_ports])
        LOCAL_SUDO_CON.sudo(command)
        return False
    except (UnexpectedExit, Exception) as e:
        # raise exception when command has stdout = 0
        print(e)
        return True


def get_port_range():
    for x in range(DEFAULT_PORT_RANGE[0], 65535, 3):
        ports = [x, x + 1, x + 2]
        if check_available_port_range(ports):
            return ports
    return []


def update_docker_compose_ports():
    """
    Update available ports in docker-compose file
    :return: web port - magento access port
    """
    ports = get_port_range()
    web_port = ports[0]
    db_port = ports[1]
    phpmyadmin_port = ports[2]
    docker_compose_path = (ENV_FOLDER_PATH + '/' + 'docker-compose.yml').replace('//', '/')
    with open(docker_compose_path, 'r') as dc:
        docker_compose_content = dc.read()
    # docker_compose_content = LOCAL_CON.local("cat %s" % docker_compose_path).stdout
    # replace correct ports
    correct_ports = {'9100': web_port, '9101': db_port, '9102': phpmyadmin_port}
    for key in correct_ports:
        docker_compose_content = docker_compose_content.replace(key, str(correct_ports[key]))
    with open(docker_compose_path, 'w') as docker_writer:
        docker_writer.write(docker_compose_content)
    return web_port


def get_local_ip_address():
    bash_script = """
    #!/bin/bash
    network_interface=`ifconfig |grep enp | awk '{gsub (":", "");print $1}'`
    ip_address=`ifconfig $network_interface | grep inet | grep -Eo '([0-9]*\.){3}[0-9]*' | awk '{print$1; exit}'`
    printf $ip_address
    """
    bash_file_name = '%s_get_ip.sh' % current_timestamp()
    bash_file = os.path.abspath(bash_file_name)
    try:
        with open(bash_file, 'w+') as bf:
            bf.write(bash_script)
        ip_address = LOCAL_SUDO_CON.sudo('bash %s' % bash_file).stdout.replace('\n', '')
        LOCAL_SUDO_CON.sudo('rm -rf %s' % bash_file)
        return ip_address
    except Exception as e:
        print(e)
        return False


def update_env_docker_compose_params():
    web_port = update_docker_compose_ports()
    local_ip_address = get_local_ip_address()
    env_file_path = (ENV_FOLDER_PATH + '/' + 'env').replace('//', '/')
    env_content = open(env_file_path, 'r').readlines()
    open(env_file_path, 'w').write('')
    env_file = open(env_file_path, 'a')
    for line in env_content:
        if 'MAGENTO_URL' in line:
            line = 'MAGENTO_URL=http://%s:%s\n' % (local_ip_address, web_port)
        env_file.write(line)
    env_file.close()


def get_instance_url():
    env_file_path = (ENV_FOLDER_PATH + '/' + 'env').replace('//', '/')
    with open(env_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'MAGENTO_URL' in line:
                return line.split('=')[-1].replace('\n', '')
    return ''


def docker_compose_up():
    update_env_docker_compose_params()
    compose_file = '%s/docker-compose.yml' % ENV_FOLDER_PATH
    LOCAL_SUDO_CON.sudo('docker-compose -f %s up -d' % compose_file)


def get_container_id(container_pattern):
    prefix_container_name = ENV_FOLDER_NAME_WITH_TIMESTAMP.lower().replace('.', '')
    cur_time = current_timestamp()
    command = "docker ps --format \"table {{.ID}}\\t{{.Names}}\" | awk  '{if ($2 ~ \"%s%s\") {print $1}}'" % (prefix_container_name, container_pattern)
    bash_file = '%s.sh' % cur_time
    with open(bash_file, 'w+') as f:
        f.write(command)
        bash_file_path = os.path.abspath(bash_file)
    out = LOCAL_SUDO_CON.sudo('bash %s' % bash_file_path).stdout
    container_id = re.sub(r'\W+', '', out)
    LOCAL_CON.local('rm %s' % bash_file_path)
    return container_id


def check_docker_compose_services_status():
    """
    Check status of all services in docker-compose file.
    Only run install-mangento when all services are healthy
    :return: True if all services are healthy, otherwise False
    """
    try:
        web_container_id = get_container_id('_web_')
        db_container_id = get_container_id('_db_')
        command = 'docker ps --filter "health=healthy"|egrep -c "%s|%s"' % (web_container_id, db_container_id)
        result = LOCAL_SUDO_CON.sudo(command)
        return True if result.stdout.replace('\n', '') == '2' else False
    except (UnexpectedExit, Exception) as e:
        # this throw exception when above command return 0 value
        return False


def get_phpmyadmin_url():
    docker_compose_path = (ENV_FOLDER_PATH + '/' + 'docker-compose.yml').replace('//', '/')
    phpmyadmin_port = ''
    instance_url = get_instance_url()
    ip_address = re.sub('[^0-9.]', '', instance_url.split(':')[1])

    with open(docker_compose_path, 'r') as fl:
        lines = fl.readlines()
        for index, line in enumerate(lines):
            if index - 2 > 0 and 'phpmyadmin/' in lines[index - 2]:
                phpmyadmin_port = re.sub('[^0-9]', '', line.split(':')[0])
                break
    return '%s:%s' % (ip_address, phpmyadmin_port)


def magento_instance_info():
    url = get_instance_url()
    phpmyadmin_url = get_phpmyadmin_url()
    result = {
        'url': url,
        'admin_url': url + '/admin',
        'phpmyadmin_url': phpmyadmin_url,
        'admin_user': 'admin',
        'admin_password': 'admin123@',
        'db_user': 'magento',
        'db_password': 'magento'
    }
    return result


def execute_install_command():
    retries = 10
    timeout = 20
    while retries != 0:
        healthy = check_docker_compose_services_status()
        if healthy:
            break
        retries -= 1
        print('Are services healthy? No')
        time.sleep(timeout)
    if retries == 0:
        print('Something went wrong! Try again later')
        return False
    print('All services are healthy and ready to install magento')
    try:
        web_container_id = get_container_id('_web_')
        LOCAL_SUDO_CON.sudo('docker exec -i {web_container_id} install-magento'.format(web_container_id=web_container_id))
        if SAMPLE_DATA != '0':
            LOCAL_SUDO_CON.sudo('docker exec -i {web_container_id} install-sampledata'.format(web_container_id=web_container_id))
        return True
    except Exception as e:
        print(e)
        return False


def install_magento(env_params, server_params, git_credential_file):
    """
    MAIN function.
    Install magento with defined params
    :param env_params: dict params for magento requirements
    :param server_params: dict params for local and backup server info
    :param git_credential_file: path to .git-credentials file
    :return:
    """
    prepare_environment_variables(env_params, server_params, git_credential_file)
    install_docker_components()
    prepare_source_folder()
    docker_compose_up()
    done = execute_install_command()

    return magento_instance_info() if done else 'Something went wrong, please try again.'
