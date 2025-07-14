#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import os
import sys
import random
import subprocess
import platform
from pathlib import Path

def get_audio_files(audio_type):
    """
    Get all audio files from the specified audio type directory.
    
    Args:
        audio_type (str): Type of audio ('notification', 'blocked', 'completed')
    
    Returns:
        list: List of audio file paths
    """
    # Get current script directory and construct audio path
    script_dir = Path(__file__).parent.parent
    audio_dir = script_dir / "audio" / audio_type
    
    if not audio_dir.exists():
        return []
    
    # Get all .wav files in the directory
    audio_files = list(audio_dir.glob("*.wav"))
    return [str(f) for f in audio_files]

def play_audio_file(file_path):
    """
    Play an audio file using the system's default audio player.
    
    Args:
        file_path (str): Path to the audio file to play
    """
    if not os.path.exists(file_path):
        return False
    
    try:
        system = platform.system().lower()
        
        if system == "darwin":  # macOS
            subprocess.run(["afplay", file_path], 
                         capture_output=True, timeout=10)
        elif system == "linux":
            # Try different audio players on Linux
            players = ["paplay", "aplay", "play"]
            for player in players:
                try:
                    subprocess.run([player, file_path], 
                                 capture_output=True, timeout=10, check=True)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
        elif system == "windows":
            # Windows PowerShell method
            subprocess.run([
                "powershell", "-c", 
                f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"
            ], capture_output=True, timeout=10)
        
        return True
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return False
    except Exception:
        return False

def play_random_audio(audio_type):
    """
    Play a random audio file from the specified type directory.
    
    Args:
        audio_type (str): Type of audio ('notification', 'blocked', 'completed')
    
    Returns:
        bool: True if audio was played successfully, False otherwise
    """
    audio_files = get_audio_files(audio_type)
    
    if not audio_files:
        return False
    
    # Choose a random audio file
    chosen_file = random.choice(audio_files)
    
    # Play the chosen file
    return play_audio_file(chosen_file)

def main():
    """Command line interface for audio player."""
    if len(sys.argv) != 2:
        print("Usage: ./audio_player.py <audio_type>")
        print("Audio types: notification, blocked, completed")
        sys.exit(1)
    
    audio_type = sys.argv[1].lower()
    
    # Validate audio type
    valid_types = ["notification", "blocked", "completed"]
    if audio_type not in valid_types:
        print(f"Error: Invalid audio type '{audio_type}'")
        print(f"Valid types: {', '.join(valid_types)}")
        sys.exit(1)
    
    # Play random audio
    success = play_random_audio(audio_type)
    
    if not success:
        print(f"Warning: Could not play audio for type '{audio_type}'", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()