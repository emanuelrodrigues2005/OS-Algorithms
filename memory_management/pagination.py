import math
import random
import time

class Processo:
    def __init__(self, pid, nome, tamanho, tam_pagina):
        self.pid = pid
        self.nome = nome
        self.tamanho = tamanho
        self.qtd_paginas = math.ceil(tamanho / tam_pagina)
        self.frag_interna = (self.qtd_paginas * tam_pagina) - tamanho
        self.paginas = [f"Processo {self.pid} - Pg{i}" for i in range(self.qtd_paginas)]

class SimuladorPaginacao:
    def __init__(self, mem_fisica, mem_virtual, tam_pagina, algoritmo):
        self.mem_fisica = mem_fisica
        self.mem_virtual = mem_virtual
        self.tam_pagina = tam_pagina
        self.algoritmo = algoritmo.upper()
        self.num_frames = mem_fisica // tam_pagina
        self.ram = []
        self.page_faults = 0

    def acessar_pagina(self, pagina):
        print(f"> Solicitando acesso à página: {pagina}")

        if pagina in self.ram:
            print(f"  [HIT] A página {pagina} já está na memória física.")

            if self.algoritmo == "LRU":
                self.ram.remove(pagina)
                self.ram.append(pagina)

        else:
            self.page_faults += 1
            print(f"  [FAULT] A página {pagina} não está na memória física. Será carregada do disco.")

            if len(self.ram) >= self.num_frames:
                pagina_vitima = self.ram.pop(0)
                print(f"  [SWAP] RAM cheia! Substituindo a página {pagina_vitima} pela {pagina}.")

            self.ram.append(pagina)

    def exibir_estado_ram(self):
        print(f"\n--- ESTADO DA RAM (Algoritmo: {self.algoritmo}) ---")
        for i in range(self.num_frames):
            if i < len(self.ram):
                print(f" Frame {i}: [ {self.ram[i]} ]")
            else:
                print(f" Frame {i}: [ LIVRE ]")
        print("----------------------------------------\n")

if __name__ == "__main__":
    MEM_FISICA = 16
    MEM_VIRTUAL = 64
    TAM_PAGINA = 4

    simulador = SimuladorPaginacao(MEM_FISICA, MEM_VIRTUAL, TAM_PAGINA, algoritmo="LRU")

    processos = [
        Processo(1, "Chrome", tamanho=10, tam_pagina=TAM_PAGINA),
        Processo(2, "Spotify", tamanho=6, tam_pagina=TAM_PAGINA),
        Processo(3, "VSCode", tamanho=4, tam_pagina=TAM_PAGINA)
    ]

    print("RESUMO DOS PROCESSOS E FRAGMENTAÇÃO")
    for p in processos:
        print(f"Processo {p.nome} (ID {p.pid}): Tamanho {p.tamanho}KB -> Alocado em {p.qtd_paginas} páginas. Fragmentação Interna: {p.frag_interna}KB")

    todas_as_paginas = []
    for p in processos:
        todas_as_paginas.extend(p.paginas)

    print("\nINICIANDO ACESSOS À MEMÓRIA")
    simulador.exibir_estado_ram()

    for _ in range(15):
        pagina_solicitada = random.choice(todas_as_paginas)
        simulador.acessar_pagina(pagina_solicitada)
        simulador.exibir_estado_ram()
        time.sleep(2)

    print(f"FIM DA EXECUÇÃO")
    print(f"Total de Page Faults (Page Misses): {simulador.page_faults}")