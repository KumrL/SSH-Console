import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SSH Console")
        self.geometry("1250x750")
        self.resizable(False, False)
        self.draw_gui()

    def draw_gui(self):
        #drwing top frame
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.place(relwidth=1, relheight=0.95)

        self.input_log = ctk.CTkTextbox(self.top_frame, state="disabled")
        self.input_log.place(relwidth=0.33, relheight=1)

        self.output_log = ctk.CTkTextbox(self.top_frame, state="disabled")
        self.output_log.place(relx=0.33, relwidth=0.34, relheight=1)

        self.error_log = ctk.CTkTextbox(self.top_frame, state="disabled")
        self.error_log.place(relx=0.67, relwidth=0.33, relheight=1)

        #drawimg bottom frame
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.place(relwidth=1, relheight=0.05, rely=0.95)

        self.command_entry = ctk.CTkEntry(self.bottom_frame)
        self.command_entry.place(relwidth=0.9, relheight=1)

        self.send_button = ctk.CTkButton(self.bottom_frame, text="Send")
        self.send_button.place(relx=0.9, relwidth=0.1, relheight=1)

ctk.set_appearance_mode("dark")
app = App()
app.mainloop()