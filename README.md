# 🌌 Espectro de Estrelas

Projeto desenvolvido para a disciplina **Introdução à Astrofísica e Cosmologia**.  
Este projeto implementa um **classificador automático de tipos espectrais estelares**, analisando espectros de alta resolução e comparando-os com modelos teóricos.

## 👨‍👩‍👧‍👦 Grupo
- Júlia Pereira de Souza  
- Hélio José de Queiroz Neto  

---

## 🔭 Sobre o Projeto

O script automatiza a classificação espectral de estrelas por meio da análise de seus espectros. Ele executa as seguintes etapas:

1. 📥 **Download de Espectros** (SDSS ou arquivos FITS locais)  
2. 📈 **Normalização** do espectro para realce de características espectrais  
3. 💾 **Download de Linhas Espectrais** de um banco de dados atômico  
4. 🔍 **Detecção Automática de Linhas de Absorção**  
5. 🧬 **Superposição com Banco de Dados Químico**  
6. 🌠 **Download de Modelos PHOENIX** (tipos espectrais O, B, A, F, G, K, M)  
7. ⭐ **Espectros de Referência** para cada tipo  
8. ⚖️ **Comparação Modelo vs Observação**  
9. 🤖 **Classificação via Random Forest**  

📊 Resultados são apresentados em tabelas no terminal, com um gráfico salvo como `spectrum.png` e um relatório em `relatorio.txt`.

---
## 🛠️ Pré-requisitos

- Python **3.8+**  
- Internet (para download via SDSS)  
- Arquivos FITS (opcional, para uso local)

---

## ⚙️ Instalação

1. Clone o repositório:
- https://github.com/<seu_usuario>/tef-mini-projeto.git
- cd tef-mini-projeto
2. Crie um ambiente virtual:
- python -m venv venv
- source venv/bin/activate        
- venv\Scripts\activate 
3. Instale as dependências:
-pip install -r requirements.txt

---

## 🚀 Uso
### 🔧 Preparação (para arquivos FITS locais)
🔍 FITS Locais: devem estar em data/input/, e o nome informado deve ser sem extensão.
1. Coloque os arquivos em data/input/
- Extensões permitidas: .fits, .fit, .fts, .FITS
2. ▶️ Executar o programa:
python -m src.main ou python src/main.py





