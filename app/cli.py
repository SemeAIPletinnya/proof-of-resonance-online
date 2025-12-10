# app/cli.py
import typer
from typing import Optional

from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

try:
    from por_multimodal.resonance_mm import MultimodalResonance
except ImportError:
    MultimodalResonance = None

app = typer.Typer(help="PoR Suite CLI — run resonance simulations and benchmarks.")


@app.command()
def simulate(
    steps: int = typer.Option(200, help="Number of resonance iterations."),
    chain_length: int = typer.Option(64, help="Length of the simulated chain."),
    seed: Optional[int] = typer.Option(None, help="Random seed for reproducibility."),
):
    """Run a basic resonance simulation using por_core.ResonanceSimulator."""
    typer.echo(f"Running PoR simulation: steps={steps}, chain_length={chain_length}, seed={seed}")

    sim = ResonanceSimulator(chain_length=chain_length, seed=seed)
    sim.run_iterations(steps)

    stab = stability_score(sim.chain)
    coh = coherence(sim.chain)

    typer.echo(f"Stability: {stab:.6f}")
    typer.echo(f"Coherence: {coh:.6f}")


@app.command()
def multimodal(
    image_path: str = typer.Argument(..., help="Path to image file."),
    text: str = typer.Argument(..., help="Text description to compare with image."),
):
    """Run a multimodal resonance check (image + text)."""
    if MultimodalResonance is None:
        typer.echo("Multimodal module not available. Check por_multimodal imports.")
        raise typer.Exit(code=1)

    typer.echo("Running multimodal resonance...")
    mm = MultimodalResonance()
    result = mm.compare(image_path=image_path, text=text)

    score = result.get("score")
    typer.echo(f"Resonance score: {score:.4f}" if score is not None else f"Result: {result}")


@app.command()
def benchmark(
    config: str = typer.Option("benchmarks/configs/reasoning_v1.yaml", help="Path to PoR benchmark config."),
):
    """Thin wrapper over benchmark runners."""
    import subprocess
    import sys

    cmd = [
        sys.executable,
        "benchmarks/runners/run_solo.py",
        "--config",
        config,
        "--model",
        "gpt-4.1",
        "--out",
        "solo_results.json",
    ]
    typer.echo(f"Running benchmark:\n{' '.join(cmd)}")
    subprocess.run(cmd, check=False)


def main():
    app()


if __name__ == "__main__":
    main()
