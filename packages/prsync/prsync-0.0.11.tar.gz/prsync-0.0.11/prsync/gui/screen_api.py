import paramiko

import prsync.network.ssh.connection
import prsync.network.ssh.ssh_client
import prsync.network.ssh.commands.routing
import prsync.network.ssh.commands.rsync
import prsync.gui.screen_vars

import threading
import collections
import time


class ScreenApi:
    test_credentials = {"host": "", "username": "", "pass": ""}  # if you want to init connections
    default_root_path = None
    default_destination_root_path = None

    def __init__(self):
        self._default_clients_pwd = "";
        self._client_pwd = "";
        self._last_root_dir_with_selected_paths = ""
        self._root_path = None
        self._dest_root_path = None
        self._exclude_paths = {}
        self._Result = collections.namedtuple("Result", ["exit_code", "desc", "data"])
        self._source_path, self._dest_path = ("", "")
        self._paths = {}
        self._sources = {"source": "1", "dest": "2"}
        self._sources_flipped = {"1": "source", "2": "dest"}
        self.source_path, self.dest_path = ("", "")
        self._connections = {self.source_code: prsync.network.ssh.ssh_client.SSHClient(), self.dest_code: prsync.network.ssh.ssh_client.SSHClient()}
        self.reset_connections()

    def pwd_in_exclude(self, ls_result):
        to_compare = self._client_pwd+ls_result
        return any([path in to_compare and path != to_compare for path in self._exclude_paths])

    def _return_response(self, exit_code: int = 0, description: str = "", data : dict = {}):
        return self._Result(exit_code=exit_code, desc=description, data=data)

    def thread_process(self, target: callable, args: tuple = tuple()):
        threading.Thread(target=target, args=args).start()

    def _valid_path(self, path):
        return False if path in {".", "..", "./", "../"} else True

    def mark_source_root(self, selected_item_id, selected_path):
        old_index, old_path = self.root_path
        data={}
        if not self._valid_path(selected_path):
            result = self._return_response(exit_code=1, description="invalid path")
        else:
            if old_index is not None:
                data["old_index_exists"] = True
                data["old_index"] = old_index

            if selected_item_id is None:
                self.root_path = selected_path #default path
            else:
                self.root_path = self._build_root_path(selected_path)

            if old_path != self.root_path:
                self._paths = {}

            result = self._return_response(data=data)

        return result

    def _build_root_path(self, selected_item_id, selected_path):
        return (selected_item_id, "{}/{}".format(self.source_path, selected_path))

    def rsync(self):
        stdin, stdout, stderr = self._run_cmd(self.source_code, prsync.network.ssh.commands.rsync.rsync_exists())
        err = stderr.readlines(1)
        if len(err) and not "tty" in str(err[0]):
            return err

        flags = [
            prsync.gui.screen_vars.rsync_options_bitwise[bit]["value"] for bit in
                 prsync.gui.screen_vars.rsync_options_bitwise if
            prsync.gui.screen_vars.rsync_options_bitwise[bit]["element"].get() == 1]

        exclude_paths = list(self._exclude_paths.keys())
        exclude_paths.append("/*")
        cmd = prsync.network.ssh.commands.rsync.rsync(flags, list(self.paths), exclude_paths,
                                                      self._connections[self.dest_code].host,
                                                      self._connections[self.dest_code].username,
                                                      self.root_path,
                                                      self.dest_root_path)
        chan = self.connections[self.source_code].client.invoke_shell()
        chan.send(cmd + "\n") #send prsync cmd

        # Ssh and wait for the password prompt.
        buff = ''
        passed_yes_no_prompt = False
        while True:
            buff += str(chan.recv(9999)).lower()

            if any(prompt_yes_no in buff for prompt_yes_no in ["y/n", "yes/no"]) and not passed_yes_no_prompt:
                passed_yes_no_prompt = True
                chan.send('{}\n'.format("yes"))

            if "password" in buff:
                # Send the password and wait for a prompt.
                chan.send('{}\n'.format(self.connections[self.dest_code].password))
                break

            if "sending" in buff:
                #in case that there is no password prompt
                break


        return self._channel_reader(chan)


    def _channel_reader(self, channel):
        resp = ''
        try:
            while not resp.endswith('\''):
                while channel.recv_ready():
                    resp = str(channel.recv(9999))

                    if "" == resp.replace("b'\\r\\n'", ''): #parse the string, checking if its  an empty otuput..
                        time.sleep(0.5)  # prevent multi loops...
                        resp = ''  # init to get all output
                        break  # wait for recv again

                    for line in resp.lstrip("b'").rstrip("'").split('\\r\\n'):
                        if not "$ " in line: # process end
                            yield line
                        else:
                            raise Exception("")

                    resp = '' #init to get all output
                    break #wait for recv again

        except Exception:
            channel.close()

    def get_files(self, server_type, path):
        result = self._Result(exit_code=0, desc="", data={})
        try:
            stdin, stdout, stderr = self._run_cmd(server_type, prsync.network.ssh.commands.routing.list_files(path))
        except Exception as e:
            result = self._Result(exit_code=4, desc=str(e), data={})
        else:
            err = " ".join(stderr.readlines(1999))
            if len(err):
                result = self._Result(exit_code=1, desc=err , data={})

            if stdout:
                try:
                    pwd = next(stdout).strip("\n")
                except Exception as e:
                    result = self._Result(exit_code=2, desc=str(e), data={})
                else:
                    if server_type == self.source_code:
                        self.source_path = pwd
                        self.root_path = pwd if not self.paths else self.root_path
                        ScreenApi.default_root_path = pwd
                    else:
                        if self.dest_root_path is None:
                            ScreenApi.default_destination_root_path = pwd
                            self.dest_root_path = pwd
                        self.dest_path = pwd  # save te new path

                    result = self._Result(exit_code=0, desc="", data={"pwd": pwd, "files": stdout})
            else:
                result = self._Result(exit_code=3, desc="something went wrong", data={})
        return result

    def prepare_path_command(self, client_path, server_path) -> str:
        temp_path = prsync.network.ssh.commands.routing.build_path(client_path, self._client_pwd)

        if temp_path.startswith("/"):
            temp_path = temp_path.replace("/", "", 1)

        self._client_pwd = "" if temp_path == "/" or temp_path+"/" == self._client_pwd else temp_path+"/" if len(self._paths) else "" # chain this path to the includes path
        return prsync.network.ssh.commands.routing.build_path(client_path, server_path)

    def _run_cmd(self, server_type, cmd):
        return prsync.network.ssh.connection.run_cmd(self._connections[server_type], cmd)
    def connect(self, server_type, source_host='', source_user='', source_password=''):
        exit_code = 0
        desc = "Connected"

        if server_type in self._sources_flipped:
            try:
                self.connections[server_type].__init__(source_host, source_user, source_password)
                prsync.network.ssh.connection.create_connection(self.connections[server_type])
            except Exception as e:
                self.reset_connections()
                desc = str(e)
                exit_code = 1
        else:
            desc = "server type not in whitelist"
        return (exit_code, desc)

    def get_source_path(self):
        return self._source_path

    def set_source_path(self, sp):
        self._source_path = sp

    def get_dest_path(self):
        return self._dest_path

    def set_dest_path(self, dp):
        self._dest_path = dp

    def get_source_code(self):
        return self._sources["source"]

    def set_source_code(self, sc):
        self._sources["source"] = sc

    def get_dest_code(self):
        return self._sources["dest"]

    def set_dest_code(self, dc):
        self._sources["dest"] = dc


    def get_source_connection(self):
        return self._connections[self.get_source_code]

    def set_source_connection(self, sc):
        self._connections[self.get_source_code] = sc

    def get_dest_connection(self):
        return self._connections[self.get_dest_code]

    def set_dest_connection(self, dc):
        self._connections[self.get_dest_code] = dc

    def reset_connections(self):
        for connection_code in self.connections:
            if isinstance(self.connections[connection_code].client, paramiko.SSHClient):
                prsync.network.ssh.connection.close_connection(self.connections[connection_code]) # close paramiko connection
            self.connections[connection_code].client = None

    def get_connections(self):
        return self._connections

    def get_sources(self):
        return self._sources

    def _build_source_selectbox_item_path(self, path):
        return "{}/{}".format(self.source_path, path)

    def add_path(self, path, skip_if_in_exclude : bool = False):
        full_path = self._build_source_selectbox_item_path(path)

        if not self._is_path_selected(path) and (path != "." and path != ".."):

            if not self.last_root_dir_with_selected_paths or self.last_root_dir_with_selected_paths not in self.source_path:
                self.last_root_dir_with_selected_paths = self.source_path
                self._paths = {}

            full_path = self._client_pwd+path
            final_path = self._client_pwd+path if not full_path.endswith("/") else full_path[:-1]
            client_pwd = self._client_pwd

            if client_pwd:
                if client_pwd.endswith("/"):
                    client_pwd = client_pwd[:-1]
                if client_pwd not in self._paths:
                    self._paths[client_pwd] = True

            if not skip_if_in_exclude or (skip_if_in_exclude and final_path not in self._exclude_paths):
                self._paths[final_path] = True
                if final_path in self._exclude_paths:
                    del self._exclude_paths[final_path]


    def get_paths(self):
        return self._paths

    def _is_path_selected(self, path):
        return True if self._client_pwd+path in self.paths and \
                        self.last_root_dir_with_selected_paths in self.source_path and \
                        self.source_path \
            else False

    def _del_path(self, path):
        #path = self._build_source_selectbox_item_path(path)
        if self._is_path_selected(path):
            path = self._client_pwd + path
            del self.paths[path]
            self._exclude_paths[path] = True

    def delete_path(self, path):
        self._del_path(path)


    def is_source_item_selected(self, path):
        #path = self._build_source_selectbox_item_path(path)
        return self._is_path_selected(path)

    @property
    def dest_root_path(self):
        return self._dest_root_path

    @property
    def last_root_dir_with_selected_paths(self):
        return self._last_root_dir_with_selected_paths

    @last_root_dir_with_selected_paths.setter
    def last_root_dir_with_selected_paths(self, path):
        self._last_root_dir_with_selected_paths = path

    @dest_root_path.setter
    def dest_root_path(self, drp):
        if self._valid_path(drp):
            self._dest_root_path = drp

    @property
    def root_path(self):
        return self._root_path

    @root_path.setter
    def root_path(self, rp: str = ""):
        self._root_path = rp

    sources = property(get_sources)
    source_path = property(get_source_path, set_source_path)
    source_code = property(get_source_code, set_source_code)
    source_connection = property(get_source_connection, set_source_connection)

    dest_path = property(get_dest_path, set_dest_path)
    dest_code = property(get_dest_code, set_dest_code)
    dest_connection = property(get_dest_connection, set_dest_connection)

    connections = property(get_connections)
    paths = property(get_paths, add_path)
