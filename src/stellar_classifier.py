import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
from scipy.interpolate import interp1d
from sklearn.ensemble import RandomForestClassifier
from rich.console import Console
from rich.table import Table
from rich.progress import track
import os
import warnings
import logging
from pathlib import Path
import yaml
from typing import Dict, List, Tuple, Optional
from astropy.utils.data import download_file
import random

# Configurações iniciais
warnings.filterwarnings('ignore')
console = Console()

def setup_logging():
    """Configura sistema de logging detalhado"""
    logging.basicConfig(
        filename='stellar_classifier.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger('').addHandler(console_handler)

def load_config() -> Dict:
    """Carrega configurações do arquivo YAML"""
    try:
        with open('config/settings.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.warning("Arquivo de configuração não encontrado. Usando valores padrão.")
        return {
            'stellar_models': {
                'O': (35000, 4.5, 0.0),
                'B': (20000, 4.0, 0.0),
                'A': (8500, 4.0, 0.0),
                'F': (6500, 4.5, 0.0),
                'G': (5800, 4.5, 0.0),
                'K': (4000, 4.5, 0.0),
                'M': (3000, 4.5, 0.0)
            },
            'atomic_database': {
                6562.8: "H-alfa (Balmer)",
                4861.3: "H-beta (Balmer)",
                4340.5: "H-gama (Balmer)",
                5892.9: "Na I (Sódio)",
                3968.5: "Ca II (Cálcio)",
                3933.7: "Ca II (Cálcio)",
                5172.7: "Mg I (Magnésio)",
                5270.3: "Fe I (Ferro)",
                8542.1: "Ca II (Infravermelho)"
            }
        }

# Configurações globais
setup_logging()
config = load_config()
MODELOS_PHOENIX = config['stellar_models']
MODELS_CACHE = {}

def show_header():
    """Exibe cabeçalho estilizado"""
    console.rule("[bold cyan]ANÁLISE ESPECTRAL ESTELAR", style="bold blue")
    console.print("🔭 [bold]Classificador Automático de Tipos Estelares\n", justify="center")

def get_local_filename() -> str:
    """Obtém o nome do arquivo sem extensão e valida a existência"""
    while True:
        base_name = console.input("\nDigite o nome do arquivo (sem extensão): ").strip()
        
        if not base_name:
            console.print("[red]Erro: Nome não pode ser vazio!")
            continue
            
        # Tenta encontrar o arquivo com extensões comuns
        extensions = ['.fits', '.fit', '.fts', '.FITS']
        for ext in extensions:
            full_path = f"data/input/{base_name}{ext}"
            if os.path.exists(full_path):
                return full_path
        
        console.print(f"[red]Erro: Arquivo '{base_name}' não encontrado na pasta 'data/input/'")
        console.print("[yellow]Extensões tentadas: .fits, .fit, .fts, .FITS")
        console.print("Por favor, verifique o nome e tente novamente.")

def get_user_choice() -> Dict:
    """Obtém a escolha do usuário para a fonte de dados"""
    while True:
        console.print("\n[bold]Opções de entrada de dados:[/]")
        console.print("1. Baixar espectro do SDSS (online)")
        console.print("2. Usar arquivo FITS local")
        
        choice = console.input("\nEscolha a opção (1 ou 2): ").strip()
        
        if choice == "1":
            return {'source': 'sdss'}
        elif choice == "2":
            filename = get_local_filename()
            return {'source': 'local', 'filename': filename}
        else:
            console.print("[red]Opção inválida! Por favor, escolha 1 ou 2.")

def download_sdss_spectrum() -> Tuple[np.ndarray, np.ndarray]:
    """Baixa um espectro aleatório do SDSS"""
    samples = [
        {'plate': 1323, 'fiber': 275, 'mjd': 52797},  # Tipo G
        {'plate': 1616, 'fiber': 14, 'mjd': 53149},   # Tipo A
        {'plate': 266, 'fiber': 516, 'mjd': 51630}    # Tipo M
    ]
    sample = random.choice(samples)
    
    url = (f"https://dr16.sdss.org/optical/spectrum/view/data/format=fits/spec=lite?"
           f"plate={sample['plate']}&fiber={sample['fiber']}&mjd={sample['mjd']}")
    
    try:
        file_path = download_file(url, cache=True)
        with fits.open(file_path) as hdul:
            flux = hdul[1].data['flux']
            wavelength = 10**hdul[1].data['loglam']
        return wavelength, flux
    except Exception as e:
        logging.error(f"Erro ao baixar espectro: {str(e)}")
        raise

def load_spectrum(choice: Dict) -> Tuple[np.ndarray, np.ndarray]:
    """Carrega o espectro conforme a escolha do usuário"""
    try:
        if choice['source'] == 'sdss':
            return download_sdss_spectrum()
        else:
            with fits.open(choice['filename']) as hdul:
                if len(hdul) > 1 and 'FLUX' in hdul[1].columns.names:
                    flux = hdul[1].data['FLUX']
                    wavelength = 10**hdul[1].data['LOGLAM']
                else:
                    flux = hdul[0].data
                    wavelength = np.linspace(3000, 10000, len(flux))
            return wavelength, flux
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}")
        console.print("[yellow]Gerando espectro simulado...")
        return simulate_model(5800)  # Default tipo G

def simulate_model(teff: float) -> Tuple[np.ndarray, np.ndarray]:
    """Gera modelo sintético baseado na temperatura"""
    wavelength = np.linspace(3000, 10000, 5000)
    flux = np.ones_like(wavelength)
    
    if teff > 30000:  # Tipo O
        flux -= 0.2 * np.exp(-(wavelength - 4540)**2 / 50)
    elif teff > 10000:  # Tipo B
        flux -= 0.3 * np.exp(-(wavelength - 4471)**2 / 50)
    elif teff > 7500:  # Tipo A
        flux -= 0.4 * np.exp(-(wavelength - 6563)**2 / 50)
    elif teff > 6000:  # Tipo F
        flux -= 0.5 * np.exp(-(wavelength - 4861)**2 / 50)
    elif teff > 5000:  # Tipo G
        flux -= 0.6 * np.exp(-(wavelength - 5893)**2 / 50)
    elif teff > 3500:  # Tipo K
        flux -= 0.7 * np.exp(-(wavelength - 3968)**2 / 50)
    else:  # Tipo M
        flux -= 0.8 * np.exp(-(wavelength - 6563)**2 / 50)
    
    return wavelength, flux

def normalize_spectrum(wavelength: np.ndarray, flux: np.ndarray) -> np.ndarray:
    """Normaliza o espectro"""
    continuum = np.polyval(np.polyfit(wavelength, flux, deg=3), wavelength)
    normalized = flux / continuum
    return savgol_filter(normalized, window_length=21, polyorder=3)

def detect_lines(wavelength: np.ndarray, flux: np.ndarray) -> List[Tuple[float, float]]:
    """Detecta linhas de absorção"""
    peaks, properties = find_peaks(-flux, height=-0.95, prominence=0.05, width=2)
    return [(wavelength[p], np.trapz(1-flux[p-10:p+10], wavelength[p-10:p+10])) for p in peaks]

def load_phoenix_model(teff: float, log_g: float = 4.5, metal: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
    """Carrega modelos PHOENIX (simulados)"""
    wavelength = np.linspace(3000, 10000, 5000)
    flux = np.ones_like(wavelength)
    
    if teff > 30000:  # Tipo O
        flux -= 0.2 * np.exp(-(wavelength - 4540)**2 / 50)
    elif teff > 10000:  # Tipo B
        flux -= 0.3 * np.exp(-(wavelength - 4471)**2 / 50)
    elif teff > 7500:  # Tipo A
        flux -= 0.4 * np.exp(-(wavelength - 6563)**2 / 50)
    elif teff > 6000:  # Tipo F
        flux -= 0.5 * np.exp(-(wavelength - 4861)**2 / 50)
    elif teff > 5000:  # Tipo G
        flux -= 0.6 * np.exp(-(wavelength - 5893)**2 / 50)
    elif teff > 3500:  # Tipo K
        flux -= 0.7 * np.exp(-(wavelength - 3968)**2 / 50)
    else:  # Tipo M
        flux -= 0.8 * np.exp(-(wavelength - 6563)**2 / 50)
    
    return wavelength, flux

def train_classifier() -> RandomForestClassifier:
    """Treina classificador com modelos PHOENIX"""
    X, y = [], []
    for star_type, params in MODELOS_PHOENIX.items():
        wl, flux = load_phoenix_model(*params)
        flux_interp = interp1d(wl, flux, bounds_error=False)(np.linspace(4000, 7000, 1000))
        X.append(flux_interp)
        y.append(star_type)
    
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)
    return clf

def compare_with_database(lines: List[Tuple[float, float]]) -> Tuple[List[Tuple[float, float, str]], List[float]]:
    """Compara linhas com banco de dados atômico"""
    detected = []
    unknown = []
    
    for wl, ew in lines:
        matched = False
        for known_wl, element in config['atomic_database'].items():
            if abs(wl - known_wl) <= 1.5:
                detected.append((wl, ew, element))
                matched = True
                break
        if not matched:
            unknown.append(wl)
    
    return detected, unknown

def display_results(star_type: str, certainty: float, elements: List[Tuple[float, float, str]]):
    """Exibe resultados formatados"""
    # Tabela de classificação
    class_table = Table(show_header=False)
    class_table.title = "[bold]RESULTADOS DA CLASSIFICAÇÃO"
    class_table.add_row("Tipo Estelar Identificado:", f"[bold green]{star_type}")
    class_table.add_row("Nível de Certeza:", f"[bold cyan]{certainty:.1f}%")
    console.print("\n")
    console.print(class_table)
    
    # Tabela de elementos
    if elements:
        elem_table = Table(show_header=True, header_style="bold blue")
        elem_table.title = "[bold]LINHAS IDENTIFICADAS"
        elem_table.add_column("Compr. Onda (Å)", justify="right")
        elem_table.add_column("Larg. Equiv.", justify="right")
        elem_table.add_column("Elemento")
        
        for wl, ew, elem in elements:
            elem_table.add_row(f"{wl:.2f}", f"{ew:.2f}", elem)
        
        console.print("\n")
        console.print(elem_table)

def save_results(output_dir: str, star_type: str, certainty: float, elements: List[Tuple[float, float, str]], wavelength: np.ndarray, flux: np.ndarray):
    """Salva resultados em arquivo"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Salvar gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(wavelength, flux)
    plt.xlabel("Comprimento de Onda (Å)")
    plt.ylabel("Fluxo Normalizado")
    plt.title(f"Espectro - Tipo {star_type}")
    plot_path = Path(output_dir) / "spectrum.png"
    plt.savefig(plot_path, dpi=120)
    plt.close()
    
    # Salvar relatório
    report_path = Path(output_dir) / "relatorio.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Tipo Estelar: {star_type}\n")
        f.write(f"Certeza: {certainty:.1f}%\n\n")
        f.write("Linhas identificadas:\n")
        for wl, ew, elem in elements:
            f.write(f"{elem} @ {wl:.2f}Å (EW: {ew:.2f})\n")
    
    return plot_path, report_path