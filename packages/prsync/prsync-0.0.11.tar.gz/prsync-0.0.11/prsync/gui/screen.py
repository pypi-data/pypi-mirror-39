import prsync.network.ssh
import datetime
import prsync.gui.screen_vars
try:
    import tkinter
except ImportError: # python 2
    import Tkinter as tkinter

from tkinter import messagebox
import tkinter.font

class Gui:
    _width = 1300
    _height = 600
    _program_name = "Linux Rsync GUI"

    def __init__(self):
        prsync.gui.api.__init__()
        self._win = tkinter.Tk() if not hasattr(self, "_win") else self._win
        self.fromContainer = tkinter.LabelFrame(self._win, text="From", padx=5)
        self.dataContainer = tkinter.Frame(self.fromContainer)
        self.readDirContainer = tkinter.Frame(self.dataContainer, pady=5)
        self.bottom_btns = tkinter.Label(self.readDirContainer)
        self._btns = self._btns if hasattr(self, "_btns") else {
            "include_path": tkinter.Button(self.bottom_btns, state="disabled", text="include path's", border=3, command=self._on_click_add_path, width=15),
            "exclude_path": tkinter.Button(self.bottom_btns, state="disabled", text="exclude path's", border=3, command=self._on_click_remove_path, width=15),
            "view_includes": tkinter.Button(self.bottom_btns, state="disabled", text="view include's", border=3, command=self._on_click_view_path, width=15)
        }

        self._textLog = self._textLog if hasattr(self, "_textLog") else None
        self._connect_btn = self._connect_btn if hasattr(self, "_connect_btn") else None
        self._disconnect_btn = self._disconnect_btn if hasattr(self, "_disconnect_btn") else None
        self._source_fileList = self._source_fileList if hasattr(self, "_source_fileList") else None
        self._dest_fileList = self._dest_fileList if hasattr(self, "_dest_fileList") else None

        self._options_bitwise_sum = sum([int(bit) for bit in prsync.gui.screen_vars.rsync_options_bitwise if prsync.gui.screen_vars.rsync_options_bitwise[bit]["default_value"] == 1])
        self.credentials_inputs = self.credentials_inputs if hasattr(self, "credentials_inputs") else {
            "source": {
                "host": "",
                "username": "",
                "password": "",
            },
            "dest": {
                "host": "",
                "username": "",
                "password": "",
            }
        }

        if self._connect_btn is not None:
            self._connect_btn["state"] = "normal"
        if self._disconnect_btn is not None:
            self._disconnect_btn["state"] = "disabled"

        self._set_root_path()
        self._set_dest_path()
        self._clear_listbox(self._source_fileList)
        self._clear_listbox(self._dest_fileList)

    def _clear_listbox(self, listbox):
        if listbox is not None:
            listbox.delete(0, tkinter.END)

    def _error_msg(self, **kwargs):
        title = kwargs.pop("title", '')
        tkinter.messagebox.showerror(title=title, **kwargs)

    def insert_row_to_log_box(self, index=tkinter.INSERT, msg="", tag="", show_date=True):
        tmplt = ''
        if show_date:
            tmplt += "[{}]\n".format(datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        tmplt += "{}\n".format(str(msg))
        self._textLog.insert(index, tmplt, tag)
        self._textLog.see("end")

    def async(self, lines):

        for line in lines:
            self.insert_row_to_log_box(msg=line, tag=prsync.gui.screen_vars.INFO, show_date=False)
    def _start_rsync_process(self):
        self.insert_row_to_log_box(msg="Start prsync process:")
        self.insert_row_to_log_box(msg="registering flags")

        prsync.gui.api.thread_process(target=self.async, args=(prsync.gui.api.rsync(),))  # generator))

    def _on_click_sync(self):
        prsync.gui.api.thread_process(target=self._start_rsync_process)

    def _check_if_rsync_exists(self):
        cmd = "prsync --version"
        return self._run_cmd(prsync.gui.api.source_code, cmd)

    def _fill_list_box_with_server_files(self, server_type, tkinter_file_list, path="."):
        server = "Source" if server_type == prsync.gui.api.source_code else "Destination"
        self.insert_row_to_log_box(msg="changing {} dir to {}".format(server, path), tag=prsync.gui.screen_vars.INFO)

        exit_code, desc, data = prsync.gui.api.get_files(server_type, path)
        if exit_code == 0:
            self._clear_listbox(tkinter_file_list)
            self.insert_row_to_log_box(msg="{}: list files, path: {}".format(server, data["pwd"]), tag=prsync.gui.screen_vars.SUCCESS)
            self._total_items = 0
            for ls_result in data.get("files", []):
                ls_result = ls_result.strip("\n")
                if ls_result != ".":
                    tkinter_file_list.insert(tkinter.END, ls_result)
                    if server_type == prsync.gui.api.source_code:

                        if prsync.gui.api.paths and prsync.gui.api.last_root_dir_with_selected_paths in data["pwd"]\
                                and prsync.gui.api.last_root_dir_with_selected_paths != data["pwd"] and not prsync.gui.api.pwd_in_exclude(ls_result):
                            self._select_source_item(self._total_items, True)

                        if prsync.gui.api.is_source_item_selected(ls_result):
                            tkinter_file_list.itemconfig(self._total_items, {"bg": "yellow"})

                        elif prsync.gui.api.root_path == prsync.gui.api.source_path + "/" +ls_result + "/":
                            self._source_fileList.itemconfig(self._total_items, {"bg": "green"})
                    self._total_items += 1

            if prsync.gui.api.root_path is not None:
                self._set_root_path()
            if prsync.gui.api.dest_root_path is not None:
                self._set_dest_path()

        else:
            self.insert_row_to_log_box(msg="{}: can't list entries in {}".format(server, path), tag=prsync.gui.screen_vars.ERROR)
            self.insert_row_to_log_box(msg="ERROR: {}".format(str(desc)), tag=prsync.gui.screen_vars.ERROR)

        return  exit_code

    def _change_dest_dir(self, event):
        path = self._dest_fileList.get(tkinter.ACTIVE)
        
        prsync.gui.api.thread_process(target=self._fill_list_box_with_server_files, args=(
            prsync.gui.api.dest_code, self._dest_fileList,
            prsync.gui.api.prepare_path_command(path, prsync.gui.api.dest_path)))

    def _change_source_dir(self, event):
        path = self._source_fileList.get(tkinter.ACTIVE)

        prsync.gui.api.thread_process(target=self._fill_list_box_with_server_files, args=(
            prsync.gui.api.source_code, self._source_fileList,
            prsync.gui.api.prepare_path_command(path, prsync.gui.api.source_path)))

    def _on_disconnect_click(self):
        for _, elem in self._btns.items():
            elem.config(state="disabled")
        self._mark_base_dir_as_root_btn.config(state="disabled")
        self._mark_as_destination_btn.config(state="disabled")
        self._sync_btn.config(state="disabled")

        self.__init__()
        self.insert_row_to_log_box(msg="Disconnected......", tag=prsync.gui.screen_vars.INFO)

    def _gui_connect_process(self, server_type, host, user_name, password):
        self.insert_row_to_log_box(msg="Connecting to {0} as {1}@{0}".format(host, user_name), tag=prsync.gui.screen_vars.INFO)
        result_code, desc = prsync.gui.api.connect(server_type, host, user_name, password)
        if result_code == 0: # success
            self.insert_row_to_log_box(msg="Connected to {}".format(host), tag=prsync.gui.screen_vars.SUCCESS)
        else:
            self._connect_btn["state"] = "normal"
            self.insert_row_to_log_box(msg="could not connect to {}".format(host))
            self.insert_row_to_log_box(msg=desc)
            self.insert_row_to_log_box(msg="session aborted")

        return result_code

    def _init_connection(self):
        if self._gui_connect_process(prsync.gui.api.source_code, self.source_host.get(), self.source_user.get(), self.source_password.get()) == 0:
            if self._gui_connect_process(prsync.gui.api.dest_code, self.dest_host.get(), self.dest_user.get(), self.dest_password.get()) == 0:
                self._disconnect_btn["state"] = "normal"
                if self._fill_list_box_with_server_files(prsync.gui.api.source_code, self._source_fileList) == 0 and \
                        self._fill_list_box_with_server_files(prsync.gui.api.dest_code, self._dest_fileList) == 0:
                    self.insert_row_to_log_box(msg="====new seesion has been started====", tag=prsync.gui.screen_vars.SUCCESS)
                    for _, elem in self._btns.items():
                        elem.config(state="active")
                    self._mark_base_dir_as_root_btn.config(state="active")
                    self._mark_as_destination_btn.config(state="active")
                    self._sync_btn.config(state="active")

    def on_click_connect(self):
        if prsync.gui.screen_validations.validate_new_session(self) == 0:
            self._connect_btn["state"] = "disabled"
            prsync.gui.api.thread_process(target=self._init_connection)
        else:
            self._error_msg(message="all fields must be filled")

    def _select_source_item(self, select_id, skip_if_in_exclude: bool = False):
        prsync.gui.api.add_path(self._source_fileList.get(select_id), skip_if_in_exclude)

    def _on_click_add_path(self):
        if len(self._source_fileList.curselection()):
            for select_id in self._source_fileList.curselection():
                if prsync.gui.api.pwd_in_exclude(self._source_fileList.get(select_id)):
                    self._error_msg(message="Parent dir of {} is in exclude list".format(prsync.gui.api._client_pwd + self._source_fileList.get(select_id)))
                    break
                self._select_source_item(select_id)
                if prsync.gui.api.is_source_item_selected(self._source_fileList.get(select_id)):
                    self._source_fileList.itemconfig(select_id, {"bg": "yellow"})

    def _on_click_remove_path(self):
        if len(self._source_fileList.curselection()):
            for select_id in self._source_fileList.curselection():
                self._source_fileList.itemconfig(select_id, {"bg": ""})
                prsync.gui.api.delete_path(self._source_fileList.get(select_id))


    def _on_click_view_path(self):
        path_list = tkinter.Toplevel(self._win)
        path_list.title = "View include's"
        path_list.geometry("300x300+0+0")
        Frame = tkinter.Frame(path_list)
        Frame.grid(row=0, column=0)
        list_box = tkinter.Listbox(Frame, width=45, height=17)
        list_box.grid(row=0, column=0)
        listScroll = tkinter.Scrollbar(Frame, orient=tkinter.VERTICAL, command=list_box.yview)
        listScroll.grid(row=0, column=1, sticky="ens")
        list_box["yscrollcommand"] = listScroll.set

        for path in prsync.gui.api.paths:
            list_box.insert(tkinter.END, "{}".format(path))

    def _on_click_mark_as_destination(self):
        prsync.gui.api.dest_root_path = "{}/{}/".format(prsync.gui.api.dest_path, self._dest_fileList.get(tkinter.ACTIVE))
        self._set_dest_path()

    def _on_click_mark_dest_base_as_root(self):
        prsync.gui.api.dest_root_path = prsync.gui.api.default_destination_root_path
        self._set_dest_path()

    def _on_click_mark_base_as_root(self):
        self._set_base_root(None, prsync.gui.api.default_root_path)

    def _on_click_mark_as_root(self):
         self._set_base_root(self._source_fileList.curselection()[0], "{}/".format(self._source_fileList.get(tkinter.ACTIVE)))

    def _set_base_root(self, item_index, item_path):
        if len(self._source_fileList.curselection()) > 1:
            self._error_msg(message="only one path can be set as root path")
        else:
            exit_code, desc, data = prsync.gui.api.mark_source_root(item_index, item_path)
            if exit_code == 0:
                if data.get("old_index_exists", False) and data.get("old_index", False) and self._total_items > data["old_index"]:
                    self._source_fileList.itemconfig(data["old_index"], {"bg": ""})

                if item_index is not None:
                    self._source_fileList.itemconfig(item_index, {"bg": "green"})
            else:
                self.insert_row_to_log_box(msg=desc, tag=prsync.gui.screen_vars.ERROR)
            self._set_root_path()

    def _set_root_path(self):
        if hasattr(self, "_source_path_label"):
            self._source_path_label['text'] = "Root Path: " + ("" if prsync.gui.api.root_path is None else prsync.gui.api.root_path)

    def _set_dest_path(self):
        if hasattr(self, "_dest_path_label"):
            self._dest_path_label['text'] = "Destination Path: " + ("" if prsync.gui.api.dest_root_path is None else prsync.gui.api.dest_root_path)

    def draw(self):
        self._win.title(self._program_name)
        self._win.geometry("{}x{}+0+0".format(self._width, self._height))
        self._win["padx"] = 10
        self._win.grid_columnconfigure(0, weight=0)
        self._win.grid_columnconfigure(1, weight=0)
        self._win.grid_columnconfigure(2, weight=0)
        self._win.grid_columnconfigure(3, weight=0)
        self._win.grid_rowconfigure(0, weight=0)
        self._win.grid_rowconfigure(1, weight=0)
        self._win.grid_rowconfigure(2, weight=0)
        self._win.grid_rowconfigure(3, weight=0)


        self.fromContainer.grid(row=0, column=0, sticky='nw')

        tkinter.Label(self.fromContainer, text='Host', width=3).grid(row=0, column=0, sticky='w')
        self.source_host = tkinter.Entry(self.fromContainer)
        self.source_host.grid(row=0, column=1)
        self.source_host.insert(tkinter.END, prsync.gui.api.test_credentials["host"])

        tkinter.Label(self.fromContainer, text='User', width=3).grid(row=1, column=0, sticky='w')
        self.source_user = tkinter.Entry(self.fromContainer)
        self.source_user.grid(row=1, column=1)
        self.source_user.insert(tkinter.END, prsync.gui.api.test_credentials["username"])

        tkinter.Label(self.fromContainer, text='Password').grid(row=2, column=0, sticky='w')
        self.source_password = tkinter.Entry(self.fromContainer, show="*")
        self.source_password.grid(row=2, column=1)
        self.source_password.insert(tkinter.END, prsync.gui.api.test_credentials["pass"])

        self.dataContainer.grid(row=3, column=0, columnspan=2, sticky='wn')

        tkinter.Label(self.dataContainer, text="Files to copy", pady=5).grid(row=1, column=0, sticky='w')

        self.readDirContainer.grid(row=2, column=0, sticky='ws')
        self._source_fileList = tkinter.Listbox(self.readDirContainer, selectmode=tkinter.EXTENDED, height=27, width=30)
        self._source_fileList.grid(row=0, column=0, sticky='we')
        self._source_fileList.config(border=2, relief='sunken')
        self._source_fileList.bind("<Double-1>", func=self._change_source_dir)
        listScroll = tkinter.Scrollbar(self.readDirContainer, orient=tkinter.VERTICAL, command=self._source_fileList.yview)
        listScroll.grid(row=0, column=1, sticky="ens", rowspan=2)
        self._source_fileList["yscrollcommand"] = listScroll.set

        self.bottom_btns.grid(row=0, column=3, columnspan=3, sticky='nw')
        self._btns["include_path"].grid(row=2, column=1, pady=5)
        self._btns["exclude_path"].grid(row=3, column=1, pady=5)
        self._btns["view_includes"].grid(row=4, column=1, pady=5)

        self._source_path_label = tkinter.Label(self._win, text="Root Path:")
        self._dest_path_label = tkinter.Label(self._win, text="Destination Path:")

        self._source_path_label.grid(row=1, column=0, columnspan=3, padx=5, sticky="w")
        self._dest_path_label.grid(row=2, column=0, columnspan=3, padx=5, sticky="w")

        descContainer = tkinter.LabelFrame(self._win, text="Dest", padx=5)
        descContainer.grid(row=0, column=1, sticky='nw')
        tkinter.Label(descContainer, text='Host', width=3).grid(row=0, column=0, sticky='w')
        self.dest_host = tkinter.Entry(descContainer)
        self.dest_host.grid(row=0, column=1)
        self.dest_host.insert(tkinter.END, prsync.gui.api.test_credentials["host"])

        tkinter.Label(descContainer, text='User', width=3).grid(row=1, column=0, sticky='w')
        self.dest_user = tkinter.Entry(descContainer)
        self.dest_user.grid(row=1, column=1)
        self.dest_user.insert(tkinter.END, prsync.gui.api.test_credentials["username"])

        tkinter.Label(descContainer, text='Password').grid(row=2, column=0, sticky='w')
        self.dest_password = tkinter.Entry(descContainer, show="*")
        self.dest_password.grid(row=2, column=1)
        self.dest_password.insert(tkinter.END, prsync.gui.api.test_credentials["pass"])

        dataContainer = tkinter.Frame(descContainer)
        dataContainer.grid(row=3, column=0, columnspan=2, sticky='wn')
        tkinter.Label(dataContainer, text="Path to locate files", pady=5).grid(row=1, column=0, sticky='w')
        readDirContainer = tkinter.Frame(dataContainer, pady=5)
        readDirContainer.grid(row=2, column=0, sticky='ws')
        self._dest_fileList = tkinter.Listbox(readDirContainer, height=27, width=30)
        self._dest_fileList.grid(row=0, column=0, sticky='we')
        self._dest_fileList.config(border=2, relief='sunken')
        self._dest_fileList.bind("<Double-1>", func=self._change_dest_dir) #dbl click on item from list
        listScroll = tkinter.Scrollbar(readDirContainer, orient=tkinter.VERTICAL, command=self._dest_fileList.yview)
        listScroll.grid(row=0, column=1, sticky="ens", rowspan=2)
        self._dest_fileList["yscrollcommand"] = listScroll.set

        bottom_btns = tkinter.Label(readDirContainer)
        bottom_btns.grid(row=0, column=3, columnspan=3, sticky='nw')
        self._mark_as_destination_btn = tkinter.Button(bottom_btns, state="disabled", text="mark as destination", border=3, command=self._on_click_mark_as_destination, width=15)
        self._mark_as_destination_btn.grid(row=0, column=1, pady=5)

        self._mark_base_dir_as_root_btn = tkinter.Button(bottom_btns, state="disabled", text="mark base dir as root", border=3, command=self._on_click_mark_dest_base_as_root,width=15)
        self._mark_base_dir_as_root_btn.grid(row=1, column=1, pady=5)

        lbl = tkinter.Label(self._win, pady=5)
        lbl.grid(row=0, column=3, sticky='nwe')
        btnWrapper = tkinter.LabelFrame(lbl, text='Connection', pady=5)
        btnWrapper.grid(row=0, column=0, sticky='nwe')
        self._connect_btn = tkinter.Button(btnWrapper, text='Connect', border=3, command=self.on_click_connect)
        self._connect_btn.grid(row=0, column=0, sticky='w')
        self._disconnect_btn = tkinter.Button(btnWrapper, state='disabled', text='Disconnect', border=3, command=self._on_disconnect_click)
        self._disconnect_btn.grid(row=0, column=1, sticky='w')

        btnWrapper = tkinter.LabelFrame(lbl, text='Rsync', pady=5)
        btnWrapper.grid(row=1, column=0, sticky='nwe')
        tkinter.Label(btnWrapper, text="Flags").grid(row=0, column=0, sticky='w')

        counter = 1
        for bit_value in prsync.gui.screen_vars.rsync_options_bitwise:
            prsync.gui.screen_vars.rsync_options_bitwise[bit_value]["element"] = tkinter.IntVar(value=int(bit_value) & self._options_bitwise_sum > 0)
            tkinter.Checkbutton(btnWrapper, text=prsync.gui.screen_vars.rsync_options_bitwise[bit_value]["title"],
                                variable=prsync.gui.screen_vars.rsync_options_bitwise[bit_value]["element"]
                                ).grid(row=counter, column=0, sticky="w")
            counter += 1

        self._sync_btn = tkinter.Button(btnWrapper, state="disabled", width=16, text='Run rsync', border=3, command=self._on_click_sync)
        self._sync_btn.grid(row=counter, column=0, sticky='w', columnspan=3)

        logContainer = tkinter.LabelFrame(self._win, text='Log', pady=28)


        logContainer.grid(row=0, column=2, sticky='wn')
        self._textLog = tkinter.Text(logContainer, width=53, height=30)
        self._textLog.tag_configure(prsync.gui.screen_vars.ERROR, foreground="red")
        self._textLog.tag_configure(prsync.gui.screen_vars.INFO, foreground="blue")
        self._textLog.tag_configure(prsync.gui.screen_vars.SUCCESS, foreground="green")
        self._textLog.grid(row=0, column=0, sticky='wns', rowspan=2, columnspan=2)
        listScroll = tkinter.Scrollbar(logContainer, orient=tkinter.VERTICAL, command=self._textLog.yview)
        listScroll.grid(row=0, column=2, rowspan=2, sticky="nsw")
        self._textLog["yscrollcommand"] = listScroll.set

        self._win.update()
        self._win.minsize(self._width, self._height)
        self._win.maxsize(self._width, self._height)
        self._win.mainloop()

    def get_source_host(self):
        return self.credentials_inputs["source"]["host"]

    def set_source_host(self, entry: tkinter.Entry):
        self.credentials_inputs["source"]["host"] = entry

    def get_source_username(self):
        return self.credentials_inputs["source"]["username"]

    def set_source_username(self, entry: tkinter.Entry):
        self.credentials_inputs["source"]["username"] = entry

    def get_source_password(self):
        return self.credentials_inputs["source"]["password"]

    def set_source_password(self, entry: tkinter.Entry):
        self.credentials_inputs["source"]["password"] = entry

    def get_dest_host(self):
        return self.credentials_inputs["dest"]["host"]

    def set_dest_host(self, entry: tkinter.Entry):
        self.credentials_inputs["dest"]["host"] = entry

    def get_dest_username(self):
        return self.credentials_inputs["dest"]["username"]

    def set_dest_username(self, entry: tkinter.Entry):
        self.credentials_inputs["dest"]["username"] = entry

    def get_dest_password(self):
        return self.credentials_inputs["dest"]["password"]

    def set_dest_password(self, entry: tkinter.Entry):
        self.credentials_inputs["dest"]["password"] = entry

    source_host = property(get_source_host, set_source_host)
    source_user = property(get_source_username, set_source_username)
    source_password = property(get_source_password, set_source_password)
    dest_host = property(get_dest_host, set_dest_host)
    dest_user = property(get_dest_username, set_dest_username)
    dest_password = property(get_dest_password, set_dest_password)

import prsync.gui.screen_validations