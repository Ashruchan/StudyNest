import customtkinter as ctk
from tkinter import messagebox
import os
from playsound import playsound

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


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
            if os.path.exists('mixkit-scanning-sci-fi-alarm-905.mp3'):
                playsound('mixkit-scanning-sci-fi-alarm-905.mp3')
            else:
                print("Sound file not found.")

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


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Study Time Pro")
    root.geometry("800x500")

    current_frame = None

    def switch_to_home():
        global current_frame
        if current_frame:
            current_frame.pack_forget()
        main_menu.pack(pady=20)

    def open_timer():
        global current_frame
        if current_frame:
            current_frame.pack_forget()
        main_menu.pack_forget()
        current_frame = Timer(root, switch_to_home)
        current_frame.pack(fill="both", expand=True)

    def open_stopwatch():
        global current_frame
        if current_frame:
            current_frame.pack_forget()
        main_menu.pack_forget()
        current_frame = Stopwatch(root, switch_to_home)
        current_frame.pack(fill="both", expand=True)

    main_menu = ctk.CTkFrame(root)
    main_menu.pack(pady=20)

    timer_button = ctk.CTkButton(
        main_menu,
        text="Open Timer",
        command=open_timer,
        width=250,
        height=100,
        font=("Helvetica", 24)
    )
    timer_button.pack(pady=20)

    stopwatch_button = ctk.CTkButton(
        main_menu,
        text="Open Stopwatch",
        command=open_stopwatch,
        width=250,
        height=100,
        font=("Helvetica", 24)
    )
    stopwatch_button.pack(pady=20)

    root.mainloop()
