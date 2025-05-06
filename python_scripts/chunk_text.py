import os
import sys
import nltk
print("NLTK başarıyla içe aktarıldı.")

# Gerekli tokenizer'ı indir
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Komut satırı argümanı kontrolü
if len(sys.argv) != 2:
    print(" Kullanım: python chunk_text.py <transcript_path>", flush=True)
    sys.exit(1)

# Yollar
transcript_path = sys.argv[1]
base_name = os.path.splitext(os.path.basename(transcript_path))[0]
chunks_folder = os.path.join("Chunks")
os.makedirs(chunks_folder, exist_ok=True)

# Debug: Dosya kontrolü
print(f" Kontrol: Transkript dosyası yolu: {transcript_path}", flush=True)

if not os.path.exists(transcript_path):
    print(f" HATA: Transkript dosyası bulunamadı: {transcript_path}", flush=True)
    sys.exit(1)

# Metni oku
with open(transcript_path, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    print(f" HATA: Transkript dosyası boş: {transcript_path}", flush=True)
    sys.exit(1)

# Cümlelere ayır
sentences = sent_tokenize(text)
print(f" {len(sentences)} cümle bulundu.", flush=True)

chunk_size = 500  # karakter sınırı
chunk = ""
chunk_count = 0

# Parçalama işlemi
for sentence in sentences:
    if len(chunk) + len(sentence) <= chunk_size:
        chunk += sentence + " "
    else:
        chunk_count += 1
        chunk_file = os.path.join(chunks_folder, f"{base_name}_chunk_{chunk_count}.txt")
        with open(chunk_file, "w", encoding="utf-8") as cf:
            cf.write(chunk.strip())
        chunk = sentence + " "

# Son kalan chunk
if chunk.strip():
    chunk_count += 1
    chunk_file = os.path.join(chunks_folder, f"{base_name}_chunk_{chunk_count}.txt")
    with open(chunk_file, "w", encoding="utf-8") as cf:
        cf.write(chunk.strip())

# Çıktı
if chunk_count > 0:
    print(f" Chunking tamamlandı: {chunk_count} parça oluşturuldu.", flush=True)
else:
    print(" Hiç parça oluşturulamadı. Metin yetersiz olabilir.", flush=True)
