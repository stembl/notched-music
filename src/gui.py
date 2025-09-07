"""
GUI module for the Notched Music application using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
import logging
from typing import Optional

from audio_processor import AudioProcessor

logger = logging.getLogger(__name__)


class NotchedMusicGUI:
    """Main GUI class for the Notched Music application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Notched Music - Audio Notch Filter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.notch_frequency = tk.DoubleVar(value=1000.0)
        self.quality_factor = tk.DoubleVar(value=30.0)
        self.frequency_range = tk.DoubleVar(value=50.0)  # Default 50 Hz range
        self.use_frequency_range = tk.BooleanVar(value=False)  # Toggle between Q and range
        self.new_artist = tk.StringVar()
        self.new_album = tk.StringVar()
        self.advanced_mode = tk.BooleanVar(value=False)
        
        # Audio processor
        self.audio_processor = None
        
        # Processing state
        self.is_processing = False
        
        self.setup_ui()
        self.setup_logging()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Notched Music", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input directory selection
        ttk.Label(main_frame, text="Input Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_dir, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_input_dir).grid(row=1, column=2, padx=(0, 0))
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_output_dir).grid(row=2, column=2, padx=(0, 0))
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Notch frequency
        ttk.Label(main_frame, text="Notch Frequency (Hz):").grid(row=4, column=0, sticky=tk.W, pady=5)
        frequency_frame = ttk.Frame(main_frame)
        frequency_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        frequency_frame.columnconfigure(0, weight=1)
        
        frequency_scale = ttk.Scale(frequency_frame, from_=20, to=20000, 
                                   variable=self.notch_frequency, orient=tk.HORIZONTAL)
        frequency_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        frequency_entry = ttk.Entry(frequency_frame, textvariable=self.notch_frequency, width=10)
        frequency_entry.grid(row=0, column=1, padx=(5, 0))
        
        # Quality factor
        ttk.Label(main_frame, text="Quality Factor:").grid(row=5, column=0, sticky=tk.W, pady=5)
        quality_frame = ttk.Frame(main_frame)
        quality_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        quality_frame.columnconfigure(0, weight=1)
        
        quality_scale = ttk.Scale(quality_frame, from_=1, to=100, 
                                 variable=self.quality_factor, orient=tk.HORIZONTAL)
        quality_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        quality_entry = ttk.Entry(quality_frame, textvariable=self.quality_factor, width=10)
        quality_entry.grid(row=0, column=1, padx=(5, 0))
        
        # Frequency range controls
        range_frame = ttk.LabelFrame(main_frame, text="Notch Width Control", padding="5")
        range_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        range_frame.columnconfigure(1, weight=1)
        
        # Toggle between Q factor and frequency range
        ttk.Radiobutton(range_frame, text="Use Quality Factor (Q)", 
                       variable=self.use_frequency_range, value=False,
                       command=self.toggle_range_mode).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(range_frame, text="Use Frequency Range", 
                       variable=self.use_frequency_range, value=True,
                       command=self.toggle_range_mode).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Frequency range controls (initially disabled)
        self.range_label = ttk.Label(range_frame, text="Frequency Range (Hz):")
        self.range_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        range_control_frame = ttk.Frame(range_frame)
        range_control_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        range_control_frame.columnconfigure(0, weight=1)
        
        self.range_scale = ttk.Scale(range_control_frame, from_=1, to=500, 
                                    variable=self.frequency_range, orient=tk.HORIZONTAL)
        self.range_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.range_entry = ttk.Entry(range_control_frame, textvariable=self.frequency_range, width=10)
        self.range_entry.grid(row=0, column=1, padx=(5, 0))
        
        # Initially disable range controls
        self.toggle_range_mode()
        
        # Advanced options checkbox
        advanced_check = ttk.Checkbutton(main_frame, text="Advanced Options", 
                                        variable=self.advanced_mode, command=self.toggle_advanced)
        advanced_check.grid(row=7, column=0, columnspan=3, pady=10)
        
        # Advanced options frame
        self.advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Options", padding="10")
        self.advanced_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        self.advanced_frame.columnconfigure(1, weight=1)
        
        # Artist name
        ttk.Label(self.advanced_frame, text="New Artist Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.advanced_frame, textvariable=self.new_artist, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Album name
        ttk.Label(self.advanced_frame, text="New Album Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.advanced_frame, textvariable=self.new_album, width=40).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Initially hide advanced options
        self.advanced_frame.grid_remove()
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Process Audio Files", 
                                        command=self.start_processing, style="Accent.TButton")
        self.process_button.grid(row=9, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to process audio files")
        self.status_label.grid(row=11, column=0, columnspan=3, pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="5")
        log_frame.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(12, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def setup_logging(self):
        """Set up logging to display in the GUI."""
        # Create a custom handler for the GUI
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
        
        # Add handler to logger
        gui_handler = GUILogHandler(self.log_text)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(gui_handler)
        logger.setLevel(logging.INFO)
    
    def browse_input_dir(self):
        """Browse for input directory."""
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir.set(directory)
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def toggle_advanced(self):
        """Toggle advanced options visibility."""
        if self.advanced_mode.get():
            self.advanced_frame.grid()
        else:
            self.advanced_frame.grid_remove()
    
    def toggle_range_mode(self):
        """Toggle between quality factor and frequency range modes."""
        if self.use_frequency_range.get():
            # Enable frequency range controls
            self.range_label.config(state='normal')
            self.range_scale.config(state='normal')
            self.range_entry.config(state='normal')
        else:
            # Disable frequency range controls
            self.range_label.config(state='disabled')
            self.range_scale.config(state='disabled')
            self.range_entry.config(state='disabled')
    
    def validate_inputs(self) -> bool:
        """Validate user inputs."""
        if not self.input_dir.get():
            messagebox.showerror("Error", "Please select an input directory")
            return False
        
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory")
            return False
        
        if not os.path.exists(self.input_dir.get()):
            messagebox.showerror("Error", "Input directory does not exist")
            return False
        
        if self.notch_frequency.get() <= 0:
            messagebox.showerror("Error", "Notch frequency must be greater than 0")
            return False
        
        if self.quality_factor.get() <= 0:
            messagebox.showerror("Error", "Quality factor must be greater than 0")
            return False
        
        if self.use_frequency_range.get() and self.frequency_range.get() <= 0:
            messagebox.showerror("Error", "Frequency range must be greater than 0")
            return False
        
        return True
    
    def start_processing(self):
        """Start the audio processing in a separate thread."""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing is already in progress")
            return
        
        # Disable the process button
        self.process_button.config(state='disabled')
        self.is_processing = True
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_audio_files)
        thread.daemon = True
        thread.start()
    
    def process_audio_files(self):
        """Process audio files (runs in separate thread)."""
        try:
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Initializing..."))
            
            # Create audio processor
            frequency_range = self.frequency_range.get() if self.use_frequency_range.get() else None
            self.audio_processor = AudioProcessor(
                notch_frequency=self.notch_frequency.get(),
                quality_factor=self.quality_factor.get(),
                frequency_range=frequency_range
            )
            
            # Get advanced options
            new_artist = self.new_artist.get() if self.advanced_mode.get() and self.new_artist.get() else None
            new_album = self.new_album.get() if self.advanced_mode.get() and self.new_album.get() else None
            
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Processing audio files..."))
            
            # Process files
            processed_files = self.audio_processor.process_directory(
                self.input_dir.get(),
                self.output_dir.get(),
                new_artist,
                new_album
            )
            
            # Update status
            self.root.after(0, lambda: self.status_label.config(
                text=f"Processing complete! {len(processed_files)} files processed successfully."
            ))
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Processing complete!\n\n{len(processed_files)} files processed successfully.\n\nOutput saved to: {self.output_dir.get()}"
            ))
            
        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            logger.error(error_msg)
            self.root.after(0, lambda: self.status_label.config(text="Error occurred during processing"))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Re-enable the process button
            self.root.after(0, lambda: self.process_button.config(state='normal'))
            self.is_processing = False


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = NotchedMusicGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

