"""
Trabalho para a disciplina Introdução à Astrofísica e Cosmologia
Grupo: Júlia Pereira de Souza e Hélio José de Queiroz Neto
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

from src.stellar_classifier import (
    show_header, get_user_choice, load_spectrum, normalize_spectrum,
    detect_lines, compare_with_database, train_classifier,
    display_results, save_results
)
from scipy.interpolate import interp1d
import numpy as np
from rich.console import Console

console = Console()

def main():
    show_header()
    
    # 1. Obter espectro
    choice = get_user_choice()
    
    with console.status("[blue]Processando espectro..."):
        try:
            wavelength, flux = load_spectrum(choice)
            norm_flux = normalize_spectrum(wavelength, flux)
            lines = detect_lines(wavelength, norm_flux)
            elements, _ = compare_with_database(lines)
            
            # 2. Classificação
            clf = train_classifier()
            flux_interp = interp1d(wavelength, norm_flux, bounds_error=False)(np.linspace(4000, 7000, 1000))
            star_type = clf.predict([flux_interp])[0]
            certainty = np.max(clf.predict_proba([flux_interp])) * 100
            
            # 3. Resultados
            display_results(star_type, certainty, elements)
            
            # 4. Salvar
            plot_path, report_path = save_results("resultados", star_type, certainty, elements, wavelength, norm_flux)
            console.print(f"\n[green]Resultados salvos em:")
            console.print(f"• Gráfico: [bold]{plot_path}")
            console.print(f"• Relatório: [bold]{report_path}")
            
        except Exception as e:
            console.print(f"[red]Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    main()