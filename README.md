
# Projeto: Simulação de Monitoramento de Sensores com Envio de Dados para ThingsBoard

## Descrição Geral
Este projeto implementa uma simulação de monitoramento de sensores de temperatura e umidade para um caminhão em entrega. O sistema simula a coleta de dados de sensores, como temperatura e umidade, e envia os dados para uma plataforma ThingsBoard via API. O sistema também controla automaticamente um refrigerador com base na temperatura, garantindo que ele ligue ou desligue conforme os limites estabelecidos. O código é modular e usa multithreading para gerenciar a execução simultânea da simulação e da entrega.

## Estrutura de Arquivos
- `main.py`: Arquivo principal que contém a lógica de simulação e comunicação com o ThingsBoard.
- `.env`: Arquivo de configuração onde estão armazenadas variáveis de ambiente como `THINGSBOARD_HOST` e `ACCESS_TOKEN`.

## Dependências
O projeto utiliza as seguintes bibliotecas:
- `random`: Para gerar números aleatórios (utilizado na simulação de mudanças de temperatura e umidade).
- `time`: Para controlar o tempo entre as simulações.
- `requests`: Para fazer solicitações HTTP ao ThingsBoard.
- `os`: Para acessar variáveis de ambiente armazenadas no arquivo `.env`.
- `dotenv`: Para carregar as variáveis de ambiente do arquivo `.env`.
- `threading`: Para executar a simulação em uma thread separada.
- `numpy`: Para gerar valores aleatórios a partir de uma distribuição gaussiana (utilizado para a geração inicial de temperatura e umidade).

## Configuração
1. **Instalar Dependências**
   As bibliotecas necessárias podem ser instaladas utilizando o comando:
   ```bash
   pip install requests python-dotenv numpy
   ```

2. **Arquivo `.env`**
   Crie um arquivo `.env` com as seguintes variáveis:
   ```bash
   THINGSBOARD_HOST=seu_thingsboard_host
   ACCESS_TOKEN=seu_access_token
   ```

3. **Executar o Programa**
   Para executar o programa, basta rodar o seguinte comando no terminal:
   ```bash
   python main.py
   ```

## Funcionalidades Principais

### 1. Carregar Variáveis do Arquivo `.env`
As variáveis `THINGSBOARD_HOST` e `ACCESS_TOKEN` são carregadas usando a biblioteca `dotenv`, permitindo configurar facilmente o acesso ao servidor ThingsBoard.

### 2. Simulação de Sensores

#### Técnicas em destaque:
1. **Distribuição Gaussiana** para gerar dados realistas.
2. **Ruído Aleatório Controlado** para variações naturais.
3. **Multithreading** para execução em paralelo.
4. **Controle Automático** para ajuste de temperatura com base em condições internas.
5. **Envio Periódico de Dados** em intervalos regulares para monitoramento remoto.

Essas técnicas aproximam o modelo de um sistema de transporte real, tornando a simulação mais robusta e aplicável a cenários práticos.

A função `simular_sensores` simula os dados dos sensores de temperatura e umidade. Ela gera mudanças aleatórias e progressivas a partir de valores iniciais, que são obtidos usando uma distribuição gaussiana na função `gerar_dados_iniciais`. As mudanças máximas são definidas para cada iteração, garantindo uma variação realista dos dados.

### 3. Controle do Refrigerador
A função `controlar_refrigerador` verifica se a temperatura ultrapassa o limite definido (`TEMP_LIMITE`). Caso a temperatura exceda o valor configurado, o refrigerador é ligado; caso contrário, ele permanece desligado.

### 4. Envio de Dados para o ThingsBoard
A função `enviar_dados` envia os dados simulados para o servidor ThingsBoard usando uma solicitação HTTP POST. O payload enviado contém os valores de temperatura e umidade, e a resposta do servidor é verificada para garantir que os dados foram transmitidos corretamente.

### 5. Gestão do Status da Entrega
As funções `iniciar_entrega` e `finalizar_entrega` controlam o status da simulação, permitindo que o caminhão "saia" para a entrega e retorne ao destino. A simulação só ocorre quando a entrega está em andamento.

### 6. Execução da Simulação em Paralelo
O uso da biblioteca `threading` permite que a simulação seja executada em uma thread separada, enquanto o programa principal continua rodando. Isso simula um cenário real, onde a coleta e envio de dados acontecem em segundo plano, enquanto outras ações podem ocorrer em paralelo.

## Detalhamento do Fluxo de Execução

1. **Início da Entrega**:
   A entrega é iniciada com a função `iniciar_entrega()`, e o status da entrega é alterado para `True`.

2. **Execução da Simulação**:
   A função `executar_simulacao` é executada em uma thread separada. Ela gera dados iniciais de temperatura e umidade, e em cada iteração:
   - Simula mudanças nos sensores.
   - Envia os dados simulados ao ThingsBoard.
   - Verifica a necessidade de ligar ou desligar o refrigerador.
   
   Cada iteração ocorre com um intervalo de 60 segundos.

3. **Finalização da Entrega**:
   Após um período de 4 minutos (240 segundos), a entrega é finalizada com a função `finalizar_entrega()`, interrompendo a simulação.

4. **Encerramento**:
   O programa aguarda a conclusão da thread de simulação antes de finalizar.

## Possíveis Melhorias
- **Simulação Mais Detalhada**: Introduzir outros sensores e variáveis, como pressão ou níveis de vibração, para uma simulação mais realista.
- **Interface de Monitoramento**: Adicionar uma interface gráfica ou web para visualizar os dados em tempo real.
- **Alertas Automáticos**: Configurar notificações quando os limites de temperatura ou umidade forem excedidos.
- **Implementação de sensores reais**: Usar sensores físicos de forma a medir mais realisticamente as condições climáticas de entrega

## Referências
- [ThingsBoard API Documentation](https://thingsboard.io/docs/reference/api/)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Python Threading](https://docs.python.org/3/library/threading.html)
