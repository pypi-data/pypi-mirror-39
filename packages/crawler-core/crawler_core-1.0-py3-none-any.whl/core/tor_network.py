import re
import io
import os
import socket
import psutil
import shutil
import zipfile
import pandas as pd
from core import torrc
from time import sleep
from sqlalchemy import *
from datetime import datetime
from core.request import Request
from subprocess import Popen,PIPE
from stem.control import Controller
from core.thread_pool import ThreadPool

# _database is prepared instance of core>database>Database
_database = None
_table_name = 'tor_list'
_view_name = 'v_tor_list'
_base_url = 'https://www.torproject.org'
_tor_url = '{}/download/download.html'.format(_base_url)
_dip = r'C:\Users\{}\Tor'.format(os.getlogin())  # default install path
_user_path = r'C:\Users\{}'.format(os.getlogin())


def install(install_path=_dip):
    """
    :param str install_path:
    Description:
        install_path = is place where you want Tor to be instaled
            default is in Users\yourusername\Tor
    """
    if os.path.isdir(_dip):
        shutil.rmtree(_dip)

    r = Request()
    r.go(_tor_url)
    html = r.response.content
    if type(html) is dict:
        print('Unable to download tor zip package. Try again later.')
        return

    links = html.find_all('a', {'href': True, 'class': 'button'})
    expert_url = [link for link in links if re.search('Expert Bundle', link.decode()) is not None]
    if not expert_url:
        print("Unable to find Expert Bundle.")
        return
    expert_url = expert_url[0].get('href').replace('..',_base_url)

    file = r.go(expert_url, download=True)
    z = zipfile.ZipFile(io.BytesIO(file))
    z.extractall(install_path)

    with open(r'{}\tor_path.txt'.format(_user_path), 'w') as f:
        f.write(install_path)
        f.close()

    # Deploying additional directories needed for tor_network to work
    for folder in ['TorData', 'TorData\data', 'TorData\config']:
        os.mkdir(r'{}\{}'.format(_dip, folder))


def get_ipv4():
    ipv4 = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(("8.8.8.8", 80))
        ipv4 = s.getsockname()[0]
        s.close()
        return ipv4
    except:
        return ipv4


def tor_table():
    table_cols = [{'name': 'pid', 'type_': Integer},
                  {'name': 'ipv4', 'type_': String(50)},
                  {'name': 'ip', 'type_': String(50)},
                  {'name': 'port', 'type_': Integer},
                  {'name': 'control_port', 'type_': Integer},
                  {'name': 'torrc_path', 'type_': String(3000)},
                  {'name': 'pid_file', 'type_': String(3000)},
                  {'name': 'data_dir', 'type_': String(3000)}]
    _database.create_table(_table_name, table_cols)


def get_free_ports():
    ports = []
    for i in range(2):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        ports.append(tcp.getsockname()[1])
        tcp.close()
    return ports


def clean_tor():
    db_data = _database.select(_table_name)
    df = pd.DataFrame.from_dict(db_data)
    df = df[df.dat_pro.notnull()]
    for_delete = df.to_dict('records')
    ipv4 = get_ipv4()
    for row in for_delete:
        data_dir = row.get('data_dir')
        torrc_path = row.get('torrc_path')
        ipv4_db = row.get('torrc_path')
        if ipv4 == ipv4_db:
            try:
                if os.path.isdir(data_dir):
                    shutil.rmtree(data_dir)
                if os.path.exists(torrc_path):
                    os.remove(torrc_path)
                _database.delete('tor_list')
            except:
                pass



class TorControl:
    """
        Description:
        Class task is to control tor expert programs.
        - Connect python program on it so it can send requests.
        - Change identity(exit node ip) of tor expert if it is needed.
        - Close, Kill or Delete everything for connected tor instance
    """
    socket_port = None
    control_port = None

    def __init__(self):
        self.SocketOriginal = socket.socket
        self.socket_port = self.socket_port
        self.control_port = self.control_port
        self.controller = None

    def create_controller(self, address='127.0.0.1', control_port=None):
        """Creates control instance for a caller"""
        if control_port is None:
            control_port = self.control_port
        self.controller = Controller.from_port(address=address, port=control_port)

    def tor_connect(self):
        """Connects to control instance"""
        self.controller.connect()
        self.controller.authenticate()

    @staticmethod
    def is_tor_up(pid):
        """Checks is the tor expert pid running in processes"""
        if os.path.exists(pid):
            for process in psutil.process_iter():
                if process.pid == int(pid) and process.name() == 'tor.exe':
                    return True
        return False

    def kill_tor(self, pid, data_dir, torrc_path):
        """
            Kills tor expert pid in running processes.
            Deletes data from data_dir and torrc_path
        """
        for process in psutil.process_iter():
            if process.pid == int(pid) and process.name() == 'tor.exe':
                process.terminate()
        self.clear_data(data_dir, torrc_path)

    def new_identity(self):
        """Creates new identity(exit node ip) for current tor instance"""
        controller = self.controller
        new_id_status = controller.is_newnym_available()
        new_id_wait_time = controller.get_newnym_wait()
        if new_id_status:
            controller.clear_cache()
            controller.signal('NEWNYM')
        else:
            sleep(new_id_wait_time)

    def clear_socket(self):
        if socket.socket != self.SocketOriginal:
            socket.socket = self.SocketOriginal

    def shutdown_tor(self, data_dir, torrc_path):
        """Shutdowns tor expert and cleans data behind
        Deletes data from data_dir and torrc_path"""
        self.clear_socket()
        self.controller.signal('SHUTDOWN')
        sleep(30)
        self.clear_data(data_dir, torrc_path)

    @staticmethod
    def clear_data(data_dir, torrc_path):
        """Deletes data from data_dir and torrc_path"""
        if os.path.exists(torrc_path):
            os.remove(torrc_path)
        if os.path.isdir(data_dir):
            shutil.rmtree(data_dir)

    def get_pid(self, data_dir):
        pid = None
        pid_file = '{}\pid'.format(data_dir)
        if os.path.exists(pid_file):
            with open(pid_file) as f:
                pid = f.read().strip()
        return pid


class TorBuild:
    """
    Description:
    Class task is to create new instances of tor
    and save that info to the table.
    """
    def __init__(self, tormax=1):
        """database must provide an instance of core>database>Database"""
        self.tc = TorControl()
        while True:
            tor = _database.select(_table_name, filters={'dat_pro': None})
            if len(tor) >= tormax:
                break
            ports = get_free_ports()
            self.create_tor(*ports)

    def tor_remove(self, pid, data_dir, torrc_path):
        if pid is not None:
            self.tc.kill_tor(pid, data_dir, torrc_path)
        if pid is None:
            self.tc.clear_data(data_dir, torrc_path)

    def create_tor(self, socket_port, control_port, timeout=60):
        start_time = datetime.now()

        # getting tor path
        tor_file_path = r'{}\tor_path.txt'.format(_user_path)
        with open(tor_file_path, 'r') as f:
            tor_path = f.read()

        # preparing variables
        tor_exe = r'{0}\Tor\tor.exe'.format(tor_path)
        data_dir = '{0}\TorData\data\{1}'.format(tor_path, socket_port)
        torrc_path = r'{0}\TorData\config\torrc{1}.config'.format(tor_path, socket_port)

        # create tor expert directory named by socket_port if doesn't exists
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        # create torrc file
        torrc_data = torrc.make_torrc(tor_path, socket_port, control_port, get_ipv4())
        with open(torrc_path, "w") as f:
            f.write(torrc_data)

        # start instance of tor
        cmd = [tor_exe, '-f', torrc_path]
        self.p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

        while True:
            event = self.p.stdout.readline().strip()
            diff = datetime.now() - start_time
            pid = self.tc.get_pid(data_dir)
            if diff.total_seconds() > timeout:
                self.tor_remove(pid, data_dir, torrc_path)
                err = 'Too long to establish tor circuit over {0} seconds'.format(diff.seconds)
                return 401
            if re.search('Bootstrapped 100%', str(event)):
                pid_file = '{0}\TorData\data\{1}\pid'.format(tor_path, socket_port)
                new_tor = {'pid': pid, 'ipv4': get_ipv4(),
                           'ip': get_ipv4(), 'port': socket_port,
                           'control_port': control_port, 'torrc_path': torrc_path,
                           'pid_file': pid_file, 'data_dir': data_dir}
                _database.insert(_table_name, [new_tor])
                return 200
            if re.search('No route to host', str(event)):
                self.tor_remove(pid, data_dir, torrc_path)
                return 402


class TorScanner:
    """
        Description:
        This class task is to find all torrc files that you have created
        until now on your local drives. It will read data for tor expert
        and you have currently running processes of tor instances but
        don't have info what are their connection ports.
        It will delete all torrc data including files and directories
        for that tor instance data is stored. It will free your disc space.
        It will also insert data in table you specified with following columns:
    """
    def __init__(self, drives=None):
        """drives- specifiy letters of drive to check"""
        self.drives = drives
        self.tor = TorControl()
        self.opened_tors = {}
        self.torrc_scanner()
        _database.merge(_table_name, self.opened_tors, filters={'dat_pro': None})

    def torrc_scanner(self):
        dps = psutil.disk_partitions()
        if self.drives is not None:
            drives = [drive.upper()+":\\" for drive in self.drives]
        else:
            drives = [dp.device for dp in dps if dp.fstype == 'NTFS']
        pool = ThreadPool(100)
        for drive in drives:
            pool.map(self.scan_torrc, os.walk(drive))
        pool.wait_completion()

    def scan_torrc(self, data, **kwargs):
        """Method thats goes trough all folders and files in search for torrc files"""
        root, dirs, files = data
        for f in files:
            result = re.search('torrc\d+.config', f)
            if result:
                torrc_path = os.path.join(root,f)
                torrc_data = {'torrc_path': torrc_path, 'ipv4': get_ipv4()}
                # ones found read the file and get details about connection
                with open(torrc_path) as f:
                    rexs = ['SocksPort\s+(?:\d+\.\d+\.\d+\.\d+:)?(?P<port>\d+)',
                            'ControlPort\s+(?:\d+\.\d+\.\d+\.\d+:)?(?P<control_port>\d+)',
                            'PidFile\s+(?P<pid_file>.*?pid)',
                            'DataDirectory\s+(?P<data_dir>.*?data.\d+)',
                            'SocksListenAddress\s+(?P<ip>\d+\.\d+\.\d+\.\d+)'
                            ]
                    text = f.read()
                    for rex in rexs:
                        x = re.search(rex, text, re.IGNORECASE | re.DOTALL)
                        if x is not None:
                            torrc_data.update(x.groupdict())
                    f.close()

                check_host = torrc_data.get('ip')
                if check_host is None:
                    torrc_data.update({'ip': '127.0.0.1'})

                if torrc_data.get('pid_file') is None or torrc_data.get('data_dir') is None:
                    os.remove(torrc_path)
                    continue

                if torrc_data:
                    try:
                        self.tor.create_controller(address=torrc_data.get('ip'), control_port=int(torrc_data.get('control_port')))
                        self.tor.tor_connect()
                        with open(torrc_data.get('pid_file')) as f:
                            pid = int(f.read().strip())
                            torrc_data.update({'pid': pid})
                        self.opened_tors.update({len(self.opened_tors): torrc_data})
                    except:
                        # if stem is not possible to establish controller delete
                        del_dir_org = torrc_data.get('data_dir')
                        dir_drive, root_drive = del_dir_org[:2], root[:2]
                        del_root_dir = del_dir_org.replace(dir_drive, root_drive)
                        del_dirs = [del_root_dir, del_dir_org]
                        for del_dir in del_dirs:
                            if os.path.isdir(del_dir):
                                shutil.rmtree(del_dir)

                        if os.path.exists(torrc_path):
                            os.remove(torrc_path)

from core.winservice import WinService
class TorService(WinService):
    """
        Description:
        This class task is to run at all times and secure that
        - there is always enough tors running
        - cleaning up tor data that is not longer in use
        - change identity from time to time
    """
    maxtor = 5
    _service_name_ = 'TorService'
    _service_display_name_ = 'Tor Service'
    _service_description_ = 'Ensures tors are runing 24/7'

    def main(self):
        start_time = datetime.now()
        # create table if does not exists in db
        tor_table()
        while 1:
            # find torrc data
            TorScanner()
            # clean unusable tor's
            clean_tor()
            # create enough tor services
            TorBuild(tormax=self.maxtor)

            # diff = (datetime.now()-start_time).total_seconds()
            # if diff >= 120:
            #     # get all data and ports for changing idetities
            #     tor_data = _database.select(_view_name, view=True)
            #     host = tor_data.get('ip')
            #     control_point = tor_data.get('control_port')
            #     TorControl.control_port = control_point
            #     tc = TorControl()
            #     tc.create_controller(host, control_point)
            #     tc.new_identity()

            sleep(60)
















