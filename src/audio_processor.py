"""
Audio processing module for applying notch filters to audio files.
"""

import os
import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from mutagen import File as MutagenFile
from mutagen.id3 import ID3NoHeaderError
import eyed3
import logging
from typing import Tuple, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handles audio file processing including notch filtering and metadata editing."""
    
    SUPPORTED_FORMATS = {'.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a'}
    
    def __init__(self, notch_frequency: float, quality_factor: float = 30.0, frequency_range: float = None):
        """
        Initialize the audio processor.
        
        Args:
            notch_frequency: Center frequency to notch out in Hz
            quality_factor: Quality factor for the notch filter (higher = sharper notch)
            frequency_range: Width of the notch in Hz (if None, uses quality_factor)
        """
        self.notch_frequency = notch_frequency
        self.quality_factor = quality_factor
        self.frequency_range = frequency_range
        self.sample_rate = None
        
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file and return audio data and sample rate.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            audio_data, sample_rate = librosa.load(file_path, sr=None, mono=False)
            self.sample_rate = sample_rate
            logger.info(f"Loaded audio file: {file_path}, shape: {audio_data.shape}, sr: {sample_rate}")
            return audio_data, sample_rate
        except Exception as e:
            logger.error(f"Error loading audio file {file_path}: {e}")
            raise
    
    def apply_notch_filter(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Apply notch filter to audio data.
        
        Args:
            audio_data: Audio data array
            sample_rate: Sample rate of the audio
            
        Returns:
            Filtered audio data
        """
        try:
            # Design notch filter
            nyquist = sample_rate / 2
            normalized_freq = self.notch_frequency / nyquist
            
            # Ensure frequency is within valid range
            if normalized_freq >= 1.0:
                logger.warning(f"Notch frequency {self.notch_frequency} Hz is too high for sample rate {sample_rate} Hz")
                return audio_data
            
            # Calculate effective quality factor based on frequency range
            if self.frequency_range is not None:
                # Convert frequency range to quality factor
                # Q = center_frequency / bandwidth
                effective_q = self.notch_frequency / self.frequency_range
                logger.info(f"Using frequency range {self.frequency_range} Hz (Q = {effective_q:.2f})")
            else:
                effective_q = self.quality_factor
                logger.info(f"Using quality factor Q = {effective_q}")
            
            # Design IIR notch filter
            b, a = signal.iirnotch(self.notch_frequency, effective_q, sample_rate)
            
            # Apply filter
            if audio_data.ndim == 1:
                # Mono audio
                filtered_audio = signal.filtfilt(b, a, audio_data)
            else:
                # Multi-channel audio
                filtered_audio = np.zeros_like(audio_data)
                for channel in range(audio_data.shape[0]):
                    filtered_audio[channel] = signal.filtfilt(b, a, audio_data[channel])
            
            logger.info(f"Applied notch filter at {self.notch_frequency} Hz")
            return filtered_audio
            
        except Exception as e:
            logger.error(f"Error applying notch filter: {e}")
            raise
    
    def save_audio(self, audio_data: np.ndarray, sample_rate: int, output_path: str, 
                   original_format: str = 'wav') -> None:
        """
        Save filtered audio data to MP3 file.
        
        Args:
            audio_data: Filtered audio data
            sample_rate: Sample rate of the audio
            output_path: Path to save the output file (will be converted to .mp3)
            original_format: Original file format (for logging)
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert output path to MP3
            mp3_output_path = str(Path(output_path).with_suffix('.mp3'))
            
            # Save audio data as MP3
            sf.write(mp3_output_path, audio_data.T if audio_data.ndim > 1 else audio_data, sample_rate)
            
            logger.info(f"Saved filtered audio as MP3 to: {mp3_output_path}")
            
        except Exception as e:
            logger.error(f"Error saving audio as MP3: {e}")
            raise
    
    def copy_metadata(self, source_path: str, target_path: str, 
                     new_artist: Optional[str] = None, new_album: Optional[str] = None) -> None:
        """
        Copy metadata from source file to target MP3 file, optionally modifying artist and album.
        
        Args:
            source_path: Path to source audio file
            target_path: Path to target MP3 file (will be converted to .mp3)
            new_artist: New artist name (optional)
            new_album: New album name (optional)
        """
        try:
            # Convert target path to MP3 for metadata copying
            mp3_target_path = str(Path(target_path).with_suffix('.mp3'))
            
            # Always use MP3 metadata copying since all outputs are MP3
            self._copy_mp3_metadata(source_path, mp3_target_path, new_artist, new_album)
            
            logger.info(f"Copied and updated metadata from {source_path} to {mp3_target_path}")
            
        except Exception as e:
            logger.error(f"Error copying metadata: {e}")
            # Don't raise exception as metadata copying is not critical
    
    def _copy_mp3_metadata(self, source_path: str, target_path: str, 
                          new_artist: Optional[str] = None, new_album: Optional[str] = None) -> None:
        """Copy metadata for MP3 files using eyed3."""
        try:
            # Load target file
            target_mp3 = eyed3.load(target_path)
            
            if target_mp3 is None:
                logger.warning(f"Could not load target file {target_path}")
                return
            
            # Ensure target has tags
            if target_mp3.tag is None:
                target_mp3.initTag()
            
            # Try to load source metadata, but don't fail if it doesn't exist
            source_mp3 = eyed3.load(source_path)
            source_tag = None
            
            if source_mp3 is not None and source_mp3.tag is not None:
                source_tag = source_mp3.tag
                logger.info(f"Found metadata in source file {source_path}")
                
                # Copy basic tags with error handling
                try:
                    if hasattr(source_tag, 'artist') and source_tag.artist:
                        target_mp3.tag.artist = source_tag.artist
                except Exception as e:
                    logger.debug(f"Could not copy artist: {e}")
                
                try:
                    if hasattr(source_tag, 'album') and source_tag.album:
                        target_mp3.tag.album = source_tag.album
                except Exception as e:
                    logger.debug(f"Could not copy album: {e}")
                
                try:
                    if hasattr(source_tag, 'title') and source_tag.title:
                        target_mp3.tag.title = source_tag.title
                except Exception as e:
                    logger.debug(f"Could not copy title: {e}")
                
                try:
                    if hasattr(source_tag, 'track_num') and source_tag.track_num:
                        # Handle track number carefully - it might be a CountAndTotalTuple
                        if hasattr(source_tag.track_num, 'count'):
                            # It's a CountAndTotalTuple, extract just the count
                            target_mp3.tag.track_num = source_tag.track_num.count
                        else:
                            target_mp3.tag.track_num = source_tag.track_num
                except Exception as e:
                    logger.debug(f"Could not copy track number: {e}")
                
                try:
                    if hasattr(source_tag, 'genre') and source_tag.genre:
                        target_mp3.tag.genre = source_tag.genre
                except Exception as e:
                    logger.debug(f"Could not copy genre: {e}")
                
                try:
                    if hasattr(source_tag, 'year') and source_tag.year:
                        target_mp3.tag.year = source_tag.year
                except Exception as e:
                    logger.debug(f"Could not copy year: {e}")
            else:
                logger.info(f"No metadata found in source file {source_path}, creating new tags")
            
            # Override with new values if specified
            if new_artist:
                target_mp3.tag.artist = new_artist
                logger.info(f"Set artist to: {new_artist}")
            else:
                logger.info("No new artist specified")
            
            if new_album:
                target_mp3.tag.album = new_album
                logger.info(f"Set album to: {new_album}")
            else:
                logger.info("No new album specified")
            
            # Save the tags
            target_mp3.tag.save()
            
        except Exception as e:
            logger.error(f"Error copying MP3 metadata: {e}")
    
    def _copy_other_metadata(self, source_path: str, target_path: str, 
                           new_artist: Optional[str] = None, new_album: Optional[str] = None) -> None:
        """Copy metadata for non-MP3 files using mutagen."""
        try:
            # Load target file
            target_file = MutagenFile(target_path)
            
            if target_file is None:
                logger.warning(f"Could not load target file {target_path}")
                return
            
            # Try to load source metadata, but don't fail if it doesn't exist
            source_file = MutagenFile(source_path)
            
            if source_file is not None:
                logger.info(f"Found metadata in source file {source_path}")
                
                # Copy all tags safely
                for key, value in source_file.items():
                    try:
                        # Only copy if the value is valid
                        if value is not None:
                            target_file[key] = value
                    except Exception as e:
                        logger.debug(f"Could not copy tag {key}: {e}")
                        continue
            else:
                logger.info(f"No metadata found in source file {source_path}, creating new tags")
            
            # Update artist and album if specified
            if new_artist:
                try:
                    # For WAV files, we need to use ID3 tags
                    if hasattr(target_file, 'tags') and target_file.tags is None:
                        target_file.add_tags()
                    
                    if hasattr(target_file, 'tags') and target_file.tags is not None:
                        # Use ID3 tags for WAV files
                        from mutagen.id3 import TPE1
                        target_file.tags['TPE1'] = TPE1(encoding=3, text=new_artist)
                    else:
                        # Fallback for other formats
                        target_file['artist'] = new_artist
                    logger.info(f"Set artist to: {new_artist}")
                except Exception as e:
                    logger.debug(f"Could not set artist tag: {e}")
            
            if new_album:
                try:
                    # For WAV files, we need to use ID3 tags
                    if hasattr(target_file, 'tags') and target_file.tags is None:
                        target_file.add_tags()
                    
                    if hasattr(target_file, 'tags') and target_file.tags is not None:
                        # Use ID3 tags for WAV files
                        from mutagen.id3 import TALB
                        target_file.tags['TALB'] = TALB(encoding=3, text=new_album)
                    else:
                        # Fallback for other formats
                        target_file['album'] = new_album
                    logger.info(f"Set album to: {new_album}")
                except Exception as e:
                    logger.debug(f"Could not set album tag: {e}")
            
            # Save metadata
            target_file.save()
            
        except Exception as e:
            logger.error(f"Error copying other metadata: {e}")
    
    def process_file(self, input_path: str, output_path: str, 
                    new_artist: Optional[str] = None, new_album: Optional[str] = None) -> bool:
        """
        Process a single audio file: load, apply notch filter, save, and copy metadata.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            new_artist: New artist name (optional)
            new_album: New album name (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if file format is supported
            file_ext = Path(input_path).suffix.lower()
            if file_ext not in self.SUPPORTED_FORMATS:
                logger.warning(f"Unsupported file format: {file_ext}")
                return False
            
            # Load audio
            audio_data, sample_rate = self.load_audio(input_path)
            
            # Apply notch filter
            filtered_audio = self.apply_notch_filter(audio_data, sample_rate)
            
            # Save filtered audio
            self.save_audio(filtered_audio, sample_rate, output_path, file_ext)
            
            # Copy metadata
            self.copy_metadata(input_path, output_path, new_artist, new_album)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing file {input_path}: {e}")
            return False
    
    def process_directory(self, input_dir: str, output_dir: str, 
                         new_artist: Optional[str] = None, new_album: Optional[str] = None) -> List[str]:
        """
        Process all supported audio files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            new_artist: New artist name (optional)
            new_album: New album name (optional)
            
        Returns:
            List of successfully processed files
        """
        processed_files = []
        input_path = Path(input_dir)
        
        # Debug logging
        logger.info(f"Processing directory with new_artist='{new_artist}', new_album='{new_album}'")
        
        if not input_path.exists():
            logger.error(f"Input directory does not exist: {input_dir}")
            return processed_files
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all audio files
        audio_files = []
        for ext in self.SUPPORTED_FORMATS:
            audio_files.extend(input_path.glob(f"**/*{ext}"))
        
        logger.info(f"Found {len(audio_files)} audio files to process")
        
        # Process each file
        for audio_file in audio_files:
            relative_path = audio_file.relative_to(input_path)
            output_file = Path(output_dir) / relative_path
            
            logger.info(f"Processing: {audio_file}")
            if self.process_file(str(audio_file), str(output_file), new_artist, new_album):
                processed_files.append(str(audio_file))
            else:
                logger.error(f"Failed to process: {audio_file}")
        
        logger.info(f"Successfully processed {len(processed_files)} files")
        return processed_files

