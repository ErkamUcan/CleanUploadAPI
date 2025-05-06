import sys
import subprocess
import os

if len(sys.argv) != 2:
    print("Kullanım: python extract_audio.py <video_path>")
    sys.exit(1)

video_path = sys.argv[1]
base, _ = os.path.splitext(video_path)
audio_path = base + ".wav"

# FFmpeg komutunu çalıştır
subprocess.run(["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path])

print("Audio dosyası oluşturuldu:", audio_path)
