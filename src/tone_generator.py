#!/usr/bin/env python3
"""
Tinnitus Frequency Identifier - Vintage Stereo Style
Based on National Panasonic SA-5800 aesthetic
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import threading
import time
import math
from typing import Optional

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: sounddevice not available. Install with: pip install sounddevice")

class TinnitusFrequencyIdentifier:
    """Tinnitus frequency identifier with vintage stereo receiver aesthetic."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tinnitus Frequency Identifier")
        self.root.geometry("1000x800")
        self.root.configure(bg='#C0C0C0')  # Silver brushed metal
        
        # Audio parameters
        self.sample_rate = 44100
        self.frequency = 1000.0  # Hz
        self.quality_factor = 30.0
        self.frequency_range_hz = 33.3  # Calculated from Q
        self.frequency_range_octaves = 0.1  # Calculated from Hz range
        self.amplitude = 0.3
        self.is_playing = False
        self.audio_stream = None
        
        # GUI variables
        self.freq_var = tk.DoubleVar(value=self.frequency)
        self.q_var = tk.DoubleVar(value=self.quality_factor)
        self.hz_range_var = tk.DoubleVar(value=self.frequency_range_hz)
        self.octave_range_var = tk.DoubleVar(value=self.frequency_range_octaves)
        
        # Update flags to prevent circular updates
        self.updating_q = False
        self.updating_hz = False
        self.updating_octave = False
        
        self.setup_vintage_ui()
        self.update_range_displays()
        
    def setup_vintage_ui(self):
        """Set up the vintage stereo receiver interface."""
        
        # Main frame with silver brushed metal background
        main_frame = tk.Frame(self.root, bg='#C0C0C0', relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Top title area
        title_frame = tk.Frame(main_frame, bg='#C0C0C0')
        title_frame.pack(fill='x', pady=(10, 5))
        
        title_label = tk.Label(title_frame, 
                              text="TINNITUS FREQUENCY IDENTIFIER", 
                              font=('Arial', 16, 'bold'),
                              fg='#000000',  # Black
                              bg='#C0C0C0')
        title_label.pack()
        
        # Main control panel with silver background
        control_frame = tk.Frame(main_frame, bg='#C0C0C0', relief='sunken', bd=1)
        control_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create the main display area (like the tuning dial)
        self.setup_tuning_display(control_frame)
        
        # Create control knobs and switches
        self.setup_controls(control_frame)
        
        # Add logo
        self.setup_logo(control_frame)
        
    def setup_tuning_display(self, parent):
        """Set up the main tuning display like the National Panasonic."""
        # Main display frame (black background like the tuning dial)
        display_frame = tk.Frame(parent, bg='#000000', relief='sunken', bd=3)
        display_frame.pack(fill='x', pady=(20, 30), padx=20)
        
        # Frequency scale frame
        scale_frame = tk.Frame(display_frame, bg='#000000')
        scale_frame.pack(fill='x', pady=10)
        
        # Create frequency scale (like FM/AM scales)
        self.create_frequency_scale(scale_frame)
        
        # Main frequency display (blue glowing numbers)
        freq_display_frame = tk.Frame(display_frame, bg='#000000')
        freq_display_frame.pack(pady=10)
        
        self.freq_display = tk.Label(freq_display_frame,
                                     text="1000.0",
                                     font=('Courier', 36, 'bold'),
                                     fg='#0080FF',  # Blue glowing
                                     bg='#000000',
                                     width=10)
        self.freq_display.pack()
        
        # Hz label
        hz_label = tk.Label(freq_display_frame,
                            text="Hz",
                            font=('Arial', 14, 'bold'),
                            fg='#0080FF',  # Blue glowing
                            bg='#000000')
        hz_label.pack()
        
        # Range indicators (neon green)
        range_frame = tk.Frame(display_frame, bg='#000000')
        range_frame.pack(fill='x', pady=(10, 20))
        
        # Left range (lower frequency)
        self.lower_range_label = tk.Label(range_frame,
                                          text="983.3",
                                          font=('Arial', 12, 'bold'),
                                          fg='#00FF00',  # Neon green
                                          bg='#000000')
        self.lower_range_label.pack(side='left', padx=30)
        
        # Center spacer with range indicator
        range_indicator = tk.Label(range_frame, 
                                  text="±", 
                                  font=('Arial', 16, 'bold'), 
                                  fg='#00FF00',  # Neon green
                                  bg='#000000')
        range_indicator.pack(side='left', expand=True)
        
        # Right range (upper frequency)
        self.upper_range_label = tk.Label(range_frame,
                                          text="1016.7",
                                          font=('Arial', 12, 'bold'),
                                          fg='#00FF00',  # Neon green
                                          bg='#000000')
        self.upper_range_label.pack(side='right', padx=30)
        
    def create_frequency_scale(self, parent):
        """Create the frequency scale like the tuning dial."""
        # Create a canvas for the frequency scale
        self.scale_canvas = tk.Canvas(parent, height=80, bg='#000000', highlightthickness=0)
        self.scale_canvas.pack(fill='x', padx=10)
        
        # Draw frequency scale
        self.draw_frequency_scale()
        
    def draw_frequency_scale(self):
        """Draw the frequency scale with markings."""
        self.scale_canvas.delete("all")
        
        width = self.scale_canvas.winfo_width()
        if width <= 1:  # Canvas not yet sized
            self.root.after(100, self.draw_frequency_scale)
            return
            
        height = 80
        
        # Draw frequency scale background
        self.scale_canvas.create_rectangle(0, 0, width, height, fill='#000000', outline='#333333')
        
        # Draw frequency markings (20 Hz to 20 kHz)
        freq_min, freq_max = 20, 20000
        
        # Major markings every 1000 Hz
        for freq in range(1000, 20001, 1000):
            x = (freq - freq_min) / (freq_max - freq_min) * (width - 40) + 20
            self.scale_canvas.create_line(x, height-20, x, height-5, fill='#00FF00', width=2)
            
            # Frequency labels
            if freq % 2000 == 0:  # Show every 2kHz
                self.scale_canvas.create_text(x, height-25, text=f"{freq//1000}k", 
                                            fill='#00FF00', font=('Arial', 8, 'bold'))
        
        # Draw bright yellow tuning indicator
        current_freq = self.frequency
        indicator_x = (current_freq - freq_min) / (freq_max - freq_min) * (width - 40) + 20
        self.scale_canvas.create_line(indicator_x, 5, indicator_x, height-30, fill='#FFFF00', width=3)
        
        # Draw range indicators (bright yellow)
        range_hz = self.frequency_range_hz
        lower_x = ((current_freq - range_hz) - freq_min) / (freq_max - freq_min) * (width - 40) + 20
        upper_x = ((current_freq + range_hz) - freq_min) / (freq_max - freq_min) * (width - 40) + 20
        
        if lower_x >= 20:
            self.scale_canvas.create_line(lower_x, height-15, lower_x, height-5, fill='#FFFF00', width=2)
        if upper_x <= width - 20:
            self.scale_canvas.create_line(upper_x, height-15, upper_x, height-5, fill='#FFFF00', width=2)
        
    def setup_controls(self, parent):
        """Set up the control knobs and switches like the National Panasonic."""
        # Controls frame
        controls_frame = tk.Frame(parent, bg='#C0C0C0')
        controls_frame.pack(fill='x', pady=20)
        
        # First row: Frequency tuning (dominates the row)
        freq_row_frame = tk.Frame(controls_frame, bg='#C0C0C0')
        freq_row_frame.pack(fill='x', pady=10)
        
        self.setup_frequency_tuning(freq_row_frame)
        
        # Second row: Range controls and power
        second_row_frame = tk.Frame(controls_frame, bg='#C0C0C0')
        second_row_frame.pack(fill='x', pady=10)
        
        # Left side: Range controls
        left_frame = tk.Frame(second_row_frame, bg='#C0C0C0')
        left_frame.pack(side='left', fill='both', expand=True, padx=20)
        
        # Right side: Power switch
        right_frame = tk.Frame(second_row_frame, bg='#C0C0C0')
        right_frame.pack(side='right', padx=20)
        
        # Range controls
        self.setup_range_controls(left_frame)
        
        # Power switch
        self.setup_power_switch(right_frame)
        
    def setup_frequency_tuning(self, parent):
        """Set up the main frequency tuning control (dominates first row)."""
        freq_frame = tk.Frame(parent, bg='#C0C0C0')
        freq_frame.pack(fill='x', pady=10)
        
        freq_label = tk.Label(freq_frame, text="FREQUENCY TUNING", font=('Arial', 14, 'bold'),
                             fg='#000000', bg='#C0C0C0')
        freq_label.pack()
        
        freq_knob_frame = tk.Frame(freq_frame, bg='#C0C0C0')
        freq_knob_frame.pack(fill='x', pady=10)
        
        self.freq_scale = tk.Scale(freq_knob_frame,
                                   from_=20, to=20000, resolution=1,
                                   orient='horizontal', length=600,
                                   variable=self.freq_var, command=self.on_frequency_change,
                                   font=('Arial', 10), fg='#000000', bg='#C0C0C0',
                                   troughcolor='#A0A0A0', activebackground='#E0E0E0',
                                   highlightbackground='#C0C0C0')
        self.freq_scale.pack()
        
        # Frequency range labels
        range_labels_frame = tk.Frame(freq_knob_frame, bg='#C0C0C0')
        range_labels_frame.pack(fill='x')
        
        tk.Label(range_labels_frame, text="20 Hz", font=('Arial', 10, 'bold'), 
                fg='#000000', bg='#C0C0C0').pack(side='left')
        tk.Label(range_labels_frame, text="20 kHz", font=('Arial', 10, 'bold'), 
                fg='#000000', bg='#C0C0C0').pack(side='right')
        
    def setup_range_controls(self, parent):
        """Set up range control knobs (Quality Factor, Frequency Range, and Octaves side by side)."""
        # Horizontal frame for all three range controls
        range_frame = tk.Frame(parent, bg='#C0C0C0')
        range_frame.pack(fill='x', pady=10)
        
        # Quality Factor knob (left side)
        q_frame = tk.Frame(range_frame, bg='#C0C0C0')
        q_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        q_label = tk.Label(q_frame, text="QUALITY FACTOR", font=('Arial', 10, 'bold'),
                          fg='#000000', bg='#C0C0C0')
        q_label.pack()
        
        q_knob_frame = tk.Frame(q_frame, bg='#C0C0C0')
        q_knob_frame.pack(pady=5)
        
        self.q_scale = tk.Scale(q_knob_frame,
                                from_=1, to=100, resolution=1,
                                orient='horizontal', length=150,
                                variable=self.q_var, command=self.on_q_change,
                                font=('Arial', 8), fg='#000000', bg='#C0C0C0',
                                troughcolor='#A0A0A0', activebackground='#E0E0E0',
                                highlightbackground='#C0C0C0')
        self.q_scale.pack()
        
        self.q_value_label = tk.Label(q_knob_frame, text="30.0", font=('Arial', 10, 'bold'),
                                     fg='#000000', bg='#C0C0C0')
        self.q_value_label.pack()
        
        # Hz Range knob (center)
        hz_frame = tk.Frame(range_frame, bg='#C0C0C0')
        hz_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        hz_label = tk.Label(hz_frame, text="FREQUENCY RANGE", font=('Arial', 10, 'bold'),
                           fg='#000000', bg='#C0C0C0')
        hz_label.pack()
        
        hz_knob_frame = tk.Frame(hz_frame, bg='#C0C0C0')
        hz_knob_frame.pack(pady=5)
        
        self.hz_scale = tk.Scale(hz_knob_frame,
                                 from_=1, to=500, resolution=0.1,
                                 orient='horizontal', length=150,
                                 variable=self.hz_range_var, command=self.on_hz_range_change,
                                 font=('Arial', 8), fg='#000000', bg='#C0C0C0',
                                 troughcolor='#A0A0A0', activebackground='#E0E0E0',
                                 highlightbackground='#C0C0C0')
        self.hz_scale.pack()
        
        self.hz_value_label = tk.Label(hz_knob_frame, text="33.3", font=('Arial', 10, 'bold'),
                                       fg='#000000', bg='#C0C0C0')
        self.hz_value_label.pack()
        
        # Octaves Range knob (right side)
        oct_frame = tk.Frame(range_frame, bg='#C0C0C0')
        oct_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        oct_label = tk.Label(oct_frame, text="OCTAVES RANGE", font=('Arial', 10, 'bold'),
                            fg='#000000', bg='#C0C0C0')
        oct_label.pack()
        
        oct_knob_frame = tk.Frame(oct_frame, bg='#C0C0C0')
        oct_knob_frame.pack(pady=5)
        
        self.oct_scale = tk.Scale(oct_knob_frame,
                                  from_=0.0, to=1.0, resolution=0.01,
                                  orient='horizontal', length=150,
                                  variable=self.octave_range_var, command=self.on_octave_range_change,
                                  font=('Arial', 8), fg='#000000', bg='#C0C0C0',
                                  troughcolor='#A0A0A0', activebackground='#E0E0E0',
                                  highlightbackground='#C0C0C0')
        self.oct_scale.pack()
        
        self.oct_value_label = tk.Label(oct_knob_frame, text="0.1", font=('Arial', 10, 'bold'),
                                        fg='#000000', bg='#C0C0C0')
        self.oct_value_label.pack()
        
    def setup_power_switch(self, parent):
        """Set up the power switch (toggle style)."""
        power_frame = tk.Frame(parent, bg='#C0C0C0')
        power_frame.pack(pady=10)
        
        power_label = tk.Label(power_frame, text="POWER", font=('Arial', 12, 'bold'),
                              fg='#000000', bg='#C0C0C0')
        power_label.pack()
        
        # Toggle switch frame
        switch_frame = tk.Frame(power_frame, bg='#C0C0C0')
        switch_frame.pack(pady=5)
        
        # Create toggle switch appearance
        self.power_button = tk.Button(switch_frame,
                                      text="OFF",
                                      font=('Arial', 14, 'bold'),
                                      fg='#FFFFFF',
                                      bg='#808080',  # Gray when off
                                      activebackground='#00FF00',
                                      activeforeground='#000000',
                                      relief='raised',
                                      bd=3,
                                      width=6,
                                      height=2,
                                      command=self.toggle_power)
        self.power_button.pack()
        
    def setup_logo(self, parent):
        """Set up the logo in bottom right."""
        logo_frame = tk.Frame(parent, bg='#C0C0C0')
        logo_frame.pack(side='bottom', anchor='se', padx=20, pady=10)
        
        logo_label = tk.Label(logo_frame,
                              text="Pinocchio's Wooden Heart",
                              font=('Arial', 10, 'normal'),
                              fg='#000000',
                              bg='#C0C0C0')
        logo_label.pack()
    
    def on_frequency_change(self, value):
        """Handle frequency knob changes."""
        self.frequency = float(value)
        self.update_range_displays()
        
    def on_q_change(self, value):
        """Handle quality factor changes."""
        if self.updating_q:
            return
            
        self.updating_hz = True
        self.updating_octave = True
        
        self.quality_factor = float(value)
        self.frequency_range_hz = self.frequency / self.quality_factor
        self.frequency_range_octaves = self.hz_to_octaves(self.frequency_range_hz)
        
        self.hz_range_var.set(self.frequency_range_hz)
        self.octave_range_var.set(self.frequency_range_octaves)
        
        self.update_range_displays()
        
        self.updating_hz = False
        self.updating_octave = False
        
    def on_hz_range_change(self, value):
        """Handle Hz range changes."""
        if self.updating_hz:
            return
            
        self.updating_q = True
        self.updating_octave = True
        
        self.frequency_range_hz = float(value)
        self.quality_factor = self.frequency / self.frequency_range_hz
        self.frequency_range_octaves = self.hz_to_octaves(self.frequency_range_hz)
        
        self.q_var.set(self.quality_factor)
        self.octave_range_var.set(self.frequency_range_octaves)
        
        self.update_range_displays()
        
        self.updating_q = False
        self.updating_octave = False
        
    def on_octave_range_change(self, value):
        """Handle octave range changes."""
        if self.updating_octave:
            return
            
        self.updating_q = True
        self.updating_hz = True
        
        self.frequency_range_octaves = float(value)
        self.frequency_range_hz = self.octaves_to_hz(self.frequency_range_octaves)
        if self.frequency_range_hz > 0:
            self.quality_factor = self.frequency / self.frequency_range_hz
        else:
            self.quality_factor = 1.0
        
        self.q_var.set(self.quality_factor)
        self.hz_range_var.set(self.frequency_range_hz)
        
        self.update_range_displays()
        
        self.updating_q = False
        self.updating_hz = False
        
    def toggle_power(self):
        """Toggle power on/off."""
        if self.is_playing:
            self.stop_playback()
            self.power_button.config(text="OFF", bg='#808080', fg='#FFFFFF')
        else:
            self.start_playback()
            self.power_button.config(text="ON", bg='#00FF00', fg='#000000')
        
    def hz_to_octaves(self, hz_range):
        """Convert Hz range to octave range."""
        # For small ranges, octaves ≈ log2(1 + hz_range/frequency)
        return math.log2(1 + hz_range / self.frequency)
        
    def octaves_to_hz(self, octave_range):
        """Convert octave range to Hz range."""
        # For small ranges, hz_range ≈ frequency * (2^octave_range - 1)
        return self.frequency * (2**octave_range - 1)
        
    def get_frequency_weighting(self, frequency):
        """Calculate frequency weighting for equal perceived loudness.
        
        Uses A-weighting curve approximation for frequencies 20Hz-20kHz.
        Returns a multiplier to adjust amplitude for equal perceived loudness.
        """
        if frequency < 20 or frequency > 20000:
            return 0.1  # Very low amplitude for out-of-range frequencies
            
        # A-weighting curve approximation
        # Based on ISO 226:2003 equal-loudness contours
        f = frequency
        
        # A-weighting formula (simplified)
        # A(f) = 1.2588966 * 148840000 * f^4 / ((f^2 + 424.36) * sqrt((f^2 + 11599.29)^2 - f^2 * 462.4^2) * (f^2 + 148840000))
        
        # Simplified approximation for practical use
        if f < 1000:
            # Low frequencies need more amplitude
            weight = 1.0 + (1000 - f) / 1000 * 0.8
        elif f < 4000:
            # Mid frequencies are reference (weight = 1.0)
            weight = 1.0
        else:
            # High frequencies need less amplitude
            weight = 1.0 - (f - 4000) / 16000 * 0.6
            
        # Ensure weight is within reasonable bounds
        weight = max(0.1, min(2.0, weight))
        
        return weight
        
    def update_range_displays(self):
        """Update all range displays."""
        # Update main frequency display to show sweep range
        lower_freq = self.frequency - self.frequency_range_hz
        upper_freq = self.frequency + self.frequency_range_hz
        self.freq_display.config(text=f"{self.frequency:.1f}")
        
        # Update range labels to show sweep boundaries
        self.lower_range_label.config(text=f"{lower_freq:.1f}")
        self.upper_range_label.config(text=f"{upper_freq:.1f}")
        
        # Update slider value labels
        self.q_value_label.config(text=f"{self.quality_factor:.1f}")
        self.hz_value_label.config(text=f"{self.frequency_range_hz:.1f}")
        self.oct_value_label.config(text=f"{self.frequency_range_octaves:.2f}")
        
        # Redraw the frequency scale
        self.draw_frequency_scale()
        
    def toggle_playback(self):
        """Toggle audio playback."""
        if self.is_playing:
            self.stop_playback()
        else:
            self.start_playback()
            
    def start_playback(self):
        """Start audio playback."""
        if not AUDIO_AVAILABLE:
            return
            
        try:
            self.is_playing = True
            self.power_button.config(text="ON", bg='#00FF00', fg='#000000')
            
            # Start audio stream
            self.audio_stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
                callback=self.audio_callback
            )
            self.audio_stream.start()
            
        except Exception as e:
            self.is_playing = False
            
    def stop_playback(self):
        """Stop audio playback."""
        self.is_playing = False
        self.power_button.config(text="OFF", bg='#808080', fg='#FFFFFF')
        
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
            self.audio_stream = None
            
    def audio_callback(self, outdata, frames, time, status):
        """Audio callback function."""
        if status:
            print(f"Audio status: {status}")
            
        if self.is_playing:
            # Generate frequency sweep across the defined range
            t = np.arange(frames) / self.sample_rate
            
            # Calculate frequency range boundaries
            lower_freq = max(20, self.frequency - self.frequency_range_hz)
            upper_freq = min(20000, self.frequency + self.frequency_range_hz)
            
            # Create frequency sweep pattern
            # Use logarithmic sweep for more natural progression
            sweep_duration = 2.0  # 2 seconds for full sweep cycle
            sweep_phase = (time.inputBufferAdcTime % sweep_duration) / sweep_duration
            
            # Logarithmic frequency sweep
            if lower_freq > 0 and upper_freq > lower_freq:
                log_lower = math.log10(lower_freq)
                log_upper = math.log10(upper_freq)
                current_log_freq = log_lower + sweep_phase * (log_upper - log_lower)
                current_freq = 10 ** current_log_freq
            else:
                current_freq = self.frequency
            
            # Apply frequency weighting for equal perceived loudness
            frequency_weight = self.get_frequency_weighting(current_freq)
            weighted_amplitude = self.amplitude * frequency_weight
            
            # Generate the main tone at current sweep frequency
            main_tone = weighted_amplitude * np.sin(2 * np.pi * current_freq * t)
            
            # Add notch filter effect based on Quality Factor
            if self.quality_factor > 1:
                # Calculate notch depth based on quality factor
                q_factor = min(self.quality_factor / 100.0, 1.0)  # Normalize to 0-1
                notch_depth = q_factor * 0.2  # Maximum 20% reduction
                
                # Create notch by adding out-of-phase tones at nearby frequencies
                notch_freq1 = current_freq * 0.95  # Slightly below
                notch_freq2 = current_freq * 1.05  # Slightly above
                
                notch_tone1 = notch_depth * weighted_amplitude * np.sin(2 * np.pi * notch_freq1 * t + np.pi)
                notch_tone2 = notch_depth * weighted_amplitude * np.sin(2 * np.pi * notch_freq2 * t + np.pi)
                
                # Combine main tone with notch effect
                wave = main_tone + notch_tone1 + notch_tone2
            else:
                wave = main_tone
                
            outdata[:, 0] = wave.astype(np.float32)
        else:
            outdata.fill(0)

def main():
    """Main function to run the tinnitus frequency identifier."""
    root = tk.Tk()
    app = TinnitusFrequencyIdentifier(root)
    
    # Handle window close
    def on_closing():
        app.stop_playback()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
