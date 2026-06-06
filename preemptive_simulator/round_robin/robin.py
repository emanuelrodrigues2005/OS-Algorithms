import time

class Processo:
    def __init__(self, id_proc, nome, prioridade, tipo, tempo_cpu_total, tempo_chegada=0):
        self.id = id_proc
        self.nome = nome
        self.prioridade = prioridade
        self.tipo = tipo.upper()
        self.tempo_cpu_total = tempo_cpu_total
        self.tempo_restante = tempo_cpu_total
        self.tempo_chegada = tempo_chegada
        self.tempo_conclusao = 0

    def __repr__(self):
        return f"{self.nome}(Falta:{self.tempo_restante}ms)"

class SimuladorRoundRobin:
    def __init__(self, quantum):
        self.quantum = quantum
        self.tempo_atual = 0
        self.fila_prontos = []
        self.processos_finalizados = []

    def executar(self, processos):
        print(f"\n----- INICIANDO ROUND ROBIN (Quantum: {self.quantum}ms) -----\n")

        processos.sort(key=lambda p: p.tempo_chegada)
        self.fila_prontos = processos

        print(f"[*] Fila Inicial de Prontos: {self.fila_prontos}\n")
        time.sleep(1)

        while self.fila_prontos:
            processo_atual = self.fila_prontos.pop(0)

            if self.tempo_atual < processo_atual.tempo_chegada:
                self.tempo_atual = processo_atual.tempo_chegada

            tempo_uso_cpu = min(processo_atual.tempo_restante, self.quantum)

            if processo_atual.tipo == 'IO' and tempo_uso_cpu > 1:
                tempo_uso_cpu = tempo_uso_cpu // 2
                motivo = "Fez I/O (Preempção voluntária)"
            else:
                motivo = "Fim do Quantum (Preempção)" if processo_atual.tempo_restante - tempo_uso_cpu > 0 else "Concluído"

            print(f"[{self.tempo_atual}ms] CPU -> {processo_atual.nome} [ATIVO] por {tempo_uso_cpu}ms...")
            time.sleep(0.8)

            self.tempo_atual += tempo_uso_cpu
            processo_atual.tempo_restante -= tempo_uso_cpu

            if processo_atual.tempo_restante > 0:
                self.fila_prontos.append(processo_atual)
                print(f"  |_ {motivo}.")
                print(f"  |_ Fila de Prontos Atualizada: {self.fila_prontos}\n")
            else:
                processo_atual.tempo_conclusao = self.tempo_atual
                self.processos_finalizados.append(processo_atual)
                print(f"  |_ {motivo}! {processo_atual.nome} FINALIZADO.")
                print(f"  |_ Fila de Prontos Atualizada: {self.fila_prontos}\n")

        self.exibir_relatorio()

    def exibir_relatorio(self):
        print("----- RELATÓRIO FINAL: ROUND ROBIN -----\n")
        soma_espera, soma_turnaround = 0, 0
        for p in self.processos_finalizados:
            turnaround = p.tempo_conclusao - p.tempo_chegada
            espera = turnaround - p.tempo_cpu_total
            soma_espera += espera
            soma_turnaround += turnaround
            print(f"Processo: {p.nome} | Turnaround: {turnaround}ms | Espera: {espera}ms")

        print("-" * 55)
        print(f"Tempo Médio de Espera: {soma_espera / len(self.processos_finalizados):.2f}ms")
        print(f"Tempo Médio de Turnaround: {soma_turnaround / len(self.processos_finalizados):.2f}ms")
        print("-----------------------------------------------------------\n")

if __name__ == "__main__":
    print("----- MINI SIMULADOR DE ESCALONAMENTO DE PROCESSOS -----\n")

    while True:
        try:
            quantum_input = int(input("Defina o tamanho do Quantum da preempção (em ms): "))
            if quantum_input > 0:
                break
            print("[Erro] O quantum deve ser um número maior que zero.")
        except ValueError:
            print("[Erro] Por favor, insira um número inteiro válido.")

    simulador = SimuladorRoundRobin(quantum=quantum_input)
    lista_processos = []

    while True:
        try:
            qtd_processos = int(input("Quantos processos deseja criar? "))
            if qtd_processos > 0:
                break
            print("[Erro] A quantidade de processos deve ser maior que zero.")
        except ValueError:
            print("[Erro] Por favor, insira um número inteiro válido.")

    for i in range(qtd_processos):
        print(f"\n--- Criação do Processo {i+1} ---")

        while True:
            id_proc = input("ID do Processo (Ex: 1, 2, PID_100): ")
            if any(p.id == id_proc for p in lista_processos):
                print("[Erro] Este ID já está em uso. Por favor, insira um ID único.")
            elif not id_proc.strip():
                print("[Erro] O ID não pode estar vazio.")
            else:
                break

        nome = input("Nome do Processo (Ex: P1, Chrome, Word): ")

        while True:
            try:
                prioridade = int(input("Prioridade do Processo (Inteiro): "))
                break
            except ValueError:
                print("[Erro] Insira um número inteiro para a prioridade.")

        while True:
            tipo = input("Processo I/O Bound ou CPU Bound? (Digite IO ou CPU): ").strip().upper()
            if tipo in ['IO', 'CPU']:
                break
            print("[Erro] Digite exatamente 'IO' ou 'CPU'.")

        while True:
            try:
                tempo_cpu = int(input("Tempo total de CPU necessário (em ms): "))
                if tempo_cpu > 0:
                    break
                print("[Erro] O tempo de CPU deve ser maior que zero.")
            except ValueError:
                print("[Erro] Insira um número inteiro para o tempo de CPU.")

        while True:
            try:
                tempo_chegada = int(input("Tempo de Chegada no sistema (em ms, ex: 0, 2, 5): "))
                if tempo_chegada >= 0:
                    break
                print("[Erro] O tempo de chegada não pode ser negativo.")
            except ValueError:
                print("[Erro] Insira um número inteiro (0 ou maior) para o tempo de chegada.")

        novo_processo = Processo(id_proc, nome, prioridade, tipo, tempo_cpu, tempo_chegada)
        lista_processos.append(novo_processo)
        print(f"[*] {nome} configurado e pronto para a fila!")

    input("\n[!] Configuração concluída. Pressione ENTER para iniciar o escalonamento...")
    simulador.executar(lista_processos)