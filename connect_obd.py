import obd
import time

# --- CONFIGURAÇÕES CRÍTICAS PARA ADAPTADORES CLONE ---
# Essas configurações são frequentemente necessárias para clones baratos do ELM327.
# fast=False desativa otimizações que esses clones podem não suportar corretamente.
# timeout=30 aumenta o tempo que a biblioteca esperará por uma resposta.
# [30, 31, 32]
connection = obd.OBD(portstr='COM5', fast=False, timeout=30)

# Verifica o status da conexão
if connection.is_connected():
    print("Conectado com sucesso ao adaptador OBD2.")
else:
    print("Falha na conexão. Verifique a porta, a alimentação do adaptador e a ignição do veículo.")
    exit()

# --- Define os comandos que você deseja consultar ---
cmd_rpm = obd.commands.RPM
cmd_speed = obd.commands.SPEED

print("Iniciando a leitura de dados... Pressione Ctrl+C para parar.")

try:
    while True:
        # Consulta o RPM
        response_rpm = connection.query(cmd_rpm)
        # Consulta a Velocidade
        response_speed = connection.query(cmd_speed)

        # --- TRATAMENTO CRÍTICO DE RESPOSTAS NULAS ---
        # Um script robusto deve verificar se a resposta é válida antes de usar seu valor.
        # Uma resposta nula significa que os dados não foram recebidos do carro para essa consulta.
        # [28]
        if not response_rpm.is_null():
            print(f"RPM do Motor: {response_rpm.value}")
        else:
            print("RPM: Sem dados")

        if not response_speed.is_null():
            # A biblioteca retorna valores com unidades (kph por padrão para velocidade)
            print(f"Velocidade do Veículo: {response_speed.value}")
            # Você pode facilmente converter unidades
            print(f"Velocidade do Veículo (MPH): {response_speed.value.to('mph')}")
        else:
            print("Velocidade: Sem dados")

        print("-" * 20)
        time.sleep(1) # Espera 1 segundo antes da próxima consulta

except KeyboardInterrupt:
    print("\nParando o registro de dados.")
finally:
    # Sempre feche a conexão quando terminar
    connection.close()
    print("Conexão fechada.")