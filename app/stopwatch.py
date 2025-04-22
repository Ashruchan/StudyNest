class Stopwatch(ctk.CTkFrame):
    def __init__(self, master, switch_to_home):
        super().__init__(master)
        self.master = master
        self.switch_to_home = switch_to_home
        self.running = False
        self.time_elapsed = 0

        self.label = ctk.CTkLabel(self, text="0:00:00", font=("Helvetica", 144))
        self.label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.pack(pady=10)

    def update_time(self):
        if self.running:
            self.time_elapsed += 1
            hours, remainder = divmod(self.time_elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label.configure(text=f"{hours}:{minutes:02}:{seconds:02}")
            self.after(1000, self.update_time)

    def start(self):
        if not self.running:
            self.running = True
            self.update_time()

    def stop(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.time_elapsed = 0
        self.label.configure(text="0:00:00")

    def back(self):
        self.running = False
        self.switch_to_home()
        self.pack_forget()