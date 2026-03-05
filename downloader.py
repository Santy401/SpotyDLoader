import os
import sys
import subprocess
import yt_dlp
from rich.console import Console

console = Console()

class SpotyDownloader:
    def __init__(self, download_path):
        self.download_path = download_path

    def download_url(self, url):
        urls_to_download = []
        if "spotify.com" in url:
            console.print("\n[bold green][SPOTIFY] Hackeando matriz de Spotify para descargar via YouTube...[/bold green]")
            import urllib.request
            import re
            import json
            
            embed_url = url.replace("spotify.com/", "spotify.com/embed/").split("?")[0]
            try:
                req = urllib.request.Request(embed_url, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req).read().decode('utf-8')
                json_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html)
                
                if json_data:
                    data = json.loads(json_data.group(1))
                    entity = data['props']['pageProps']['state']['data']['entity']
                    
                    if entity['type'] in ['playlist', 'album']:
                        for t in entity['trackList']:
                            urls_to_download.append(f"ytsearch1:{t['title']} {t['subtitle']}")
                    elif entity['type'] == 'track':
                        urls_to_download.append(f"ytsearch1:{entity['name']} {entity.get('subtitle', '')}")
                    
                    console.print(f"[bold bright_green][OK] ¡Encontradas {len(urls_to_download)} canciones! Descargando en máxima calidad...[/bold bright_green]")
                else:
                    console.print("[bold red][ERROR] No se pudo leer la playlist de Spotify.[/bold red]")
                    return
            except Exception as e:
                console.print(f"\n[bold red][ERROR] Inconveniente al extraer de Spotify: {str(e)}[/bold red]")
                return
        else:
            urls_to_download = [url]

        # Buscamos si FFmpeg está instalado en Windows (usaremos el que descargó SpotDL)
        import shutil
        ffmpeg_path = shutil.which('ffmpeg')
        if not ffmpeg_path and sys.platform == 'win32':
            spotdl_ffmpeg = os.path.expanduser('~/.spotdl/ffmpeg.exe')
            if os.path.exists(spotdl_ffmpeg):
                ffmpeg_path = spotdl_ffmpeg

        # Configuraciones clave para yt-dlp (YouTube y demás)
        ydl_opts = {
            'format': 'bestaudio/best',
            # Guarda los archivos en el formato especificado
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'writethumbnail': True, # Descarga la miniatura / foto
            'postprocessors': [
                {
                    # Usa FFmpeg para extraer y convertir a mp3
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320', # Máxima calidad mp3 posible
                },
                {
                    # Incrusta la foto del álbum/video en el MP3
                    'key': 'EmbedThumbnail',
                },
                # Si tienes FFmpeg instalado añadirá etiquetas/metadata cuando sea posible
                {'key': 'FFmpegMetadata'},
            ],
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,  # Ignora errores en videos inaccesibles (muy útil en playlists)
            'extract_flat': False, # Falso asegura que descargue todo el contenido, no solo info local
        }
        
        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path

        # Una función que usamos como "gancho" para mostrar la barra de progreso minimalista
        def progress_hook(d):
            if d['status'] == 'downloading':
                # Conseguir o intentar filtrar los valores de forma segura
                percent_str = d.get('_percent_str', '0%').strip()
                try:
                    # Limpiando caracteres no deseados en consolas simples
                    import re
                    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                    percent_str = ansi_escape.sub('', percent_str)

                    # Obteniendo el nombre del archivo de forma amigable
                    filename = os.path.basename(d.get('filename', 'Archivo desconocido'))
                    if hasattr(filename, 'decode'):
                        filename = filename.decode('utf-8')

                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')

                    # Imprimimos y sobreescribimos la misma línea en terminal para no ensuciar pantalla
                    sys.stdout.write(f"\r\033[K[bold cyan]Descargando:[/bold cyan] {filename[:40]}... | [green]{percent_str}[/] | {speed} | Faltan: {eta}")
                    sys.stdout.flush()

                except Exception:
                    pass
            elif d['status'] == 'finished':
                # Esto se lanza una vez acaba de bajar el mp4, pero antes de FFmpeg...
                sys.stdout.write(f"\n[green][OK] Descarga al 100%. Extrayendo audio y procesando...[/green]\n")
                sys.stdout.flush()

        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                console.print(f"\n[bold yellow][WAIT] Analizando URL... (Si es una Playlist puede demorar unos segundos)[/bold yellow]")
                # Lanza la descarga pasando la lista reconstruida
                if urls_to_download:
                    ydl.download(urls_to_download)
                
                console.print(f"\n[bold bright_green][DONE] ¡Proceso Finalizado! [DONE][/bold bright_green]")
        except Exception as e:
            console.print(f"\n[bold red][ERROR] Hubo un inconveniente con la descarga: {str(e)}[/bold red]")
