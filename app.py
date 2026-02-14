import customtkinter as ctk
import paramiko

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SSH Console")
        self.geometry("1250x750")
        self.resizable(False, False)
        self.draw_gui()

    def draw_gui(self):
        #self top frame
        self.top_frame = ctk.CTkFrame(self)
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
        self.password_entry.grid(row=0, column=5, padx=(0,30))

        self.connect_button = ctk.CTkButton(self.top_frame, text="Connect", command=lambda: [self.server_conection(self.hostname_entry.get(), self.username_entry.get(), self.password_entry.get())])
        self.connect_button.grid(row=0, column=6, padx=(30,15))

        self.disconect_button = ctk.CTkButton(self.top_frame, text="Disconnect", state="disabled", command=lambda: [self.server_desconection()])
        self.disconect_button.grid(row=0, column=7)

        #drwing middle frame
        self.middle_frame = ctk.CTkFrame(self)
        self.middle_frame.place(relwidth=1, relheight=0.90, rely=0.05)

        self.input_log = ctk.CTkTextbox(self.middle_frame, state="disabled", border_width=2)
        self.input_log.place(relwidth=0.33, relheight=1)

        self.output_log = ctk.CTkTextbox(self.middle_frame, state="disabled", border_width=2)
        self.output_log.place(relx=0.33, relwidth=0.34, relheight=1)

        self.error_log = ctk.CTkTextbox(self.middle_frame, state="disabled", border_width=2)
        self.error_log.place(relx=0.67, relwidth=0.33, relheight=1)

        #drawimg bottom frame
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.place(relwidth=1, relheight=0.05, rely=0.95)

        self.command_entry = ctk.CTkEntry(self.bottom_frame)
        self.command_entry.place(relwidth=0.9, relheight=1)

        self.send_button = ctk.CTkButton(self.bottom_frame, text="Send", command=lambda: self.send_command(self.command_entry.get()))
        self.send_button.place(relx=0.9, relwidth=0.1, relheight=1)

    def server_conection(self, hostname, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname, username=username, password=password)
            print("Connection successful")
            self.disconect_button.configure(state="normal")
            self.connect_button.configure(state="disabled")
            self.hostname_entry.configure(state="disabled")
            self.username_entry.configure(state="disabled")
            self.password_entry.configure(state="disabled")
            self.input_log.configure(state="normal")
            self.input_log.insert("end", f"Connected to {hostname}\n")
            self.input_log.configure(state="disabled")
            return self.client
        except Exception as e:
            self.error_log.configure(state="normal")
            self.error_log.insert("end", f"Connection failed: {str(e)}\n")
            self.error_log.configure(state="disabled")
            return None
        
    def server_desconection(self):
        self.client.close()
        self.disconect_button.configure(state="disabled")
        self.connect_button.configure(state="normal")
        self.hostname_entry.configure(state="normal")
        self.username_entry.configure(state="normal")
        self.password_entry.configure(state="normal")
        self.input_log.configure(state="normal")
        self.input_log.insert("end", f"Disconnected from {self.hostname_entry.get()}\n")
        self.input_log.configure(state="disabled")

    def send_command(self, command):
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            self.input_log.configure(state="normal")
            self.input_log.insert("end", f"{command}\n")
            self.output_log.configure(state="normal")
            self.output_log.insert("end", f"{stdout.read().decode()}\n")
            self.error_log.configure(state="normal")
            self.error_log.insert("end", f"{stderr.read().decode()}\n")
            self.input_log.configure(state="disabled")
            self.output_log.configure(state="disabled")
            self.error_log.configure(state="disabled")

ctk.set_appearance_mode("dark")
app = App()
app.mainloop()