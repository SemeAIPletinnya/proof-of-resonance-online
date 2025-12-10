# app/dashboard.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

app = FastAPI(title="PoR Dashboard")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="docs/visuals"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "stability": None, "coherence": None},
    )


@app.post("/run", response_class=HTMLResponse)
async def run_simulation(
    request: Request,
    steps: int = Form(200),
    chain_length: int = Form(64),
):
    sim = ResonanceSimulator(chain_length=chain_length)
    sim.run_iterations(steps)

    stab = stability_score(sim.chain)
    coh = coherence(sim.chain)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stability": f"{stab:.6f}",
            "coherence": f"{coh:.6f}",
        },
    )


def run():
    import uvicorn

    uvicorn.run("app.dashboard:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    run()
