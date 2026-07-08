
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import math
import random
import time
import re
from config import VOCABULARY, WORD_TO_IDX, IDX_TO_WORD, VOCAB_SIZE, SPINS_TENSOR, ENERGIES_TENSOR, DEVICE

GLOBAL_E0 = 5.0            
GLOBAL_SPIN = 0            
DYNAMIC_ENERGIES = ENERGIES_TENSOR.clone()

def mini_transformer_decoder(raw_words):
    """Синтаксический декодер: преобразует частоты пружинного эха в строгие тезисы."""
    if not raw_words: return "Поле стабильно. Натяжение пружины компенсировано."
    
    cleaned = []
    for word in raw_words:
        w = word.strip()
        for suffix in ["ование", "ение", "ация", "ский", "ный", "трический"]:
            if w.endswith(suffix) and len(w) > len(suffix) + 3:
                w = w[:-len(suffix)]
        cleaned.append(w)

    connectors = [
        " индуцирует фазовый сдвиг, где ",
        " активирует сопряженное поле, трансформируя ",
        " переходит в локальное устойчивое состояние, в котором ",
        " запускает кинетическую релаксацию пружины, определяя ",
        " локализует упругий потенциал, формируя "
    ]
    
    result = []
    if cleaned:
        result.append(cleaned[0].capitalize() + cleaned[0][1:])
        
    for i in range(1, len(cleaned)):
        word = cleaned[i]
        if i % 2 == 1:
            result.append(random.choice(connectors) + word)
        else:
            result.append(", в то время как " + word)
            
    return "".join(result) + "."

@torch.no_grad()
def process_semantic_spring_wave(user_input):
    global GLOBAL_E0, GLOBAL_SPIN, DYNAMIC_ENERGIES
    
    input_words = [w.lower() for w in re.findall(r'[а-яё]{3,}', user_input)]
    if not input_words:
        print("[Вакуум] Нет соударения. Пружина контекста не натянута.")
        return

    spin_accumulator = 0
    recognized = 0
    for word in input_words:
        if word in VOCABULARY:
            spin_accumulator += VOCABULARY[word]["spin"]
            recognized += 1

    if recognized > 0:
        GLOBAL_SPIN = max(-1, min(2, round(spin_accumulator / recognized)))
    else:
        GLOBAL_SPIN = 0

    current_spin_mask = (SPINS_TENSOR == GLOBAL_SPIN)
    
    if not torch.any(current_spin_mask):
        max_e_vocab = 3.0
        max_p_vocab = 3.5
    else:
        max_e_vocab = torch.max(ENERGIES_TENSOR[current_spin_mask]).item()
        max_p_vocab = torch.max(3.0 - ENERGIES_TENSOR[current_spin_mask]).item()

    # --- ТАКТ 3: РАСЧЕТ ОТНОСИТЕЛЬНЫХ МЕТРИК ЗАПРОСА ПО ЭЙНШТЕЙНУ-ГУКУ ---
    total_input_e = 0.0
    total_input_p = 0.0
    action_markers = ["течет", "формирует", "соединяет", "делит", "зажигает", "горит", "поглощает", "излучает", "угасает", "застывает", "управление", "цикл", "бесит"]

    for word in input_words:
        if word in VOCABULARY:
            w_data = VOCABULARY[word]
            total_input_e += w_data["e"]
            if word in action_markers:
                total_input_p += 4.5  
            elif len(word) % 2 == 0:
                total_input_p += 1.2
            else:
                total_input_p += 0.3
        else:
            total_input_e += 1.0
            total_input_p += 0.4

    word_count = len(input_words)
    relative_e = total_input_e / (word_count * max_e_vocab + 1e-12)
    

    relative_p = total_input_p / (max_p_vocab + 1e-12)

    raw_k = 0.4 + (relative_e - relative_p) * 1.5
    k = max(0.01, min(0.98, raw_k))
    
    if k > 0.45:
        max_gen_words = 3
        mode_desc = f"ЖЕСТКОЕ ЗАТУШЕНИЕ РАСПАДА (k={round(k,4)} | Масса упруго сжала поле)"
    else:
        max_gen_words = 12
        mode_desc = f"РЕЗОНАНСНЫЙ ПОЛЕТ ПОЛУВОЛНЫ (k={round(k,4)} | Импульс пробил натяжение поля)"

    GLOBAL_E0 += total_input_e


    start_time = time.perf_counter()
    torch.cuda.empty_cache()
    initial_vram = torch.cuda.memory_allocated(DEVICE)

    response_words = []
    current_e = GLOBAL_E0
    
    gluon_barrier = (~current_spin_mask).float() * 99999.0

    for _ in range(max_gen_words * 2):
        if len(response_words) >= max_gen_words: break
        if current_e <= 0.1: break

        word_impulse = 3.0 - DYNAMIC_ENERGIES
        
        distance = gluon_barrier + (k * torch.abs(DYNAMIC_ENERGIES - current_e)) + word_impulse
        field_density = 1.0 / (distance + 1e-5)
        
        fluctuation_strength = k * (1.0 / (current_e + 0.1)) * 0.05
        wave_function = field_density + torch.randn(VOCAB_SIZE, device=DEVICE) * fluctuation_strength
        
        _, top_indices = torch.topk(wave_function, k=5)
        next_word_idx = top_indices[random.randint(0, 4)].item()
        next_word = IDX_TO_WORD[next_word_idx]

        if any(g in next_word for g in ["янко", "слава", "собрани", "веши", "фотоархив"]): continue
        if next_word in response_words: continue

        response_words.append(next_word)
        
        DYNAMIC_ENERGIES[next_word_idx] *= 0.01
        DYNAMIC_ENERGIES = torch.lerp(DYNAMIC_ENERGIES, ENERGIES_TENSOR, 0.1)
        current_e -= (k * 0.5)

    GLOBAL_E0 = current_e * (1.0 - k)
    end_time = time.perf_counter()
    vram_used = torch.cuda.memory_allocated(DEVICE) - initial_vram

    beautiful_text = mini_transformer_decoder(response_words)

    print(f"\n [СОСТОЯНИЕ ПРУЖИНЫ]: {mode_desc}")
    print(f"  -> Относительные силы: Средняя масса E = {round(relative_e, 4)} | Прямой Импульс P = {round(relative_p, 4)}")
    print(f"  -> Железо: CUDA = {round((end_time - start_time)*1000, 2)} мс | VRAM истории = {vram_used} байт")
    print(f"\n СЕМАНТИЧЕСКОЕ ЭХО RAMoE:")
    print(f"  {beautiful_text}")
    print("=" * 60)

if __name__ == "__main__":
    print("="*60)
    print(" АДАПТИВНЫЙ АППАРАТ СЕМАНТИЧЕСКОЙ ПРУЖИНЫ RAMoE (ЗАКОН ГУКА)")
    print(" Проверь упругое натяжение полей на базе таксономии RuWordNet")
    print("="*60)
    
    while True:
        try:
            user_input = input("\nВы > ").strip()
            if user_input.lower() == "выход": break
            if not user_input: continue
            process_semantic_spring_wave(user_input)
        except KeyboardInterrupt: break
