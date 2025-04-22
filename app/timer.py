class Timer(ctk.CTkFrame):
    def __init__(self, master, switch_to_home):
        super().__init__(master)
        self.master = master
        self.switch_to_home = switch_to_home
        self.running = False
        self.is_paused = False
        self.time_remaining = 0

        self.label = ctk.CTkLabel(self, text="Set Time (hh:mm:ss):", font=("Helvetica", 15))
        self.label.pack(pady=10)

        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5)

        self.hour_entry = ctk.CTkEntry(entry_frame, width=60)
        self.hour_entry.pack(side="left", padx=5)
        self.minute_entry = ctk.CTkEntry(entry_frame, width=60)
        self.minute_entry.pack(side="left", padx=5)
        self.second_entry = ctk.CTkEntry(entry_frame, width=60)
        self.second_entry.pack(side="left", padx=5)

        self.start_button = ctk.CTkButton(self, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.pause_button = ctk.CTkButton(self, text="Pause / Resume", command=self.toggle_pause)
        self.pause_button.pack(pady=10)

        self.time_label = ctk.CTkLabel(self, text="Time Left: 0:00:00", font=("Helvetica", 50))
        self.time_label.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.pack(pady=10)

    def update_timer(self):
        if self.running and not self.is_paused and self.time_remaining > 0:
            self.time_remaining -= 1
            hours, remainder = divmod(self.time_remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.configure(text=f"Time Left: {hours}:{minutes:02}:{seconds:02}")
            self.after(1000, self.update_timer)
        elif self.time_remaining == 0 and self.running:
    self.running = False
    self.time_label.configure(text="Time's up!")

    # Alert sound from assets/alert.mp3
    alert_path = os.path.join("assets", "alert.mp3")
    if os.path.exists(alert_path):
        playsound(alert_path)
    else:
        print("Sound file not found at:", alert_path)
        

    def start_timer(self):
        try:
            hours = int(self.hour_entry.get()) if self.hour_entry.get().strip() else 0
            minutes = int(self.minute_entry.get()) if self.minute_entry.get().strip() else 0
            seconds = int(self.second_entry.get()) if self.second_entry.get().strip() else 0

            self.time_remaining = hours * 3600 + minutes * 60 + seconds
            if self.time_remaining <= 0:
                messagebox.showerror("Input Error", "Please enter a time greater than 0.")
                return

            self.running = True
            self.is_paused = False
            self.update_timer()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for time.")


    def toggle_pause(self):
        if self.running:
            self.is_paused = not self.is_paused
            if not self.is_paused:
                self.update_timer()

    def back(self):
        self.running = False
        self.switch_to_home()
        self.pack_forget()