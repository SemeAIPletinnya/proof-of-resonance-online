"""
PoR Time Capsule
================

PoR Time Capsule is a re-imagining of Andrej Karpathy’s HN Time Capsule,
viewed through the computational framework of Proof-of-Resonance (PoR).

The system processes Hacker News front pages from 10 years ago using a
modern LLM (GPT-5.1, Grok, or others) and applies additional PoR metrics
to measure the resonant stability of the model’s hindsight analysis.

Core evaluation metrics include:

    - Internal coherence of the generated analysis
    - Prediction density (how many forward-looking claims exist)
    - Phase-locking index between user discussions and real outcomes
    - Overall PoR Score (resonant stability under hindsight)

By layering PoR analytics on top of LLM retrospective evaluation,
the Time Capsule becomes a measurable computational experiment,
rather than a purely qualitative exercise.
"""
por_time_capsule/
    pipeline/
        fetch.py       # Stage 1: fetch HN frontpage, articles, comments
        por_eval.py    # Stage 2–3: prompt generation + LLM analysis + PoR scoring
        parse.py       # Stage 4: extract grades, scores, aggregate user statistics
        render.py      # Stage 5: render interactive HTML dashboards
    por_core/
        metrics.py     # PoR metrics computed on top of LLM responses
        simulator.py   # (stub) resonance simulation across days or models
        phase_lock.py  # (stub) phase-locking functions for grade/score patterns
    data/              # cached raw data (HN JSON, article text, prompts, responses)
    output/            # final rendered dashboards for each analyzed date
