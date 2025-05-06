import whisper
import sys
import os

if len(sys.argv) != 2:
    print("Kullanım: python transcribe_audio.py <audio_path>")
    sys.exit(1)

audio_path = sys.argv[1]
base, _ = os.path.splitext(audio_path)
output_path = os.path.join("Transcripts", os.path.basename(base) + ".txt")

model = whisper.load_model("medium")  # İstersen "small", "medium", "large" da kullanabilirsin
result = model.transcribe(audio_path)

os.makedirs("Transcripts", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Transkripsiyon tamamlandı:", output_path)
