import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from natsort import natsorted

from cbz_extractor import CBZExtractor
from stitcher import Stitcher
from settings_manager import SettingsManager
from logger import Logger


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CBZ AI Script Converter")
        self.geometry("900x700")

        self.cbz_paths = []

        self.settings = SettingsManager()
        self.config = self.settings.load()

        self.extractor = CBZExtractor()

        self.logger = Logger(
            callback=self.add_log
        )


        self.create_widgets()

    # --------------------------------------------------

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="CBZ AI Script Converter",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=20
        )

        # ------------------------------

        self.select_button = ctk.CTkButton(
            self,
            text="Select CBZ Files",
            command=self.select_cbz,
            width=220,
            height=40
        )

        self.select_button.pack(
            pady=10
        )

        # ------------------------------

        self.file_label = ctk.CTkLabel(
            self,
            text="No CBZ Selected"
        )

        self.file_label.pack(
            pady=5
        )

        # ------------------------------

        settings_frame = ctk.CTkFrame(self)

        settings_frame.pack(
            padx=20,
            pady=20,
            fill="x"
        )

        # Max Width

        ctk.CTkLabel(
            settings_frame,
            text="Max Width"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.width_entry = ctk.CTkEntry(
            settings_frame,
            width=120
        )

        self.width_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        self.width_entry.insert(
            0,
            str(self.config["max_width"])
        )

        # JPEG Quality

        ctk.CTkLabel(
            settings_frame,
            text="JPEG Quality"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.quality_entry = ctk.CTkEntry(
            settings_frame,
            width=120
        )

        self.quality_entry.grid(
            row=0,
            column=3,
            padx=10
        )

        self.quality_entry.insert(
            0,
            str(self.config["quality"])
        )

        # Pages Per Strip

        ctk.CTkLabel(
            settings_frame,
            text="Pages / Strip"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        self.pages_menu = ctk.CTkOptionMenu(
            settings_frame,
            values=[
                "5",
                "10",
                "15",
                "20"
            ]
        )

        self.pages_menu.grid(
            row=1,
            column=1,
            padx=10
        )

        self.pages_menu.set(
            str(self.config["pages_per_strip"])
        )

        # ------------------------------

        self.progress = ctk.CTkProgressBar(
            self,
            width=500
        )

        self.progress.pack(
            pady=20
        )

        self.progress.set(0)

        # ------------------------------

        self.log_box = ctk.CTkTextbox(
            self,
            height=220
        )

        self.log_box.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        self.create_bottom_buttons()

            # --------------------------------------------------
    # Buttons
    # --------------------------------------------------

    def create_bottom_buttons(self):

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.convert_button = ctk.CTkButton(
            button_frame,
            text="Convert",
            width=180,
            height=40,
            command=self.start_conversion
        )

        self.convert_button.grid(
            row=0,
            column=0,
            padx=10
        )

        self.output_button = ctk.CTkButton(
            button_frame,
            text="Open Output",
            width=180,
            height=40,
            command=self.open_output
        )

        self.output_button.grid(
            row=0,
            column=1,
            padx=10
        )

    # --------------------------------------------------

    def select_cbz(self):

        filenames = filedialog.askopenfilenames(
            title="Select CBZ Chapters",
            filetypes=[("CBZ Files", "*.cbz")]
        )

        if not filenames:
            return

        self.cbz_paths = natsorted(
            [str(path) for path in filenames],
            key=lambda path: os.path.basename(path).lower()
        )

        names = [os.path.basename(path) for path in self.cbz_paths]
        display = f"{len(names)} CBZ file(s): " + ", ".join(names)
        self.file_label.configure(text=display)

        self.logger.log(f"Selected {len(self.cbz_paths)} CBZ file(s) in natural order:")
        for filename in self.cbz_paths:
            self.logger.log(filename)

    # --------------------------------------------------

    def add_log(self, message):

        self.log_box.insert(
            "end",
            message + "\n"
        )

        self.log_box.see("end")

    # --------------------------------------------------

    def update_progress(self, value):

        self.progress.set(value)

        self.update_idletasks()

    # --------------------------------------------------

    def open_output(self):

        output = os.path.join(
            os.getcwd(),
            "Output"
        )

        os.makedirs(
            output,
            exist_ok=True
        )

        os.startfile(output)

            # --------------------------------------------------

    def save_settings(self):

        self.settings.save({
            "max_width": int(self.width_entry.get()),
            "quality": int(self.quality_entry.get()),
            "pages_per_strip": int(self.pages_menu.get())
        })

    # --------------------------------------------------

    def start_conversion(self):

        if not self.cbz_paths:
            messagebox.showerror(
                "Error",
                "Please select one or more CBZ files first."
            )
            return

        self.convert_button.configure(
            state="disabled"
        )

        thread = threading.Thread(
            target=self.convert,
            daemon=True
        )

        thread.start()

    # --------------------------------------------------

    def convert(self):

        try:
            self.progress.set(0)
            self.save_settings()
            config = self.settings.load()

            output_folder = os.path.join(os.getcwd(), "Output")
            os.makedirs(output_folder, exist_ok=True)

            # Strip numbering is shared across all selected chapters.
            next_part_number = 1
            total_chapters = len(self.cbz_paths)

            stitcher = Stitcher(
                max_width=config["max_width"],
                quality=config["quality"],
                pages_per_strip=config["pages_per_strip"]
            )

            for chapter_index, cbz_path in enumerate(self.cbz_paths, start=1):
                chapter_name = os.path.splitext(os.path.basename(cbz_path))[0]
                self.logger.log(f"[{chapter_index}/{total_chapters}] Extracting {chapter_name}...")

                images = self.extractor.extract_and_list(cbz_path)
                self.logger.log(f"Found {len(images)} image(s) in {chapter_name}.")
                if not images:
                    self.logger.log(f"Skipping {chapter_name}: no supported images found.")
                    self.extractor.cleanup()
                    continue

                self.logger.log(f"Creating strips for {chapter_name}...")
                # Existing strip creation, resizing, color handling, and JPEG quality stay unchanged.
                stitcher.stitch(
                    images,
                    chapter_name,
                    start_part_number=next_part_number
                )
                next_part_number += (len(images) + config["pages_per_strip"] - 1) // config["pages_per_strip"]
                self.extractor.cleanup()
                self.progress.set(chapter_index / total_chapters)

            if next_part_number == 1:
                raise ValueError("No supported images were found in the selected CBZ files.")

            self.progress.set(1.0)
            self.logger.log(f"Finished! Created {next_part_number - 1} strip(s) in {output_folder}.")
            messagebox.showinfo("Done", "Conversion completed successfully!")

        except Exception as e:
            self.logger.log(f"ERROR: {e}")
            messagebox.showerror("Error", str(e))

        finally:
            self.convert_button.configure(state="normal")
