import os
import platform

def get_download_path():
    """Detecta la plataforma y retorna la ruta ideal de guardado."""
    system = platform.system()
    
    # Comprobar si estamos en Termux (Android) usando variables de entorno
    if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ:
        # Ruta en el almacenamiento interno compartido en Android (Carpeta Music)
        base_path = os.path.expanduser("~/storage/shared/Music/SpotyDLoader")
    elif system == "Windows":
        # Carpeta Music de Windows
        base_path = os.path.join(os.path.expanduser("~"), "Music", "SpotyDLoader")
    elif system == "Darwin": 
        # Mac
        base_path = os.path.join(os.path.expanduser("~"), "Music", "SpotyDLoader")
    else: 
        # Linux general
        base_path = os.path.join(os.path.expanduser("~"), "Music", "SpotyDLoader")
        
    # Crear el directorio si no existe
    os.makedirs(base_path, exist_ok=True)
    return base_path
