import sys
import os
import traceback

try:
    import customtkinter as ctk
    from tkinter import filedialog
    from pydub import AudioSegment
    from pydub.generators import WhiteNoise
    import threading
    import shutil
except Exception as e:
    print("\n" + "="*60)
    print("X KRYTYCZNY BLAD: BRAK BIBLIOTEKI X")
    print("="*60)
    print(traceback.format_exc())
    print("="*60)
    input("\nWcisnij ENTER aby zamknac to okno...")
    sys.exit()

# =========================================================
# GLOWNY PROGRAM V-OMEGA (STUDIO MASTERING EDITION)
# =========================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdvancedAudioCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Audio Signature Cleaner by Swir - V-OMEGA")
        self.geometry("900x820")
        self.neon_blue = "#00bcff"
        self.selected_files = []
        self.output_dir = ""
        
        self.has_ffmpeg = shutil.which("ffmpeg") is not None
        self.has_ffprobe = shutil.which("ffprobe") is not None
        self.engine_ready = self.has_ffmpeg and self.has_ffprobe
        
        self.setup_ui()

    def setup_ui(self):
        # Pasek statusu
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(fill="x", padx=20, pady=(10, 0))
        
        if self.engine_ready:
            ffmpeg_text = "OK FFmpeg/FFprobe: WYKRYTO (Silnik gotowy)"
            ffmpeg_color = "#00ff00"
        else:
            ffmpeg_text = "ERROR FFmpeg/FFprobe: BRAK (Wymagane!)"
            ffmpeg_color = "#ff3333"

        self.label_ffmpeg = ctk.CTkLabel(self.frame_top, text=ffmpeg_text, font=("Roboto", 12, "bold"), text_color=ffmpeg_color)
        self.label_ffmpeg.pack(side="right")

        self.label_title = ctk.CTkLabel(self, text="AI Cleaner & RouteNote Master", font=("Roboto", 28, "bold"), text_color=self.neon_blue)
        self.label_title.pack(pady=(5, 5))

        self.label_desc = ctk.CTkLabel(self, text="Zacieranie sladow AI, phase-shift, analog hiss oraz inteligentny mastering do -1 dB.", font=("Roboto", 14), text_color="gray")
        self.label_desc.pack(pady=(0, 15))

        # --- PANEL INZYNIERYJNY (Toggles) ---
        self.frame_toggles = ctk.CTkFrame(self, fg_color="#141414", border_width=1, border_color=self.neon_blue)
        self.frame_toggles.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(self.frame_toggles, text="MODULY DSP (Digital Signal Processing):", font=("Roboto", 14, "bold"), text_color=self.neon_blue).grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=15, sticky="w")

        # Zmienne logiczne
        self.toggle_watermark = ctk.BooleanVar(value=True)
        self.toggle_phase = ctk.BooleanVar(value=True)
        self.toggle_noise = ctk.BooleanVar(value=True)
        self.toggle_mastering = ctk.BooleanVar(value=True)

        sw_1 = ctk.CTkSwitch(self.frame_toggles, text="1. Usun Watermark AI (16kHz / 20Hz)", variable=self.toggle_watermark, progress_color=self.neon_blue, font=("Roboto", 12))
        sw_1.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        sw_2 = ctk.CTkSwitch(self.frame_toggles, text="2. Rozbij Faze Stereo (Humanizacja)", variable=self.toggle_phase, progress_color=self.neon_blue, font=("Roboto", 12))
        sw_2.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        sw_3 = ctk.CTkSwitch(self.frame_toggles, text="3. Wstrzyknij Cieplo Tasmy (-45dB)", variable=self.toggle_noise, progress_color=self.neon_blue, font=("Roboto", 12))
        sw_3.grid(row=2, column=0, padx=20, pady=(10, 15), sticky="w")

        sw_4 = ctk.CTkSwitch(self.frame_toggles, text="4. Studio Mastering (Limit -1.0 dBFS)", variable=self.toggle_mastering, progress_color=self.neon_blue, font=("Roboto", 12))
        sw_4.grid(row=2, column=1, padx=20, pady=(10, 15), sticky="w")
        # ------------------------------------

        # Formatowanie wyjsciowe
        self.frame_options = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.frame_options.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.frame_options, text="Format Dystrybucyjny:", font=("Roboto", 14, "bold")).pack(side="top", pady=(10, 5))
        
        self.frame_radios = ctk.CTkFrame(self.frame_options, fg_color="transparent")
        self.frame_radios.pack(pady=(0, 10))

        self.format_var = ctk.StringVar(value="Zachowaj oryginalny")
        
        self.radio_orig = ctk.CTkRadioButton(self.frame_radios, text="Oryginalny", variable=self.format_var, value="Zachowaj oryginalny", fg_color=self.neon_blue)
        self.radio_mp3 = ctk.CTkRadioButton(self.frame_radios, text="Wymus MP3", variable=self.format_var, value="mp3", fg_color=self.neon_blue)
        self.radio_wav = ctk.CTkRadioButton(self.frame_radios, text="Wymus WAV", variable=self.format_var, value="wav", fg_color=self.neon_blue)
        self.radio_routenote = ctk.CTkRadioButton(self.frame_radios, text="RouteNote Ready (Stereo, 44.1kHz, 320k)", variable=self.format_var, value="routenote", fg_color=self.neon_blue)
        
        self.radio_orig.pack(side="left", padx=10)
        self.radio_mp3.pack(side="left", padx=10)
        self.radio_wav.pack(side="left", padx=10)
        self.radio_routenote.pack(side="left", padx=10)

        # Przyciski
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(pady=5)

        self.btn_file = ctk.CTkButton(self.frame_buttons, text="Wybierz Plik (WAV/MP3)", command=self.select_file, width=200, height=40, fg_color="transparent", border_width=2, border_color=self.neon_blue, text_color=self.neon_blue, hover_color="#003344")
        self.btn_file.pack(side="left", padx=10)

        self.btn_folder = ctk.CTkButton(self.frame_buttons, text="Wybierz Caly Folder", command=self.select_folder, width=200, height=40, fg_color="transparent", border_width=2, border_color=self.neon_blue, text_color=self.neon_blue, hover_color="#003344")
        self.btn_folder.pack(side="left", padx=10)

        self.textbox_log = ctk.CTkTextbox(self, width=800, height=180, font=("Consolas", 12), fg_color="#0d0d0d")
        self.textbox_log.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=800, progress_color=self.neon_blue)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        self.btn_start = ctk.CTkButton(self, text="INICJUJ SILNIK DSP (START)", command=self.start_processing_thread, width=300, height=50, font=("Roboto", 16, "bold"), fg_color=self.neon_blue, text_color="black", hover_color="#0099cc", state="disabled")
        self.btn_start.pack(pady=10)

        if self.engine_ready:
            self.log_message("System gotowy i autoryzowany. Wybierz pliki.")
        else:
            self.log_message("[BLAD] Brak FFmpeg. Program zablokowany.")
            self.btn_file.configure(state="disabled")
            self.btn_folder.configure(state="disabled")

    def log_message(self, message):
        self.after(0, self._insert_log, message)

    def _insert_log(self, message):
        self.textbox_log.insert("end", f"{message}\n")
        self.textbox_log.see("end")

    def update_progress(self, value):
        self.after(0, self.progress_bar.set, value)

    def set_buttons_state(self, state):
        self.after(0, lambda: self.btn_start.configure(state=state))
        self.after(0, lambda: self.btn_file.configure(state=state))
        self.after(0, lambda: self.btn_folder.configure(state=state))

    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if filepath:
            self.selected_files = [filepath]
            self.output_dir = os.path.dirname(filepath)
            self.log_message(f"[*] Zaladowano plik: {os.path.basename(filepath)}")
            self.set_buttons_state("normal")

    def select_folder(self):
        folderpath = filedialog.askdirectory()
        if folderpath:
            self.selected_files = [os.path.join(folderpath, f) for f in os.listdir(folderpath) if f.lower().endswith(('.mp3', '.wav'))]
            self.output_dir = folderpath
            self.log_message(f"[*] Zaladowano folder: {folderpath} | Plikow: {len(self.selected_files)}")
            if self.selected_files:
                self.set_buttons_state("normal")

    def start_processing_thread(self):
        self.set_buttons_state("disabled")
        self.update_progress(0)
        threading.Thread(target=self.process_files, daemon=True).start()

    def apply_stereo_phase_shift(self, audio):
        if audio.channels != 2:
            audio = audio.set_channels(2)
        left, right = audio.split_to_mono()
        delay = AudioSegment.silent(duration=1, frame_rate=audio.frame_rate)
        left = delay + left
        right = right + delay
        return AudioSegment.from_mono_audiosegments(left, right)

    def process_files(self):
        total_files = len(self.selected_files)
        save_dir = os.path.join(self.output_dir, "Cleaned_Export")
        os.makedirs(save_dir, exist_ok=True)
        target_format = self.format_var.get()
        
        self.log_message("\n================ SILNIK OMEGA URUCHOMIONY ================")
        for index, file_path in enumerate(self.selected_files):
            filename = os.path.basename(file_path)
            orig_ext = os.path.splitext(filename)[1].lower()
            base_name = os.path.splitext(filename)[0]
            self.log_message(f"\n---> Przetwarzanie: {filename}")
            
            try:
                audio = AudioSegment.from_file(file_path)
                
                # 1. Wyg?adzanie tranzjentow (Fade In / Fade Out) - 50ms (Usuwa trzaski z AI)
                audio = audio.fade_in(50).fade_out(50)

                # 2. Usuwanie znakow wodnych
                if self.toggle_watermark.get():
                    self.log_message("   [+] DSP: Filtracja AI (Low-Pass 16kHz & High-Pass 20Hz)")
                    audio = audio.high_pass_filter(20)
                    audio = audio.low_pass_filter(16000)
                
                # 3. Fazowanie przestrzenne
                if self.toggle_phase.get():
                    self.log_message("   [+] DSP: Humanizacja Fazy (Opoznienie kanalu L)")
                    audio = self.apply_stereo_phase_shift(audio)

                # Micro-Shift czasu (Robimy zawsze, to najlepszy obronca anty-detekcyjny)
                self.log_message("   [+] DSP: Rekalkulacja siatki czasowej o 0.5%")
                new_sample_rate = int(audio.frame_rate * 1.005)
                audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
                audio = audio.set_frame_rate(44100) 
                
                # 4. Szum analogowy
                if self.toggle_noise.get():
                    self.log_message("   [+] DSP: Saturacja tasmy (Wstrzykiwanie szumu -45dB)")
                    raw_noise = WhiteNoise().to_audio_segment(duration=len(audio), volume=-45.0)
                    filtered_noise = raw_noise.low_pass_filter(8000) 
                    audio = audio.overlay(filtered_noise)
                
                # 5. Studio Mastering (Normalizacja)
                if self.toggle_mastering.get():
                    current_max = audio.max_dBFS
                    target_dbfs = -1.0
                    change_in_db = target_dbfs - current_max
                    self.log_message(f"   [+] MASTERING: Normalizacja poziomu z {current_max:.2f}dB na {target_dbfs}dB")
                    audio = audio.apply_gain(change_in_db)
                
                # Formatowanie pliku
                if target_format == "routenote":
                    self.log_message("   [+] EXPORT: Optymalizacja RouteNote (Stereo, 44.1kHz, 320kbps)")
                    audio = audio.set_channels(2)
                    audio = audio.set_frame_rate(44100)
                    export_ext, export_fmt, bit_rate = ".mp3", "mp3", "320k"
                elif target_format == "mp3":
                    export_ext, export_fmt, bit_rate = ".mp3", "mp3", "320k"
                elif target_format == "wav":
                    export_ext, export_fmt, bit_rate = ".wav", "wav", None
                else: 
                    export_ext = orig_ext
                    export_fmt = orig_ext.replace(".", "")
                    bit_rate = "320k" if export_fmt == "mp3" else None

                prefix = "MASTER_" if target_format == "routenote" else "SECURE_"
                output_name = f"{prefix}{base_name}{export_ext}"
                output_path = os.path.join(save_dir, output_name)
                
                # WIPE METADANYCH
                clean_tags = {'artist': 'Independent', 'album': 'Single', 'title': base_name, 'encoded_by': 'Swir Audio Tools OMEGA'}
                if bit_rate:
                    audio.export(output_path, format=export_fmt, bitrate=bit_rate, tags=clean_tags)
                else:
                    audio.export(output_path, format=export_fmt, tags=clean_tags)
                
                final_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                self.log_message(f"   [OK] ZAPISANO: {output_name} ({final_size_mb:.2f} MB)")
                
            except Exception as e:
                self.log_message(f"   [BLAD KRYTYCZNY]: {str(e)}")
                self.log_message(traceback.format_exc())
            
            progress = (index + 1) / total_files
            self.update_progress(progress)
            
        self.log_message("\n================ PROCEDURA ZAKONCZONA ================")
        self.set_buttons_state("normal")
        self.update_progress(0)

if __name__ == "__main__":
    try:
        app = AdvancedAudioCleanerApp()
        app.mainloop()
    except Exception as e:
        print("\n" + "="*60)
        print("X KRYTYCZNY BLAD APLIKACJI X")
        print("="*60)
        print(traceback.format_exc())
        print("="*60)
        input("\nWcisnij ENTER aby zamknac okno...")
