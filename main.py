"""
Text to Speech Converter
-------------------------
A beginner-friendly BCA mini project that converts user-entered text
into speech using pyttsx3 (offline Text-to-Speech engine) with a
Tkinter based Graphical User Interface (GUI).

Author : (Your Name)
Course : BCA
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import threading


class TextToSpeechApp:
    """
    This class contains the entire Text to Speech application.
    Using a class (Object Oriented Programming) keeps all the
    GUI widgets and the speech engine organized together.
    """

    def __init__(self, root):
        # ---------- Basic Window Setup ----------
        self.root = root
        self.root.title("Text to Speech Converter")
        self.root.geometry("650x600")
        self.root.minsize(600, 550)
        self.root.configure(bg="#f0f4f8")

        # ---------- Initialize the pyttsx3 Speech Engine ----------
        # pyttsx3.init() loads the text-to-speech engine available
        # on the user's operating system (SAPI5 on Windows,
        # NSSpeechSynthesizer on Mac, espeak on Linux).
        try:
            self.engine = pyttsx3.init()
        except Exception as error:
            messagebox.showerror(
                "Engine Error",
                f"Could not start the speech engine.\n\n{error}"
            )
            self.engine = None

        # A flag to know if the application is currently speaking.
        self.is_speaking = False

        # Build all the GUI widgets.
        self.create_widgets()

        # Load the voices available on this computer into the dropdown.
        self.load_voices()

    # ------------------------------------------------------------------
    # GUI CREATION
    # ------------------------------------------------------------------
    def create_widgets(self):
        """Creates and arranges all the GUI elements on the window."""

        # ---------- Title Section ----------
        title_label = tk.Label(
            self.root,
            text="Text to Speech Converter",
            font=("Segoe UI", 20, "bold"),
            bg="#f0f4f8",
            fg="#1a237e"
        )
        title_label.pack(pady=(15, 0))

        subtitle_label = tk.Label(
            self.root,
            text="Convert your text into speech easily",
            font=("Segoe UI", 11),
            bg="#f0f4f8",
            fg="#455a64"
        )
        subtitle_label.pack(pady=(0, 10))

        # ---------- Text Input Area ----------
        text_frame = tk.Frame(self.root, bg="#f0f4f8")
        text_frame.pack(padx=20, pady=5, fill="both", expand=True)

        text_label = tk.Label(
            text_frame,
            text="Enter your text below:",
            font=("Segoe UI", 10, "bold"),
            bg="#f0f4f8",
            fg="#263238"
        )
        text_label.pack(anchor="w")

        # A frame to hold the Text widget + scrollbar together
        text_box_frame = tk.Frame(text_frame)
        text_box_frame.pack(fill="both", expand=True, pady=5)

        scrollbar = tk.Scrollbar(text_box_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            text_box_frame,
            wrap="word",
            font=("Segoe UI", 11),
            height=10,
            yscrollcommand=scrollbar.set,
            relief="solid",
            borderwidth=1
        )
        self.text_area.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_area.yview)

        # ---------- Voice Selection ----------
        options_frame = tk.LabelFrame(
            self.root,
            text="Voice Settings",
            font=("Segoe UI", 10, "bold"),
            bg="#f0f4f8",
            padx=10,
            pady=10
        )
        options_frame.pack(padx=20, pady=10, fill="x")

        voice_label = tk.Label(
            options_frame, text="Select Voice:", bg="#f0f4f8"
        )
        voice_label.grid(row=0, column=0, sticky="w", pady=5)

        self.voice_combo = ttk.Combobox(
            options_frame, state="readonly", width=40
        )
        self.voice_combo.grid(row=0, column=1, columnspan=2, sticky="w", padx=10)

        # ---------- Speech Rate Slider ----------
        rate_label = tk.Label(
            options_frame, text="Speech Rate:", bg="#f0f4f8"
        )
        rate_label.grid(row=1, column=0, sticky="w", pady=5)

        # A reasonable speaking rate range: 100 (slow) to 300 (fast)
        # Normal human speech is roughly around 150-180 words/min.
        self.rate_slider = tk.Scale(
            options_frame,
            from_=100,
            to=300,
            orient="horizontal",
            length=250,
            bg="#f0f4f8"
        )
        self.rate_slider.set(170)  # default, comfortable speaking rate
        self.rate_slider.grid(row=1, column=1, columnspan=2, sticky="w", padx=10)

        # ---------- Volume Slider ----------
        volume_label = tk.Label(
            options_frame, text="Volume:", bg="#f0f4f8"
        )
        volume_label.grid(row=2, column=0, sticky="w", pady=5)

        # Slider is shown to the user as 0-100 (easy to understand),
        # but pyttsx3 expects volume between 0.0 and 1.0, so we
        # convert it later inside the speak_text() function.
        self.volume_slider = tk.Scale(
            options_frame,
            from_=0,
            to=100,
            orient="horizontal",
            length=250,
            bg="#f0f4f8"
        )
        self.volume_slider.set(80)  # default volume
        self.volume_slider.grid(row=2, column=1, columnspan=2, sticky="w", padx=10)

        # ---------- Buttons ----------
        button_frame = tk.Frame(self.root, bg="#f0f4f8")
        button_frame.pack(pady=15)

        self.speak_button = tk.Button(
            button_frame,
            text="▶ Speak",
            font=("Segoe UI", 11, "bold"),
            bg="#2e7d32",
            fg="white",
            width=12,
            command=self.speak_text
        )
        self.speak_button.grid(row=0, column=0, padx=8)

        self.stop_button = tk.Button(
            button_frame,
            text="■ Stop",
            font=("Segoe UI", 11, "bold"),
            bg="#c62828",
            fg="white",
            width=12,
            command=self.stop_speech
        )
        self.stop_button.grid(row=0, column=1, padx=8)

        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            font=("Segoe UI", 11, "bold"),
            bg="#546e7a",
            fg="white",
            width=12,
            command=self.clear_text
        )
        self.clear_button.grid(row=0, column=2, padx=8)

        # ---------- Status Bar ----------
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "italic"),
            bg="#cfd8dc",
            fg="#263238",
            anchor="w",
            padx=10
        )
        status_bar.pack(side="bottom", fill="x")

    # ------------------------------------------------------------------
    # VOICE LOADING
    # ------------------------------------------------------------------
    def load_voices(self):
        """
        Fetches all voices installed on the current system and
        displays their names inside the dropdown (Combobox).
        """
        if self.engine is None:
            return

        voices = self.engine.getProperty('voices')
        self.voice_list = voices  # keep reference for later use

        voice_names = []
        for index, voice in enumerate(voices):
            # Some systems give long names, so we keep it readable.
            voice_names.append(f"{index}: {voice.name}")

        if voice_names:
            self.voice_combo['values'] = voice_names
            self.voice_combo.current(0)  # select the first voice by default
        else:
            self.voice_combo['values'] = ["Default Voice"]
            self.voice_combo.current(0)

    # ------------------------------------------------------------------
    # SPEAK FUNCTION
    # ------------------------------------------------------------------
    def speak_text(self):
        """
        Reads the text typed by the user and converts it to speech
        using the pyttsx3 engine, applying the selected voice,
        rate and volume.
        """
        if self.engine is None:
            messagebox.showerror("Error", "Speech engine is not available.")
            return

        # Get text from the text box (from start "1.0" to the end)
        user_text = self.text_area.get("1.0", tk.END).strip()

        # Handle empty input without crashing.
        if user_text == "":
            self.status_var.set("Please enter some text")
            return

        # Prevent starting a new speech while one is already running.
        if self.is_speaking:
            self.status_var.set("Already speaking...")
            return

        try:
            # ---------- Apply Voice ----------
            selected_index = self.voice_combo.current()
            if hasattr(self, "voice_list") and self.voice_list:
                self.engine.setProperty('voice', self.voice_list[selected_index].id)

            # ---------- Apply Rate ----------
            rate_value = self.rate_slider.get()
            self.engine.setProperty('rate', rate_value)

            # ---------- Apply Volume ----------
            # Convert the 0-100 slider value into pyttsx3's 0.0-1.0 range.
            volume_value = self.volume_slider.get() / 100
            self.engine.setProperty('volume', volume_value)

            # Update status and disable the Speak button while speaking.
            self.status_var.set("Speaking...")
            self.is_speaking = True
            self.speak_button.config(state="disabled")

            # ---------- Run Speech in a Separate Thread ----------
            # Speech playback (runAndWait) is a blocking operation.
            # Running it inside a thread keeps the GUI responsive,
            # so the window does not freeze while speaking.
            speech_thread = threading.Thread(
                target=self._run_speech, args=(user_text,), daemon=True
            )
            speech_thread.start()

        except Exception as error:
            self.is_speaking = False
            self.speak_button.config(state="normal")
            messagebox.showerror("Error", f"Something went wrong:\n{error}")
            self.status_var.set("Ready")

    def _run_speech(self, text):
        """
        Internal helper method that actually performs the speech.
        Runs inside a background thread so the GUI stays responsive.
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            # After speaking completes normally (not stopped)
            self.status_var.set("Ready")
        except Exception as error:
            self.status_var.set("Ready")
            print(f"Speech error: {error}")
        finally:
            self.is_speaking = False
            # Re-enable the Speak button (must be done via 'after'
            # because we are inside a background thread).
            self.root.after(0, lambda: self.speak_button.config(state="normal"))

    # ------------------------------------------------------------------
    # STOP FUNCTION
    # ------------------------------------------------------------------
    def stop_speech(self):
        """Stops the speech immediately, if it is currently speaking."""
        if self.engine is None:
            return

        try:
            self.engine.stop()
            self.is_speaking = False
            self.speak_button.config(state="normal")
            self.status_var.set("Speech stopped")
        except Exception as error:
            messagebox.showerror("Error", f"Could not stop speech:\n{error}")

    # ------------------------------------------------------------------
    # CLEAR FUNCTION
    # ------------------------------------------------------------------
    def clear_text(self):
        """Clears all text from the text box."""
        self.text_area.delete("1.0", tk.END)
        self.status_var.set("Ready")


def main():
    """Entry point of the application."""
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
