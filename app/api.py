# app/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

try:
    from por_multimodal.resonance_mm import MultimodalResonance
except ImportError:
    MultimodalResonance = None

app = FastAPI(title="PoR Suite API", version="0.1.0")


class SimulateRequest(BaseModel):
    steps: int = 200
    chain_length: int = 64
    seed: Optional[int] = None


class SimulateResponse(BaseModel):
    stability: float
    coherence: float


@app.post("/simulate", response_model=SimulateResponse)
def simulate(req: SimulateRequest):
    sim = ResonanceSimulator(chain_length=req.chain_length, seed=req.seed)
    sim.run_iterations(req.steps)

    stab = stability_score(sim.chain)
    coh = coherence(sim.chain)

    return SimulateResponse(stability=stab, coherence=coh)


class MultimodalRequest(BaseModel):
    image_path: str
    text: str


@app.post("/multimodal")
def multimodal(req: MultimodalRequest):
    if MultimodalResonance is None:
        return {"error": "Multimodal module not available on server."}

    mm = MultimodalResonance()
    result = mm.compare(image_path=req.image_path, text=req.text)
    return result


def run():
    import uvicorn

    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
