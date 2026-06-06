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
        return f"{self.nome}(Prio:{self.prioridade}, Falta:{self.tempo_restante}ms)"

class SimuladorPrioridadePreemptiva:
    def __init__(self):
        self.tempo_atual = 0
        self.fila_prontos = []
        self.processos_finalizados = []
        self.processo_na_cpu = None

    def executar(self, processos_pendentes):
        print("----- INICIANDO ESCALONAMENTO POR PRIORIDADE PREEMPTIVA -----\n")
        print("[!] Regra: Menor número = Maior prioridade.")
        print("[!] Preempção ocorre se um processo melhor chegar durante a execução.\n")
        time.sleep(1.5)

        total_processos = len(processos_pendentes)

        while len(self.processos_finalizados) < total_processos:
            mudanca_de_estado = False

            chegaram_agora = [p for p in processos_pendentes if p.tempo_chegada == self.tempo_atual]
            for p in chegaram_agora:
                self.fila_prontos.append(p)
                processos_pendentes.remove(p)
                print(f"[{self.tempo_atual}ms] [*] CHEGADA: {p.nome} (Prioridade {p.prioridade}) entrou no sistema.")
                mudanca_de_estado = True

            self.fila_prontos.sort(key=lambda p: p.prioridade)

            if self.processo_na_cpu and self.fila_prontos:
                processo_topo_fila = self.fila_prontos[0]
                if processo_topo_fila.prioridade < self.processo_na_cpu.prioridade:
                    print(f"[{self.tempo_atual}ms] [!] PREEMPÇÃO: {processo_topo_fila.nome} (Prio:{processo_topo_fila.prioridade}) interrompeu {self.processo_na_cpu.nome} (Prio:{self.processo_na_cpu.prioridade})!")
                    self.fila_prontos.append(self.processo_na_cpu)
                    self.processo_na_cpu = self.fila_prontos.pop(0)
                    self.fila_prontos.sort(key=lambda p: p.prioridade)
                    mudanca_de_estado = True

            if not self.processo_na_cpu and self.fila_prontos:
                self.processo_na_cpu = self.fila_prontos.pop(0)
                print(f"[{self.tempo_atual}ms] CPU -> {self.processo_na_cpu.nome} [ATIVO] no processador.")
                mudanca_de_estado = True

            if mudanca_de_estado:
                print(f"  |_ Fila de Prontos Atualizada: {self.fila_prontos}\n")
                time.sleep(0.8)

            if self.processo_na_cpu:
                self.processo_na_cpu.tempo_restante -= 1

                if self.processo_na_cpu.tempo_restante == 0:
                    self.processo_na_cpu.tempo_conclusao = self.tempo_atual + 1
                    self.processos_finalizados.append(self.processo_na_cpu)
                    print(f"[{self.tempo_atual + 1}ms] [v] {self.processo_na_cpu.nome} FINALIZADO.")
                    self.processo_na_cpu = None
                    print(f"  |_ Fila de Prontos Atualizada: {self.fila_prontos}\n")
                    time.sleep(0.5)

            self.tempo_atual += 1
            time.sleep(0.05)

        self.exibir_relatorio()

    def exibir_relatorio(self):
        print("----- RELATÓRIO FINAL: PRIORIDADE PREEMPTIVA -----\n")
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
    print("----- SIMULADOR DE ESCALONAMENTO - PRIORIDADE PREEMPTIVA -----\n")

    simulador = SimuladorPrioridadePreemptiva()
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
                prioridade = int(input("Prioridade do Processo (Menor número = Maior Prio): "))
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
        print(f"[*] {nome} configurado e aguardando no tempo de chegada {tempo_chegada}ms!")

    input("\n[!] Configuração concluída. Pressione ENTER para iniciar o escalonamento...")
    simulador.executar(lista_processos)