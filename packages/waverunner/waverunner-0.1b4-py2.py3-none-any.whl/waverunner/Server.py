from __future__ import print_function

import sys
import os
import os.path as path
import fnmatch
import argparse
from netifaces import interfaces, ifaddresses, AF_INET
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait as futures_wait
import threading
import inspect
import traceback
from socket import gethostname
from socket import error as socketerror

from multiprocessing import cpu_count

import hashlib
import binascii
from random import randint, getrandbits


if sys.version_info.major == 2:
    # for Python2
    from SocketServer import ThreadingMixIn
    from DocXMLRPCServer import DocXMLRPCServer, resolve_dotted_attribute
    from xmlrpclib import ServerProxy
    from Tkinter import *  ## notice capitalized T in Tkinter
    from ttk import Notebook
    import tkFileDialog
    import imp
    PY_SYSVER = 2

elif sys.version_info.major == 3:
    # for Python3
    from socketserver import ThreadingMixIn
    from xmlrpc.server import DocXMLRPCServer, resolve_dotted_attribute
    from xmlrpc.client import ServerProxy
    from tkinter import *  ## notice lowercase 't' in tkinter here
    from tkinter.ttk import Notebook
    from tkinter import filedialog as tkFileDialog
    import importlib
    PY_SYSVER = 3


iflist = {}
for interface in interfaces():
    config = ifaddresses(interface)
    # AF_INET is not always present
    if AF_INET in config.keys():
        for link in config[AF_INET]:
            # loopback holds a 'peer' instead of a 'broadcast' address
            # if 'addr' in link.keys() and 'peer' not in link.keys():
            if 'addr' in link.keys():
                iflist.update({str(interface): link['addr']})

default_port = 12344
default_user_ips = (('143.215.156.66', default_port),)
default_password = 'ratsofftoya'

thisfile = os.path.abspath(__file__)
thispath = os.path.split(thisfile)[0]


class PublicMethod(object):
    def __init__(self, fn):
        self.__name__ = fn.__name__
        self._method = fn

    def __call__(self, *args, **kwargs):
        return self._method(*args, **kwargs)


class SecureMethod(object):
    def __init__(self, fn):
        self.__name__ = fn.__name__
        self._method = fn

    def __call__(self, *args, **kwargs):
        return self._method(*args, **kwargs)


class PublicInstance(object):
    def __init__(self, instance):
        self.__name__ = instance.__name__
        self._instance = instance

    def __getattr__(self, item):
        return self._instance.__getattr__(item)


class SecureInstance(object):
    def __init__(self, instance):
        self.__name__ = instance.__name__
        self._instance = instance

    def __getattr__(self, item):
        return self._instance.__getattr__(item)


class OutOfChallengesError(RuntimeError):
    pass


class NoWaverunnerThereError(RuntimeError):
    pass


class MaxRetriesError(RuntimeError):
    pass


class ChallengeNotValidError(RuntimeError):
    pass


class Client(threading.local):
    def __init__(self):
        self.address = None


class ThreadingRPCServer(ThreadingMixIn, DocXMLRPCServer, object):
    def __init__(self, *args, **kwargs):
        super(ThreadingRPCServer, self).__init__(*args, **kwargs)
        self.client = Client()
        self.lock = threading.Lock()

    def process_request_thread(self, request, client_address):
        # self.lock.acquire()
        self.client.address = client_address
        return super(ThreadingRPCServer, self).process_request_thread(request, client_address)

    # def _dispatch(self, method, params):
    #     """Dispatches the XML-RPC method.
    #
    #     This is monkeypatched from the source.
    #     Releasing the lock only in order to run the external code.
    #     """
    #     try:
    #         # call the matching registered function
    #         func = self.funcs[method]
    #     except KeyError:
    #         pass
    #     else:
    #         if func is not None:
    #             return func(*params)
    #         raise Exception('method "%s" is not supported' % method)
    #
    #     if self.instance is not None:
    #         if hasattr(self.instance, '_dispatch'):
    #             # call the `_dispatch` method on the instance
    #             self.lock.release()
    #             return self.instance._dispatch(method, params)
    #
    #         # call the instance's method directly
    #         try:
    #             func = resolve_dotted_attribute(
    #                 self.instance,
    #                 method,
    #                 self.allow_dotted_names
    #             )
    #         except AttributeError:
    #             pass
    #         else:
    #             if func is not None:
    #                 self.lock.release()
    #                 return func(*params)
    #
    #     raise Exception('method "%s" is not supported' % method)


class RPCServer(DocXMLRPCServer, object):
    def __init__(self, *args, **kwargs):
        super(RPCServer, self).__init__(*args, **kwargs)
        self.client = Client()

    def process_request(self, request, client_address):
        self.client.address = client_address
        return super(RPCServer, self).process_request(request, client_address)


class HookedDict(dict):
    def __init__(self, hookfn, *args, **kwargs):
        super(HookedDict, self).__init__(*args, **kwargs)
        self.hook = hookfn

    def __setitem__(self, *args, **kwargs):
        super(HookedDict, self).__setitem__(*args, **kwargs)
        self.hook()

    def update(self, *args, **kwargs):
        super(HookedDict, self).update(*args, **kwargs)
        self.hook()


class Server(object):

    def __init__(self,
                 user_ips=default_user_ips,
                 interface=None,
                 port=default_port,
                 path_to_serve=None,
                 password=default_password,
                 notify_interval=60,
                 max_outstanding_challenges=2,
                 challenge_ttl=120,
                 max_challenge_retries=3,
                 challenge_retry_interval=3,
    ):

        self._events = {
            'stop_notify': threading.Event(),
            'challenge_accepted': threading.Event(),
            'shutdown': threading.Event(),
        }

        self._events['stop_notify'].set()
        self._events['challenge_accepted'].clear()
        self._events['shutdown'].clear()

        self._threadlocks = {
            'server_challenge': threading.Lock(),
            'client_challenge': threading.Lock(),
        }

        self.tkroot = None
        self.rtvars = None
        self.server = None
        self.server_thread = None
        self.challenge_tender_thread = None
        self.notify_server_thread = None

        self.serving = False
        self.srv_functions = []
        self.srv_instances = []
        self.srv_functions_secured = []
        self.srv_instances_secured = []
        self._outstanding_challenges = {}
        self.initialized = True

        self._srv_path = None
        self._registered_services = HookedDict(self._update_gui_vars)
        self._host_file = traceback.extract_stack(limit=2)[-2][0]
        self._host_path = os.path.split(self._host_file)
        self._port = port if port is not None else default_port
        self._iface = [key for key in iflist.keys() if 'lo' not in key][0] if not interface else interface
        self._ip = iflist[self.iface]
        self._max_outstanding_challenges = max_outstanding_challenges if 0 < max_outstanding_challenges < 50 else 2
        self._max_challenge_retries = max_challenge_retries
        self._challenge_retry_interval = challenge_retry_interval

        self.password = str(password) if password is not None else default_password
        self.notify_interval = int(notify_interval) if notify_interval else 60
        self._challenge_ttl = int(challenge_ttl)
        self._challenge_tender_interval = 15

        user_ips = default_user_ips if user_ips is None else user_ips

        if isinstance(user_ips, str):
            if ',' in user_ips:
                user_ips = [item.strip() for item in user_ips.split(',')]
            elif ' ' in user_ips:
                user_ips = [item.strip() for item in user_ips.split(' ')]
            else:
                user_ips = [user_ips]

        parsed = []
        for i, user in enumerate(list(user_ips)):
            if isinstance(user, str):
                user = user.split(':')
            if len(user) == 1:
                user = (user[0].strip('\''), default_port)
            elif len(user) == 2:
                user = (user[0].strip('\''), int(user[1].strip('\'')))

            parsed.append(tuple(user))

        self.user_ips = parsed if parsed else list(default_user_ips)

        if path_to_serve is not None:
            self.set_testpath(path_to_serve)

    # gui needs: 'srv_path','ip','iface','port','services'

    @property
    def port(self):
        return self._port

    @property
    def srv_path(self):
        return self._srv_path

    @property
    def ip(self):
        return self._ip

    @property
    def iface(self):
        return self._iface

    @property
    def registered_services(self):
        return self._registered_services

    @port.setter
    def port(self, value):
        self._set_port(value)

    @srv_path.setter
    def srv_path(self, value):
        self._set_srv_path(value)

    @ip.setter
    def ip(self, value):
        self._set_ip(value)

    @iface.setter
    def iface(self, value):
        self._set_iface(value)

    def _update_gui_vars(self):
        if self.rtvars is not None:
            for gui_var in self.rtvars.keys():
                self.rtvars[gui_var].set(getattr(self, gui_var))

    def _set_port(self, value):
        self._port = int(value)
        if self.rtvars is not None:
            self.rtvars['port'].set(str(self._port))

    def _set_srv_path(self, value):
        self._srv_path = str(value)
        if self.rtvars is not None:
            self.rtvars['srv_path'].set(self._srv_path)

    def _set_ip(self, value):
        self._ip = str(value)
        if self.rtvars is not None:
            self.rtvars['ip'].set(str(self._ip))

    def _set_iface(self, value):
        self._iface = str(value)
        if self.rtvars is not None:
            self.rtvars['iface'].set(self._iface)

    def is_secure(self, fn):
        if fn in [name for name, _ in self.srv_functions_secured]:
            return True
        elif fn in [name for name, _ in self.srv_functions]:
            return False
        else:
            print('Server.is_secture(): could not find function named {}'.format(fn))
            return None

    def get_challenge(self):
        try:
            self._threadlocks['server_challenge'].acquire()

            if len(self._outstanding_challenges) >= self._max_outstanding_challenges:
                print('ran out of challenges')
                raise OutOfChallengesError

            else:
                client = self.server.client.address[0]
                challenge = ''.join([format(randint(0, 16), 'x') for i in range(256)])

                if client in self._outstanding_challenges:
                    self._outstanding_challenges[client].append(challenge)
                else:
                    self._outstanding_challenges.update({client: [challenge]})
                print('issued a challenge')
                return challenge

        except Exception as e:
            raise e

        finally:
            self._threadlocks['server_challenge'].release()

    def _generate_response(self, challenge, salt=None):
        salt = format(getrandbits(256), 'x').encode() if salt is None else salt
        key = binascii.hexlify(hashlib.pbkdf2_hmac('sha1', self.password.encode(), salt=salt, iterations=1000))
        return hashlib.sha1(key+challenge.encode()).hexdigest(), salt

    def threaded_external_requests(self, hosts, fn_names, args=None, kwargs=None, timeout=10*60):

        with ThreadPoolExecutor(max_workers=100) as E_daddy:
            if args is None and kwargs is None:
                futures = E_daddy.map(self.external_request, hosts, fn_names)
            elif args is not None and kwargs is None:
                futures = E_daddy.map(self.external_request, hosts, fn_names, args)
            elif args is None and kwargs is not None:
                futures = E_daddy.map(self.external_request, hosts, fn_names, kwargs)
            else:
                futures = E_daddy.map(self.external_request, hosts, fn_names, args, kwargs)

            results = []
            for i in futures:
                results.append(i)
            return results

    def external_request(self, remote_host, remote_fn_name, *args, **kwargs):
        try:
            self._threadlocks['client_challenge'].acquire()
            print('got challenge acquisition lock')

            if isinstance(remote_host, str):
                remote_host = remote_host.split(':')
            if len(remote_host) < 2:
                remote_host = [remote_host, default_port]

            host = ServerProxy('http://{}:{}'.format(remote_host[0], remote_host[1]))

            try:
                secure = host.is_secure(remote_fn_name)

            except socketerror:
                raise NoWaverunnerThereError

            if secure is True:
                retry_ct = 0
                response = None

                try:
                    while retry_ct < self._max_challenge_retries:
                        challenge = host.get_challenge()
                        response, salt = self._generate_response(challenge)
                        break

                except OutOfChallengesError:
                    print('server was out of challenges')
                    retry_ct += 1
                    self._events['shutdown'].wait(self._challenge_retry_interval)
                    pass

                if response is None:
                    raise MaxRetriesError("couldn't get a challenge and ran out of retries")

        except Exception as e:
            raise e

        finally:
            self._threadlocks['client_challenge'].release()
            print('released challenge acquisition lock')

        if secure is True and response is not None:
            print('got a challenge. calling remote fn: {}'.format(remote_fn_name))
            result = host.__getattr__(remote_fn_name)((response, salt), *args, **kwargs)
            print('result= {}'.format(result))

        elif secure is False:
            print('calling public remote fn: {}'.format(remote_fn_name))
            result = host.__getattr__(remote_fn_name)(*args, **kwargs)
            print('result={}'.format(result))

        elif secure is None:
            print('remote host did not recognize that fn: {}'.format(remote_fn_name))
            result = None

        return result

    def _external_security_wrapper(self, fn):

        def wrapped(response_tuple, *args, **kwargs):
            try:
                print('received external request for secure function')
                response, salt = response_tuple
                client = self.server.client.address[0]
                if client not in self._outstanding_challenges:
                    print('challenge was not issued by me')
                    return ChallengeNotValidError

                authorized = False
                try:
                    self._threadlocks['server_challenge'].acquire()
                    for index, item in enumerate(self._outstanding_challenges[client]):
                        if PY_SYSVER == 3:
                            test_response = self._generate_response(item, salt.data)[0]
                        elif PY_SYSVER == 2:
                            test_response = self._generate_response(item, salt)[0]
                        if response == test_response:
                            del self._outstanding_challenges[client][index]
                            authorized = True

                except Exception as e:
                    return e

                finally:
                    self._threadlocks['server_challenge'].release()

                if authorized:
                    print('accepted response for secure function: {}'.format(fn.__name__))
                    print('running secure fn: {}'.format(fn.__name__))
                    result = fn(*args, **kwargs)
                    print('result is: {}'.format(result))
                else:
                    print('rejecting response for secure function: {}'.format(fn.__name__))
                    result = ChallengeNotValidError

                return result

            except Exception as e:
                print('exception raised before calling secure function: {}'.format(fn.__name__))
                return e

        wrapped.__name__ = fn.__name__
        return wrapped

    def tend_challenges(self):
        ages = {}
        update_interval = self._challenge_tender_interval

        def prune_challenges():
            """
            make sure you have a lock before entering here
            :return:
            """
            hosts = self._outstanding_challenges.keys()
            ids = [ [ hash(str(host) + str(item)) for item in self._outstanding_challenges[host] ]  for host in hosts]
            ids_flat = []
            [ids_flat.extend(item) for item in ids]

            newct = 0
            for id in ids_flat:
                if id not in ages:
                    ages.update({id: 0})
                    newct += 1
                else:
                    ages[id] += update_interval
            print('tender found {} new challenges have been issued.'.format(newct))

            purges = []
            for id, age in ages.items():
                if id not in ids_flat:
                    purges.append(id)
                if age > self._challenge_ttl:
                    purges.append(id)

            print('pruning {} challenges'.format(len(purges)))
            for item in purges:
                if item in ages:
                    del ages[item]

                for i, host in enumerate(hosts):
                    for j, item in enumerate(self._outstanding_challenges[host]):
                        if ids[i][j] == item:
                            del self._outstanding_challenges[host][j]

            print('outstanding challenges: {}'.format(ages))
            print('tender going to sleep')

        try:
            while not self._events['shutdown'].is_set() and self.serving:
                self._threadlocks['server_challenge'].acquire()
                prune_challenges()
                self._threadlocks['server_challenge'].release()
                self._events['shutdown'].wait(timeout=update_interval)

        except Exception as e:
            self._events['shutdown'].set()
            raise e

    def notify_users(self):
        print('user notification starting')
        while not self._events['stop_notify'].is_set() and self.serving:
            print('user notification running')
            if self.user_ips and self.notify_interval > 0:
                print('about to send notifications')
                try:
                    for ip, port in self.user_ips:
                        if not (ip == self.ip and port == self.port):
                            print('about to notify {}:{}'.format(ip, port))
                            self.external_request(
                                (ip, port),
                                'notify',
                                self.ip, self.port,
                                [name for name, _ in self.srv_functions],
                                [name for name, _ in self.srv_instances],
                                [name for name, _ in self.srv_functions_secured],
                                [name for name, _ in self.srv_instances_secured]
                            )
                            print('notified {}:{}'.format(ip, port))

                except NoWaverunnerThereError:
                    pass

                except Exception as e:
                    self._events['shutdown'].set()
                    raise e

                self._events['stop_notify'].wait(timeout=self.notify_interval)

    def notify(self, address, port, bare_fns, bare_insts, sec_fns, sec_insts):

        self.registered_services.update({
            ':'.join([address, str(port)]): [bare_fns, bare_insts, sec_fns, sec_insts],
        })
        print('got a notification from {}:{}'.format(address,port))
        return '10-4'

    def register_user(self, ip, port=None):
        if ':' in ip and port is None:
            self.user_ips.append(tuple(ip.split(':')))
        elif ip and not port:
            self.user_ips.append(tuple(ip, self.default_port))
        elif ip and port:
            self.user_ips.append(tuple(ip, port))

    def make_gui(self, ):

        self.tkroot = Tk()
        self.tkroot.title('WaveRunner')

        rtvars = {'srv_path': StringVar(),
                  'ip': StringVar(),
                  'iface': StringVar(),
                  'port': StringVar(),
                  'services': StringVar()
                  }
        rtvars['iface'].set(self.iface)
        rtvars['ip'].set(self.ip)
        rtvars['port'].set(self.port)
        rtvars['services'].set(self.registered_services)
        self.rtvars = rtvars

        note = Notebook(self.tkroot, padding=0)
        note.grid(sticky=N + S + E + W)

        status_tab = Frame(note)
        status_tab.grid(sticky=N + S + E + W)
        config_tab = Frame(note)
        config_tab.grid(sticky=N + S + E + W)

        note.add(status_tab, text="Status", sticky=N + S + E + W, padding=10)
        note.add(config_tab, text="Configure", sticky=N + S + E + W, padding=10)

        """ Status Tab """
        Label(status_tab, text="Waverunner is running", font="Sans 24 bold").grid(columnspan=2)

        ip_lframe = LabelFrame(status_tab, text="Waverunner http server address")
        ip_lframe.grid(row=1, padx=10, pady=10, sticky=E)
        Label(ip_lframe, textvariable=self.rtvars['ip']).grid(row=0, column=0, sticky=E)
        Label(ip_lframe, text=':').grid(row=0, column=1)
        Label(ip_lframe, textvariable=self.rtvars['port']).grid(row=0, column=2, sticky=W)

        testdir_lframe = LabelFrame(status_tab, text="Waverunner tests path")
        testdir_lframe.grid(row=2, padx=10, pady=10, sticky=E)
        Label(testdir_lframe, textvariable=self.rtvars['srv_path']).grid(row=1, column=1)

        password_lframe = LabelFrame(status_tab, text="Password")
        password_lframe.grid(row=3, padx=10, pady=10, sticky=E)
        Label(password_lframe, text=self.password).grid()

        services_lframe = LabelFrame(status_tab, text="Registered Services")
        services_lframe.grid(row=4, padx=10, pady=10, sticky=E)
        Label(services_lframe, textvariable=self.rtvars['services']).grid()

        Button(status_tab, text="Change\nTest Directory", command=self.gui_update_testpath).grid(row=2, column=1, sticky=W)
        Button(status_tab, text="Copy", command=self.gui_address_to_clipboard).grid(row=1, column=1, sticky=W)

        Label(status_tab, text='You can get more details by directing a web browser\nto the ip address above.').grid(row=5, sticky=S+W)
        Button(status_tab, text="QUIT", bg='red', fg="black", font="sans 24 bold", command=self.exit_gracefully).grid(row=5, column=1, sticky=S+E)

        """ Config Tab """
        conff1 = LabelFrame(config_tab, text="select ethernet interface")
        conff1.grid()
        [Radiobutton(conff1, text=str(iface), variable=self.rtvars['iface'], value=str(iface),
                     command=self.resolve_interface_request).grid(column=0, sticky=W) for iface in iflist.keys()]

    def gui_address_to_clipboard(self):
        address = ':'.join([self.ip, str(self.port)])
        self.copytext(address)

    def gui_update_testpath(self):
        cur_path = self.srv_path
        if cur_path:
            newpath = os.path.abspath(tkFileDialog.askdirectory(initialdir=cur_path))
        else:
            newpath = os.path.abspath(tkFileDialog.askdirectory())
        if newpath and os.path.isdir(newpath):
            self.set_testpath(newpath)

    def set_testpath(self, path):
        testpath = os.path.abspath(path)
        if testpath != self.srv_path and testpath != thispath and testpath and testpath is not None:
            serving = bool(self.server)
            _ = self.stop_service() if serving else None
            self.parse_test_dir(testpath)
            _ = self.start_service() if serving else None

    def parse_test_dir(self, new_path):

        testmodules = []
        for root, dirs, files in os.walk(new_path):
            for tfile in files:
                if not tfile.startswith('_') and tfile.endswith('.py') and os.path.join(root, tfile) != self._host_file:
                    testmodules.append((str(os.path.join(root, tfile))))

        print('found modules: {}'.format(testmodules))

        if self.srv_path is not None and self.srv_path in sys.path and self.srv_path != new_path:
            sys.path.remove(self.srv_path)
        self._set_srv_path(new_path)
        if self.srv_path not in sys.path:
            sys.path.append(self.srv_path)

        live_modules = []
        for module in testmodules:
            try:
                live_modules.append(_get_live_module(module))
            except (ImportError, SyntaxError, TypeError, ValueError) as e:
                print('problem importing {}: {}. moving on...'.format(module, e.message))

        for module in live_modules:
            for itemname, item in [(item, getattr(module, item)) for item in dir(module)]:
                if isinstance(item, (SecureMethod, PublicInstance, PublicMethod, SecureInstance)):

                    if isinstance(item, SecureMethod):
                        self.register_secure_method(item, modulename=module.__name__)

                    elif isinstance(item, PublicMethod):
                        self.register_insecure_method(item, modulename=module.__name__)

                    elif isinstance(item, SecureInstance):
                        self.register_secure_instance(item, modulename=module.__name__)

                    elif isinstance(item, PublicInstance):
                        self.register_insecure_instance(item, modulename=module.__name__)

        if self.srv_functions:
            print('methods available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self.srv_functions]
            )))
        if self.srv_instances:
            print('instances available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self.srv_instances]
            )))
        if self.srv_functions_secured:
            print('methods available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self.srv_functions_secured]
            )))
        if self.srv_instances_secured:
            print('instances available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self.srv_instances_secured]
            )))

    def register_secure_method(self, method, modulename=None):
        assert isinstance(method, SecureMethod)
        serving = self.serving
        self.stop_service()
        name = '.'.join([modulename, method.__name__]) if modulename is not None else method.__name__
        self.srv_functions_secured.append((name, self._external_security_wrapper(method._method)))
        if serving:
            self.start_service()

    def register_insecure_method(self, method, modulename=None):
        assert isinstance(method, PublicMethod)
        serving = self.serving
        self.stop_service()
        name = '.'.join([modulename, method.__name__]) if modulename is not None else method.__name__
        self.srv_functions.append((name, method._method))
        if serving:
            self.start_service()

    def register_secure_instance(self, instance, modulename=None):
        assert isinstance(instance, SecureInstance)
        serving = self.serving
        self.stop_service()
        name = '.'.join([modulename, instance.__name__]) if modulename is not None else instance.__name__
        self.srv_functions_secured.append((name, self._external_security_wrapper(instance._instance)))
        if serving:
            self.start_service()

    def register_insecure_instance(self, instance, modulename=None):
        assert isinstance(instance, PublicInstance)
        serving = self.serving
        self.stop_service()
        name = '.'.join([modulename, instance.__name__]) if modulename is not None else instance.__name__
        self.srv_functions.append((name, instance._instance))
        if serving:
            self.start_service()

    def set_interface(self, ifname):
        ip = iflist[ifname.get()]
        self._ip = ip

    def resolve_interface_request(self, ):
        if self.server is not None:
            needsrestart = True
            self.stop_service()
        else:
            needsrestart = False

        self.set_interface(self.rtvars['iface'])

        if needsrestart:
            self.start_service()

    def copytext(self, text_to_copy=''):
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(text_to_copy)
        clip.destroy()

    def start_xmlrpc_server(self, ):

        if self.server is None and self.server_thread is None:

            server = ThreadingRPCServer(addr=(self.ip, int(self.port)), allow_none=True)
            # server = RPCServer(addr=(self.ip, int(self.port)))

            server.set_server_title('Waverunner in python')
            server.set_server_documentation('Application provides RPC access to python scripts')
            server.set_server_name('waverunner_'+gethostname())

            # register system functions
            server.register_function(self.get_challenge)
            server.register_function(self.notify)
            server.register_function(self.is_secure)

            for name, fn in self.srv_functions + self.srv_functions_secured:
                server.register_function(fn, name=name)

            for name, inst in self.srv_instances + self.srv_instances_secured:
                server.register_instance(inst, name=name)

            server.register_introspection_functions()
            server.register_multicall_functions()

            server_thread = threading.Thread(target=server.serve_forever)
            self.challenge_tender_thread = threading.Thread(target=self.tend_challenges)

            self.challenge_tender_thread.start()
            server_thread.start()

            print('server started at {}:{}'.format(self.ip, self.port))
            self.server = server
            self.server_thread = server_thread

        else:
            print('server already running... restarting')
            self.stop_xmlrpc_server()
            self.start_xmlrpc_server()

    def stop_xmlrpc_server(self):

        if self.server_thread or self.server:
            if self.server_thread and self.server_thread.is_alive():
                self.server.shutdown()
            self.server.server_close()
            print('server stopped')
            del self.server
            del self.server_thread
            self.server = None
            self.server_thread = None

    def start_notify_server(self, ):
        self._events['stop_notify'].clear()
        self.notify_server_thread = threading.Thread(target=self.notify_users)
        self.notify_server_thread.start()
        if self.user_ips:
            print('sending notifications to:\n{}'.format('\n'.join(
                [':'.join([ip, str(port)]) for ip, port in self.user_ips]
            )))

    def stop_notify_server(self, ):
        self._events['stop_notify'].set()
        self.notify_server_thread.join()

    def serve_forever(self):
        self.start_service()
        try:
            while not self._events['shutdown'].is_set():
                self._events['shutdown'].wait(3.0)
        except:
            pass
        finally:
            self.exit_gracefully()

    def join(self):
        try:
            while not self._events['shutdown'].is_set():
                self._events['shutdown'].wait(3.0)
        except:
            pass
        finally:
            self.exit_gracefully()

    def start_service(self, ):
        if not self.serving:
            self.start_xmlrpc_server()
            self.start_notify_server()
            self.serving = True

    def stop_service(self, ):
        if self.serving:
            self.stop_xmlrpc_server()
            self.stop_notify_server()
            self.serving = False

    def exit_gracefully(self, ):
        self.stop_service()
        self._events['shutdown'].set()
        if self.tkroot is not None:
            self.tkroot.quit()
            self.tkroot = None

    def list_remote_services(self):
        return repr(self.registered_services)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d')
    parser.add_argument('--port', '-p')
    parser.add_argument('--notify', '-n')
    parser.add_argument('--password', '-s')
    parser.add_argument('--gui', action='store_true')
    parser.add_argument('--notify-interval', '-i')

    args = parser.parse_args()
    if args.notify:
        args.notify = args.notify.split(',')

    server = Server(
        user_ips=args.notify,
        path_to_serve=args.directory,
        port=args.port,
        password=args.password,
        notify_interval=args.notify_interval
    )

    try:
        server.start_service()
        if args.gui:
            server.make_gui()
            server.tkroot.mainloop()
        server.join()
    except Exception as e:
        server.exit_gracefully()
        server.join()
        raise e


def _file2mod(filepath):
    return os.path.split(filepath)[-1].split('.py')[0]


def _list_modules_at_path(pathspec, names=None):
    assert os.path.isdir(pathspec)
    mods = [file.split('.')[0] for file in fnmatch.filter(os.listdir(pathspec), '[!_]*.py')]
    mods.sort()
    mods = list(filter(lambda item: item in names, mods)) if names else mods
    paths = [path.join(pathspec, mod + '.py') for mod in mods]
    return zip(mods, paths)


def _get_live_module(module_path):

    module_name = _file2mod(module_path)
    if module_name not in sys.modules:
        if PY_SYSVER == 2:
            module = imp.load_source(module_name, module_path)
        else:
            module = importlib.import_module(module_name)
    module = sys.modules[module_name]
    return module


if __name__ == '__main__':
    main()
