
import re
import math
import collections
import urllib.request
import random

DATA_SOURCES = {
    1: {  # Спин +1: Философия (Зеленый глюон)
        "urls": [
            "https://githubusercontent.com"
        ],
        "name": "Философия"
    },
    0: {  # Спин 0: Кванты / Физика (Синий глюон)
        "urls": [
            "https://githubusercontent.com"
        ],
        "name": "Кванты и Физика"
    },
    2: {  # Спин +2: Матан / Системы / Логика (Красный глюон)
        "urls": [
            "https://githubusercontent.com"
        ],
        "name": "Матан и Логика"
    },
    -1: { # Спин -1: Когнитивистика / Разум (Желтый глюон)
        "urls": [
            "https://githubusercontent.com"
        ],
        "name": "Когнитивистика"
    }
}

def download_live_science(urls):
    """Скачивает научные тексты в UTF-8."""
    combined_text = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RAMoE_Bot/1.0'}
    
    for url in urls:
        try:
            print(f"   -> Запрос к серверу: {url[:50]}...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_bytes = response.read()
                text = raw_bytes.decode('utf-8', errors='ignore')
                combined_text += " " + text
        except Exception:
            pass 
            
    return combined_text

def clean_and_tokenize(text):
    return re.findall(r'[а-яё]{4,}', text.lower())

def farm_real_network_multiverse(max_total_words=10000):
    print("[ФЕРМА] ЗАПУСК ЖИВОГО СЕТЕВОГО СБОРА НАУЧНЫХ ДАННЫХ RAMoE...")
    
    stop_words = {
        'чтобы', 'было', 'быть', 'хотя', 'если', 'когда', 'будет', 'даже', 'того', 'потому',
        'этого', 'этой', 'этом', 'этими', 'были', 'будут', 'через', 'однако', 'здесь', 'между',
        'также', 'тоже', 'лишь', 'разве', 'прямо', 'вообще', 'только', 'очень', 'была'
    }
    
    global_vocabulary = {}
    
    
    fallback_pool = {
        1: ["абсолют", "бытие", "субстанция", "сущность", "явление", "категория", "диалектика", "онтология", "гносеология", "метафизика", "трансцендентный", "априори", "истина", "созерцание", "феномен", "суждение", "понятие", "критерий"],
        0: ["квант", "излучение", "вакуум", "волна", "частица", "импульс", "энергия", "фотон", "спектр", "сингулярность", "эфир", "гравитация", "плазма", "флуктуация", "потенциал", "глюон", "аттрактор", "энтропия", "симметрия", "распад"],
        2: ["вектор", "матрица", "система", "структура", "алгоритм", "координата", "аксиома", "анализ", "тензор", "дифференциал", "интеграл", "дискретный", "линейный", "градиент", "сегмент", "функция", "топология", "оператор", "уравнение"],
        -1: ["мысль", "разум", "мозг", "память", "внимание", "интеллект", "осознание", "восприятие", "инсайт", "психика", "когнитивный", "нейрон", "синапс", "рефлекс", "субъект", "эго", "ассоциация", "коллапс", "интуиция", "эмоция"]
    }

    for spin, info in DATA_SOURCES.items():
        print(f"\n[СЕТЬ] Загрузка для Спина {spin} ({info['name']})...")
        raw_text = download_live_science(info["urls"])
        
        words = clean_and_tokenize(raw_text)
        
        if words and len(words) > 100:
            print(f"   [ОК] Успешно скачано {len(words)} реальных слов.")
        else:
            print(f"   [РЕЗЕРВ] Подключаю автономный пласт тезауруса...")
            words = []
            
            for _ in range(3000):
                words.append(random.choice(fallback_pool[spin]) + random.choice(["", "ный", "ский", "ование", "ение", "ация"]))
        
        word_counts = collections.Counter(words)
        filtered = {w: c for w, c in word_counts.items() if w not in stop_words}
        
        if not filtered: continue
        max_freq = max(filtered.values())
        min_freq = min(filtered.values())
        
        for word, freq in filtered.items():
            if any(g in word for g in ["янко", "слава", "собрани", "веши", "фотоархив"]): continue
            
            
            if max_freq == min_freq:
                energy = 1.500000
            else:
                norm = (math.log(max_freq + 1) - math.log(freq + 1)) / (math.log(max_freq + 1) - math.log(min_freq + 1) + 1e-12)
                energy = round(0.500000 + norm * 2.500000, 6)
                
            is_anomaly = energy > 2.850000
            
            if word not in global_vocabulary:
                global_vocabulary[word] = {
                    "spin": float(spin), # Спин намертво завязан на библиотеку науки!
                    "e": energy,
                    "is_anomaly": bool(is_anomaly)
                }

        sorted_global = dict(sorted(global_vocabulary.items(), key=lambda x: x[1]['e'], reverse=True)[:max_total_words])
    return sorted_global

def export_to_config(farmed_vocab):
    with open("E:\\RAMoE\\config.py", "w", encoding="utf-8") as f:
        f.write("# UTF-8 HIGH-PRECISION REAL MULTI-GLUON CONFIG FOR RAMoE\nimport torch\n\n")
        f.write('DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")\n\n')
        f.write("VOCABULARY = {\n")
        words_list = list(farmed_vocab.keys())
        for i, word in enumerate(words_list):
            comma = "," if i < len(words_list) - 1 else ""
            f.write(f'    "{word}": {{"spin": {farmed_vocab[word]["spin"]:.1f}, "e": {farmed_vocab[word]["e"]:.6f}, "is_anomaly": {farmed_vocab[word]["is_anomaly"]}}}{comma}\n')
        f.write("}\n\n")
        f.write("WORDS_LIST = list(VOCABULARY.keys())\n")
        f.write("WORD_TO_IDX = {word: i for i, word in enumerate(WORDS_LIST)}\n")
        f.write("IDX_TO_WORD = {i: word for i, word in enumerate(WORDS_LIST)}\n")
        f.write("VOCAB_SIZE = len(WORDS_LIST)\n\n")
        f.write("SPINS_TENSOR = torch.tensor([VOCABULARY[w]['spin'] for w in WORDS_LIST], dtype=torch.float32, device=DEVICE)\n")
        f.write("ENERGIES_TENSOR = torch.tensor([VOCABULARY[w]['e'] for w in WORDS_LIST], dtype=torch.float32, device=DEVICE)\n")
    print(f"\n[ГОТОВО] Сверхточный многоцветный config.py собран!")
    print(f"[МЕТРИКА] В базу успешно упаковано ровно {len(farmed_vocab)} слов с точностью до 6 знаков!")

if __name__ == "__main__":
    vocab = farm_real_network_multiverse(max_total_words=10000)
    if vocab: 
        export_to_config(vocab)
