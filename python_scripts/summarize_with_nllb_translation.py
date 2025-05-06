import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# NLLB için fonksiyon
def nllb_translate(text, src_lang, tgt_lang):
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    tokenizer.src_lang = src_lang
    encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    generated_tokens = model.generate(**encoded, forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_lang), max_length=512)
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# T5 ile İngilizce özetleme
def summarize_english(text):
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base").to(device)

    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
    summary_ids = model.generate(inputs, max_length=128, min_length=40, num_beams=4, length_penalty=1.2, repetition_penalty=2.5, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python summarize_with_nllb_translation.py <chunk_dosya_yolu>")
        sys.exit(1)

    chunk_path = sys.argv[1]
    if not os.path.exists(chunk_path):
        print(f" Dosya bulunamadı: {chunk_path}")
        sys.exit(1)

    with open(chunk_path, "r", encoding="utf-8") as f:
        turkish_text = f.read().strip()

    print(" Türkçeden İngilizceye çeviriliyor...")
    english_text = nllb_translate(turkish_text, "tur_Latn", "eng_Latn")

    print(" İngilizce özetleniyor...")
    english_summary = summarize_english(english_text)

    print(" İngilizceden Türkçeye geri çeviriliyor...")
    turkish_summary = nllb_translate(english_summary, "eng_Latn", "tur_Latn")

    output_path = os.path.join("Summaries", os.path.splitext(os.path.basename(chunk_path))[0] + "_nllb_summary.txt")
    os.makedirs("Summaries", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(turkish_summary)

    print(" Özetleme tamamlandı!")
    print(" Türkçe Özet:\n" + turkish_summary)

if __name__ == "__main__":
    main()
