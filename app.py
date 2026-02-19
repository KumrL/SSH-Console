import customtkinter as ctk
import paramiko
import tkinter as tk
import time

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SSH Console")
        self.geometry("1250x750")
        self.resizable(False, False)
        self.full_log = []
        self.err_log = []
        self.draw_ssh_console_gui()
        self.draw_saved_commands_gui()

    def draw_ssh_console_gui(self):
        #menu bar
        menubar = tk.Menu(self)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Export Log", command=lambda: self.export_log('full', self.full_log))
        menu_file.add_command(label="Export Error Log", command=lambda: self.export_log('error', self.err_log))
        menubar.add_cascade(label="File", menu=menu_file)
        self.config(menu=menubar)

        #tabview
        self.tabview = ctk.CTkTabview(self, state='enabled') ###############
        self.tabview.pack(fill="both", expand=True)
        self.tabview.add("SSH Console")
        self.tabview.add("Saved Commands")
        self.tabview.set("SSH Console")

        #top frame
        self.top_frame = ctk.CTkFrame(self.tabview.tab("SSH Console"))
        self.top_frame.place(relwidth=1, relheight=0.05, rely=0)

        hostname_lbl = ctk.CTkLabel(self.top_frame, text="Hostname:")
        hostname_lbl.grid(row=0, column=0)
        self.hostname_entry = ctk.CTkEntry(self.top_frame)
        self.hostname_entry.grid(row=0, column=1, padx=(0,25))

        username_lbl = ctk.CTkLabel(self.top_frame, text="Username:")
        username_lbl.grid(row=0, column=2)
        self.username_entry = ctk.CTkEntry(self.top_frame)
        self.username_entry.grid(row=0, column=3, padx=(0,25), pady=5)

        password_lbl = ctk.CTkLabel(self.top_frame, text="Password:")
        password_lbl.grid(row=0, column=4)
        self.password_entry = ctk.CTkEntry(self.top_frame, show="*")
        self.password_entry.grid(row=0, column=5, padx=(0,25))

        port_lbl = ctk.CTkLabel(self.top_frame, text="Port:")
        port_lbl.grid(row=0, column=6)
        self.port_entry = ctk.CTkEntry(self.top_frame)
        self.port_entry.grid(row=0, column=7, padx=(0,30))

        self.connect_button = ctk.CTkButton(self.top_frame, text="Connect", command=lambda: [self.server_conection(self.hostname_entry.get(), self.username_entry.get(), self.password_entry.get(), self.port_entry.get())])
        self.connect_button.grid(row=0, column=8, padx=(30,15))

        self.disconect_button = ctk.CTkButton(self.top_frame, text="Disconnect", state="disabled", command=lambda: [self.server_desconection()])
        self.disconect_button.grid(row=0, column=9)

        #dmiddle frame
        self.middle_frame = ctk.CTkFrame(self.tabview.tab("SSH Console"))
        self.middle_frame.place(relwidth=1, relheight=0.90, rely=0.05)

        self.input_log = ctk.CTkTextbox(self.middle_frame, state="disabled", border_width=2)
        self.input_log.place(relwidth=0.33, relheight=1)

        self.output_log = ctk.CTkTextbox(self.middle_frame, state="disabled", border_width=2)
        self.output_log.place(relx=0.33, relwidth=0.34, relheight=1)

        self.error_log = ctk.CTkTextbox(self.middle_frame, state="disabled", border_width=2)
        self.error_log.place(relx=0.67, relwidth=0.33, relheight=1)

        #bottom frame
        self.bottom_frame = ctk.CTkFrame(self.tabview.tab("SSH Console"))
        self.bottom_frame.place(relwidth=1, relheight=0.05, rely=0.95)

        self.command_entry = ctk.CTkEntry(self.bottom_frame)
        self.command_entry.place(relwidth=0.9, relheight=1)

        self.send_button = ctk.CTkButton(self.bottom_frame, text="Send", command=lambda: self.send_command(self.command_entry.get()))
        self.send_button.place(relx=0.9, relwidth=0.1, relheight=1)

    def draw_saved_commands_gui(self):
        #top frame
        sc_top_frame = ctk.CTkFrame(self.tabview.tab("Saved Commands"), fg_color="red")
        sc_top_frame.place(relwidth=1, relheight=0.25, rely=0)

        new_command_in = ctk.CTkEntry(sc_top_frame, placeholder_text="New Command")
        new_command_in.place(relx=0.05, rely=0.10, relwidth=0.90, relheight=0.20)

        name_in = ctk.CTkEntry(sc_top_frame, placeholder_text="New Name")
        name_in.place(relx=0.18, rely=0.40, relwidth=0.50, relheight=0.20)

        add_command_btn = ctk.CTkButton(sc_top_frame, text="Save")
        add_command_btn.place(relx= 0.72, rely=0.40, relwidth=0.10, relheight=0.20)

        search_in = ctk.CTkEntry(sc_top_frame, placeholder_text='Search')
        search_in.place(relx=0.18, rely=0.70, relwidth=0.64, relheight=0.20)

        #bottom frame
        sc_bottom_frame = ctk.CTkScrollableFrame(self.tabview.tab("Saved Commands"))
        sc_bottom_frame.place(relwidth=1, relheight=0.75, rely=0.25)

    def server_conection(self, hostname, username, password, port):
        self.full_log = []
        self.err_log = []
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if port:
                port = int(port)
            else:
                port = 22
            self.client.connect(hostname, port=port, username=username, password=password)
            self.disconect_button.configure(state="normal")
            self.tabview.configure(state="normal")
            self.connect_button.configure(state="disabled")
            self.hostname_entry.configure(state="disabled")
            self.username_entry.configure(state="disabled")
            self.password_entry.configure(state="disabled")
            self.port_entry.configure(state="disabled")

            self.input_log.configure(state="normal")
            self.input_log.delete("1.0", "end")
            self.input_log.insert("end", f"Connected to {hostname}\n\n")
            self.input_log.configure(state="disabled")

            self.output_log.configure(state="normal")
            self.output_log.delete("1.0", "end")
            self.output_log.configure(state="disabled")

            self.error_log.configure(state="normal")
            self.error_log.delete("1.0", "end")
            self.error_log.configure(state="disabled")

            return self.client
        except Exception as e:
            self.error_log.configure(state="normal")
            self.error_log.insert("end", f"Connection failed: {str(e)}\n\n")
            self.error_log.configure(state="disabled")
            return None
        
    def server_desconection(self):
        self.client.close()
        self.tabview.configure(state="disabled")
        self.disconect_button.configure(state="disabled")
        self.connect_button.configure(state="normal")
        self.hostname_entry.configure(state="normal")
        self.username_entry.configure(state="normal")
        self.password_entry.configure(state="normal")
        self.port_entry.configure(state="normal")
        self.input_log.configure(state="normal")
        self.input_log.insert("end", f"Disconnected from {self.hostname_entry.get()}\n\n")
        self.input_log.configure(state="disabled")

    def send_command(self, command):
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            out = stdout.read().decode()
            err = stderr.read().decode()

            if command:
                self.full_log.append(time.strftime(f"%a/%b/%Y(%H:%M:%S) -command- {command}\n", time.localtime()))
                self.input_log.configure(state="normal")
                self.input_log.insert("end", f"{command}\n\n")
            else:
                pass

            if out == '':
                pass
            else:
                self.full_log.append(time.strftime(f"%a/%b/%Y(%H:%M:%S) -output- {out}", time.localtime()))
                self.output_log.configure(state="normal")
                self.output_log.insert("end", f"{out}\n")

            if err == '': 
                pass
            else:
                self.full_log.append(time.strftime(f"%a/%b/%Y(%H:%M:%S) -error- {err}", time.localtime()))
                self.err_log.append(time.strftime(f"%a/%b/%Y(%H:%M:%S) -error- {err}", time.localtime()))
                self.error_log.configure(state="normal")
                self.error_log.insert("end", f"{err}\n")
            
            self.input_log.configure(state="disabled")
            self.output_log.configure(state="disabled")
            self.error_log.configure(state="disabled")
            self.command_entry.delete(0, "end")
            
    def export_log(self, kind, log):
        dirname = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not dirname:
            pass
        else:
            if kind == 'error':
                if log:
                    with open(dirname, 'wb') as f:
                        for e in log:
                            f.write((e+"\n").encode())
                else:
                    pass
            else:
                if log:
                    with open(dirname, 'wb') as f:
                        for e in log:
                            f.write((e+"\n").encode())
                else:
                    pass

ctk.set_appearance_mode("dark")
app = App()
app.mainloop()