import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from downloader import SpotyDownloader
from utils import get_download_path

console = Console()

def show_banner():
    # Arte ASCII estilizado para una terminal pro
    banner = """[bold bright_green]
  ____               _          ____  _                     _           
 / ___|  _ __   ___ | |_  _   _|  _ \\| |     ___    __ _  __| | ___  _ __ 
 \\___ \\ | '_ \\ / _ \\| __|| | | | | | | |    / _ \\  / _` |/ _` |/ _ \\| '__|
  ___) || |_) | (_) | |_ | |_| | |_| | |___| (_) || (_| | (_| |  __/| |   
 |____/ | .__/ \\___/ \\__| \\__, |____/|_____|\\___/  \\__,_|\\__,_|\\___||_|   
        |_|               |___/                                           
[/bold bright_green]
[white]Descarga Playlists de Spotify (vía YT), YouTube, y más. Compatible Win/Linux/Termux.[/white]
[bold cyan]*** Created by : SantyDeveloper :D ***[/bold cyan]
    """
    console.print(Panel(banner, border_style="bright_green", expand=False))

def main():
    # Detectamos la ruta de guardado (dependiendo si es Windows/Linux/Android)
    show_banner()
    save_path = get_download_path()
    
    console.print(f"[cyan][DIR] La música descargada se guardará aquí: \n[bold white]{save_path}[/bold white][/cyan]\n")

    try:
        # Bucle principal de la consola
        while True:
            # Pedimos la url al usuario
            url = Prompt.ask("[bold bright_green][?] Pega la URL del artista / playlist / canción (o escribe 'salir')[/bold bright_green]")
            
            # Condición de salida limpia
            if url.lower() in ['salir', 'exit', 'quit', 'q']:
                console.print("\n[yellow]¡Hasta pronto, disfruta la música![/yellow]\n")
                break
                
            if not url.strip():
                console.print("[red][X] La URL está vacía. Intente denuevo.[/red]\n")
                continue

            # Instanciamos el descargador y cruzamos los dedos
            downloader = SpotyDownloader(save_path)
            downloader.download_url(url.strip())
            
            # Divisor bonito
            console.print("\n[dim]----------------------------------------[/dim]\n")
            
    except KeyboardInterrupt:
        # Por si el usuario presiona CTRL + C
        console.print("\n\n[yellow]Ejecución cancelada por el usuario. ¡Adiós![/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    main()
