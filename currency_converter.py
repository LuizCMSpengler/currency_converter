import requests  # Biblioteca para acessar APIs

def obter_taxas(api_url, api_key):
    """Obtém as taxas de câmbio da API."""
    try:
        response = requests.get(f"{api_url}?access_key={api_key}")  # Faz a requisição
        response.raise_for_status()  # Verifica se houve erro na requisição
        return response.json()  # Retorna os dados no formato de dicionário
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def converter(valor, taxa_origem, taxa_destino):
    """Converte um valor entre duas moedas."""
    return valor * (taxa_destino / taxa_origem)

def listar_moedas(taxas):
    """Lista as moedas disponíveis."""
    return list(taxas.keys())

def main():
    # Configurações da API
    API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    API_KEY = "40fc1e1b080e6c909a662951"  # Substitua pela sua chave da API

    # Passo 1: Obter as taxas de câmbio
    dados = obter_taxas(API_URL, API_KEY)
    if not dados:
        print("Não foi possível obter os dados de câmbio.")
        return

    taxas = dados.get("rates")  # Obter o dicionário de taxas
    print("Moedas disponíveis:")
    print(", ".join(listar_moedas(taxas)))  # Exibir todas as moedas

    # Passo 2: Pedir entradas ao usuário
    moeda_origem = input("Digite o código da moeda de origem: ").upper()
    moeda_destino = input("Digite o código da moeda de destino: ").upper()
    try:
        valor = float(input("Digite o valor a ser convertido: "))
    except ValueError:
        print("Você deve digitar um número válido.")
        return

    # Verificar se as moedas são válidas
    if moeda_origem not in taxas or moeda_destino not in taxas:
        print("Uma ou ambas as moedas digitadas são inválidas. Tente novamente.")
        return

    # Passo 3: Fazer a conversão
    taxa_origem = taxas[moeda_origem]
    taxa_destino = taxas[moeda_destino]
    resultado = converter(valor, taxa_origem, taxa_destino)

    # Passo 4: Exibir o resultado
    print(f"{valor} {moeda_origem} equivalem a {resultado:.2f} {moeda_destino}.")

# Início do programa
if __name__ == "__main__":
    main()
