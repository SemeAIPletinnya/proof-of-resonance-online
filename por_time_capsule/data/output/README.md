# PoR Time Capsule

**PoR Time Capsule** — це переосмислення ідеї Андрія Карпаті “HN Time Capsule”  
через призму **Proof-of-Resonance (PoR)**.

Ми беремо фронт-сторінки Hacker News 10 років тому,  
пропускаємо їх через сучасну LLM (GPT-5.1 / Grok / інші)  
і додаємо поверх цього **резонансні метрики**:

- внутрішня когерентність відповіді (coherence)
- щільність передбачень (prediction density)
- фазове “зчеплення” (phase lock index)
- загальний PoR-score

## Структура

```text
por_time_capsule/
    pipeline/
        fetch.py       # Stage 1: завантаження HN + статей + коментарів
        por_eval.py    # Stage 2–3: промптинг + LLM аналіз + PoR
        parse.py       # Stage 4: парсинг оцінок, score, agregation
        render.py      # Stage 5: HTML-дашборди
    por_core/
        metrics.py     # PoR метрики поверх LLM-відповідей
        simulator.py   # (stub) симуляція резонансу між днями/моделями
        phase_lock.py  # (stub) phase-lock функції по оцінках/патернах
    data/              # кеш-сирі дані (HN, статті, промпти, відповіді)
    output/            # готові HTML-дашборди
