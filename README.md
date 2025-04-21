Espectro de estrelas

Projeto desenvolvido como Trabalho de Fim de Disciplina (TEF) para a disciplina Introdução à Astrofísica e Cosmologia. Este projeto implementa um classificador automático de tipos espectrais estelares, analisando espectros estelares de alta resolução e comparando-os com modelos teóricos.
Grupo:
Júlia Pereira de Souza
Hélio José de Queiroz Neto

Sobre o Projeto
O script tem como objetivo automatizar a classificação de tipos espectrais de estrelas por meio da análise de seus espectros. O projeto abrange as seguintes etapas:

Download de Espectros de Alta Resolução: Obtenção de espectros estelares do Sloan Digital Sky Survey (SDSS) ou de arquivos FITS locais.
Normalização: Pré-processamento do espectro para remover o contínuo e destacar características espectrais.
Download de Informações de Linhas Espectrais: Uso de um banco de dados atômico para identificar linhas de absorção.
Detecção de Linhas no Espectro: Identificação automática de linhas de absorção no espectro normalizado.
Superposição com Base de Dados: Comparação das linhas detectadas com um banco de dados para identificação de elementos químicos.
Download de Modelos de Espectro: Uso de modelos PHOENIX simulados para diferentes tipos espectrais (O, B, A, F, G, K, M).
Download de Espectros de Referência: Obtenção de espectros de estrelas representativas de cada tipo espectral.
Comparação Modelo/Observação: Análise comparativa entre o espectro observado e os modelos teóricos.
Automatização da Classificação Espectral: Uso de um classificador Random Forest para determinar o tipo espectral com base nas características do espectro.

Os resultados são apresentados em tabelas no terminal, com um gráfico do espectro (spectrum.png) e um relatório textual (relatorio.txt) contendo o tipo espectral identificado, a certeza da classificação e as linhas espectrais detectadas.
Estrutura do Repositório
StellarSpectrumClassifier/
├── src/
│   ├── __init__.py           # Arquivo vazio para marcar src como módulo
│   ├── stellar_classifier.py # Funções principais do classificador
│   ├── main.py              # Ponto de entrada do programa
├── config/
│   ├── settings.yaml        # Configurações de modelos estelares e banco de dados atômico
├── data/
│   ├── input/               # Pasta para arquivos FITS locais
├── resultados/               # Pasta para resultados (gráfico e relatório)
│   ├── spectrum.png         # Gráfico do espectro
│   ├── relatorio.txt        # Relatório textual
├── README.md                # Este arquivo
├── requirements.txt         # Dependências do projeto

Pré-requisitos

Python: Versão 3.8 ou superior
Dependências: Listadas em requirements.txt
Conexão com a Internet: Necessária para a opção de download de espectros do SDSS
Arquivos FITS (opcional): Para uso local, devem estar na pasta data/input/

Instalação

Clone o repositório:
git clone https://github.com/<SEU_USUARIO>/StellarSpectrumClassifier.git
cd StellarSpectrumClassifier


Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Instale as dependências:
pip install -r requirements.txt


Uso
Preparação para Arquivos FITS Locais (se usar a opção 2):
Coloque os arquivos FITS na pasta data/input/.
Os arquivos devem ter extensões .fits, .fit, .fts ou .FITS.

Execute o Programa:
No diretório raiz do projeto (StellarSpectrumClassifier/), execute:python -m src.main
Alternativamente, se preferir:python src/main.py


Escolha uma Opção:
Opção 1: Baixa um espectro do SDSS (requer conexão com a internet).
Opção 2: Forneça o nome do arquivo FITS sem extensão (ex.: espectro1 para data/input/espectro1.fits).


Resultados:
Gráfico: Salvo em resultados/spectrum.png.
Relatório: Salvo em resultados/relatorio.txt, contendo o tipo espectral, certeza da classificação e linhas identificadas.

Exemplo de Execução
$ python -m src.main
🔭 [bold]Classificador Automático de Tipos Estelares
[bold]Opções de entrada de dados:[/]
1. Baixar espectro do SDSS (online)
2. Usar arquivo FITS local

Escolha a opção (1 ou 2): 2
Digite o nome do arquivo (sem extensão): espectro1
[blue]Processando espectro...

[RESULTADOS DA CLASSIFICAÇÃO]
Tipo Estelar Identificado: G
Nível de Certeza: 95.2%

[LINHAS IDENTIFICADAS]
Compr. Onda (Å) | Larg. Equiv. | Elemento
6562.81        | 0.45        | H-alfa (Balmer)
5892.90        | 0.32        | Na I (Sódio)

[green]Resultados salvos em:
• Gráfico: resultados/spectrum.png
• Relatório: resultados/relatorio.txt

Dependências
As dependências estão listadas em requirements.txt:
numpy
astropy
matplotlib
scipy
scikit-learn
rich
pyyaml

Instale-as com:
pip install -r requirements.txt

Notas

Arquivos FITS Locais: Devem estar na pasta data/input/. Forneça apenas o nome do arquivo sem a extensão ao usar a opção 2.
Configurações: O arquivo config/settings.yaml define modelos estelares e o banco de dados atômico. Se ausente, valores padrão são usados.
Erros do SDSS: Caso o download do SDSS falhe (opção 1), o programa gera um espectro simulado. Verifique stellar_classifier.log para detalhes.
Sistema Operacional: Testado em Windows, Linux e macOS. Certifique-se de que os caminhos de arquivo são compatíveis com seu sistema.


Desenvolvido para a disciplina Introdução à Astrofísica e Cosmologia, 2025
