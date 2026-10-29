import click
from src.orchestrator import main as run_orchestrator
from src.modules.cvss_calculator import calculate_cvss

@click.group()
def cli():
    """BugBounty-Cal-Report Security Framework CLI."""
    pass

@cli.command()
@click.option("--target", required=True, help="Target asset, URL, or smart contract address")
@click.option("--vector", default="AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N", help="CVSS v3.1 Vector String")
def audit(target: str, vector: str):
    """Execute a full automated vulnerability audit and report generation."""
    click.echo(f"[*] Starting audit pipeline for: {target}")
    run_orchestrator()

@cli.command()
@click.option("--vector", required=True, help="CVSS v3.1 Vector String to evaluate")
def cvss(vector: str):
    """Calculate CVSS 3.1 score and severity rating."""
    score, severity = calculate_cvss(vector)
    click.echo(f"CVSS Score: {score} ({severity})")

if __name__ == "__main__":
    cli()
