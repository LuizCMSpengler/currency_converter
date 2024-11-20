import tkinter as tk
from tkinter import ttk
import requests

# Função para obter as taxas de câmbio
def obter_taxas(api_url, api_key):
    """Obtém as taxas de câmbio da API."""
    try:
        response = requests.get(f"{api_url}?access_key={api_key}")  # Requisição para a API
        response.raise_for_status()  # Verifica se houve erro na requisição
        return response.json()  # Retorna os dados no formato de dicionário
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

# Função para converter valores entre moedas
def converter():
    """Converte o valor inserido pelo usuário com base nas moedas escolhidas."""
    moeda_origem = combo_origem.get()  # Obtém a moeda de origem selecionada
    moeda_destino = combo_destino.get()  # Obtém a moeda de destino selecionada

    try:
        valor = float(entry_valor.get())  # Converte o valor digitado em número
    except ValueError:
        label_resultado.config(text="Por favor, insira um número válido.")  # Mensagem de erro
        return

    if moeda_origem not in taxas or moeda_destino not in taxas:
        label_resultado.config(text="Selecione moedas válidas.")  # Verificação de moedas
        return

    taxa_origem = taxas[moeda_origem]  # Taxa da moeda de origem
    taxa_destino = taxas[moeda_destino]  # Taxa da moeda de destino
    resultado = valor * (taxa_destino / taxa_origem)  # Fórmula de conversão
    label_resultado.config(text=f"{valor} {moeda_origem} = {resultado:.2f} {moeda_destino}")  # Exibição do resultado

# Configurações da API
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
API_KEY = "40fc1e1b080e6c909a662951"  # Substitua pela sua chave de API

# Obter as taxas de câmbio ao iniciar o programa
dados = obter_taxas(API_URL, API_KEY)
if not dados:
    print("Não foi possível obter os dados de câmbio.")
    exit()

# Dicionário de taxas e lista de moedas
taxas = dados.get("rates")
moedas = list(taxas.keys())

# Configuração da interface gráfica
root = tk.Tk()  # Cria a janela principal
root.title("Conversor de Moedas")  # Título da janela

# Criar o layout da interface
frame = ttk.Frame(root, padding="10")
frame.grid()

# Título
label_titulo = ttk.Label(frame, text="Conversor de Moedas", font=("Arial", 16))
label_titulo.grid(column=0, row=0, columnspan=2, pady=10)

# Seleção da moeda de origem
label_origem = ttk.Label(frame, text="Moeda de origem:")
label_origem.grid(column=0, row=1, sticky=tk.W)
combo_origem = ttk.Combobox(frame, values=moedas)
combo_origem.grid(column=1, row=1)
combo_origem.set("USD")  # Valor padrão

# Seleção da moeda de destino
label_destino = ttk.Label(frame, text="Moeda de destino:")
label_destino.grid(column=0, row=2, sticky=tk.W)
combo_destino = ttk.Combobox(frame, values=moedas)
combo_destino.grid(column=1, row=2)
combo_destino.set("BRL")  # Valor padrão

# Entrada do valor a ser convertido
label_valor = ttk.Label(frame, text="Valor:")
label_valor.grid(column=0, row=3, sticky=tk.W)
entry_valor = ttk.Entry(frame)
entry_valor.grid(column=1, row=3)

# Botão para converter
button_converter = ttk.Button(frame, text="Converter", command=converter)
button_converter.grid(column=0, row=4, columnspan=2, pady=10)

# Exibição do resultado
label_resultado = ttk.Label(frame, text="", font=("Arial", 12))
label_resultado.grid(column=0, row=5, columnspan=2)

# Iniciar o loop principal
root.mainloop()
