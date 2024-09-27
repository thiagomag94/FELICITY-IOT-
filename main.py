import random
import time
import requests
import os
from dotenv import load_dotenv
import threading
import numpy as np

# Carregar variáveis do .env
load_dotenv()

THINGSBOARD_HOST = os.getenv('THINGSBOARD_HOST')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Limites para acionamento do refrigerador
TEMP_LIMITE = 25  # Temperatura limite para ligar o refrigerador (em °C)
UMIDADE_LIMITE = 70  # Umidade limite (em %)

# Variáveis de status da entrega
status_entrega = False  # False: caminhão parado, True: caminhão em entrega

# Função para gerar a temperatura e umidade iniciais usando distribuição gaussiana
def gerar_dados_iniciais():
    # Parâmetros para a temperatura e umidade
    media_temp = 28.0  # média de temperatura em °C
    desvio_temp = 2.0   # desvio padrão da temperatura

    media_umidade = 80.0  # média de umidade em %
    desvio_umidade = 5.0   # desvio padrão da umidade

    # Gerar temperatura e umidade iniciais usando distribuição gaussiana
    temperatura_inicial = np.random.normal(media_temp, desvio_temp)
    umidade_inicial = np.random.normal(media_umidade, desvio_umidade)

    return round(temperatura_inicial, 2), round(umidade_inicial, 2)

# Simulação de dados dos sensores de temperatura e umidade
def simular_sensores(temperatura_atual, umidade_atual):
    # Parâmetros de simulação
    mudanca_temp_max = 0.5  # Mudança máxima de temperatura por iteração
    mudanca_umidade_max = 1.0  # Mudança máxima de umidade por iteração

    # Mudanças aleatórias na temperatura e umidade
    delta_temp = np.random.uniform(-mudanca_temp_max, mudanca_temp_max)
    delta_umidade = np.random.uniform(-mudanca_umidade_max, mudanca_umidade_max)

    # Atualizando temperatura e umidade com base nos valores anteriores
    temperatura_atual += delta_temp
    umidade_atual += delta_umidade

    # Garantindo que a umidade fique entre 0% e 100%
    umidade_atual = min(max(umidade_atual, 0), 100)

    # Exibindo os resultados da iteração
    print(f"Temperatura: {round(temperatura_atual, 2)} °C, Umidade: {round(umidade_atual, 2)} %")

    return temperatura_atual, umidade_atual

# Envia os dados para o ThingsBoard via HTTP
def enviar_dados(temperatura, umidade):
    url = f"http://{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"
    payload = {'temperatura': temperatura, 'umidade': umidade}
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f'Dados enviados: Temperatura={temperatura}°C, Umidade={umidade}%')
    else:
        print('Erro ao enviar os dados:', response.text)

# Função que controla o refrigerador
def controlar_refrigerador(temperatura):
    if temperatura > TEMP_LIMITE:
        print('Refrigerador LIGADO')
    else:
        print('Refrigerador DESLIGADO')

# Função para iniciar a simulação quando o caminhão sair para entrega
def iniciar_entrega():
    global status_entrega
    status_entrega = True
    print("Simulação iniciada: Caminhão saiu para a entrega.")

# Função para finalizar a simulação quando o caminhão chegar ao destino
def finalizar_entrega():
    global status_entrega
    status_entrega = False
    print("Simulação finalizada: Caminhão chegou ao destino.")

# Função principal que executa a simulação durante a entrega
def executar_simulacao():
    # Gerar dados iniciais
    temperatura_atual, umidade_atual = gerar_dados_iniciais()

    while status_entrega:
        # Chama a função para simular sensores, passando os valores atuais
        temperatura_atual, umidade_atual = simular_sensores(temperatura_atual, umidade_atual)
        enviar_dados(temperatura_atual, umidade_atual)
        controlar_refrigerador(temperatura_atual)
        time.sleep(60)  # Aguarda 60 segundos entre leituras

if __name__ == '__main__':
    # Simula o início da entrega
    iniciar_entrega()  # Início da entrega
    
    # Iniciar a simulação em uma thread separada
    simulacao_thread = threading.Thread(target=executar_simulacao)
    simulacao_thread.start()
    
    # Simulação continua até que uma condição externa encerre
    time.sleep(240)  # Simula 4 minutos de entrega
    finalizar_entrega()  # Fim da entrega
    
    # Aguarda a finalização da thread
    simulacao_thread.join()
    print("Simulação concluída.")
