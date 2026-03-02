import click
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from passkeeper.core.vault import Vault, Credential
import uuid

console = Console()
VAULT_FILE = Path.home() / ".local-passkeeper" / "vault.json"

@click.group()
def cli():
    """Local Passkeeper - Secure Python Password Manager"""
    pass

@cli.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Master password for the vault')
def init(password: str):
    """Initialize a new secure password vault."""
    if VAULT_FILE.exists():
        console.print("[bold red]Warning:[/bold red] Vault already exists. Initializing will overwrite it!")
        if not click.confirm("Do you want to continue?"):
            return
            
    vault = Vault(password, VAULT_FILE)
    vault.initialize_new()
    console.print(f"[bold green]Success![/bold green] Vault initialized securely at {VAULT_FILE}")

@cli.command()
@click.option('--name', prompt="Service Name", help='Name of the service')
@click.option('--username', prompt="Username/Email", help='Username or email')
@click.option('--password', prompt="Password", hide_input=True, help='The password for the service')
@click.option('--master-password', prompt="Master Password", hide_input=True)
def add(name: str, username: str, password: str, master_password: str):
    """Add a new credential to the vault."""
    try:
        vault = Vault(master_password, VAULT_FILE)
        vault.load()
        
        cipher, nonce = vault.encrypt_password(password)
        cred = Credential(
            id=str(uuid.uuid4()),
            name=name,
            username=username,
            password_cipher=cipher,
            nonce=nonce
        )
        vault.add_credential(cred)
        console.print(f"[bold green]Added:[/bold green] Credential for {name} saved successfully.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cli.command()
@click.option('--master-password', prompt="Master Password", hide_input=True)
def list(master_password: str):
    """List all saved credentials."""
    try:
        vault = Vault(master_password, VAULT_FILE)
        vault.load()
        
        creds = vault.list_credentials()
        if not creds:
            console.print("[yellow]Vault is empty.[/yellow]")
            return
            
        table = Table(title="Secure Vault Credentials")
        table.add_column("Name", style="cyan")
        table.add_column("Username", style="magenta")
        table.add_column("ID", style="dim")
        
        for c in creds:
            table.add_row(c.name, c.username, c.id[:8])
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error[/bold red]: Invalid master password or missing vault. ({e})")

@cli.command()
@click.argument('name')
@click.option('--master-password', prompt="Master Password", hide_input=True)
def get(name: str, master_password: str):
    """Get the password for a specific service."""
    try:
        vault = Vault(master_password, VAULT_FILE)
        vault.load()
        
        creds = vault.list_credentials()
        target = next((c for c in creds if c.name.lower() == name.lower()), None)
        
        if not target:
            console.print(f"[bold red]Warning:[/bold red] No credential found for '{name}'")
            return
            
        plaintext_password = vault.decrypt_password(target.password_cipher, target.nonce)
        console.print(f"\n[bold cyan]Name:[/bold cyan] {target.name}")
        console.print(f"[bold magenta]Username:[/bold magenta] {target.username}")
        console.print(f"[bold green]Password:[/bold green] {plaintext_password}\n")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to decrypt. Incorrect master password. ({e})")

if __name__ == '__main__':
    cli()
