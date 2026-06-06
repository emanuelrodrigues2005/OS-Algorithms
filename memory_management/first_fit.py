import random
import time

class Processo:
    def __init__(self, pid, nome, tamanho):
        self.pid = pid
        self.nome = nome
        self.tamanho = tamanho

class GerenciadorMemoria:
    def __init__(self, tamanho_total):
        self.tamanho_total = tamanho_total
        self.memoria = [{'pid': None, 'nome': 'Livre', 'tamanho': tamanho_total, 'alocado': False}]

    def exibir_estado(self):
        print("\n" + "="*30)
        print("ESTADO ATUAL DA MEMÓRIA")
        frag_externa = 0
        memoria_usada = 0

        for i, bloco in enumerate(self.memoria):
            if bloco['alocado']:
                print(f"[{i}] Alocado: {bloco['nome']} (ID:{bloco['pid']}) | Tamanho: {bloco['tamanho']} KB")
                memoria_usada += bloco['tamanho']
            else:
                print(f"[{i}] LIVRE | Tamanho: {bloco['tamanho']} KB")
                frag_externa += bloco['tamanho']

        memoria_livre = self.tamanho_total - memoria_usada
        print("-" * 30)
        print(f"Fragmentação Externa: {frag_externa} KB")
        print(f"Memória Usada: {memoria_usada} KB")
        print(f"Memória Livre: {memoria_livre} KB")
        print("="*30 + "\n")

    def first_fit(self, processo):
        for i, bloco in enumerate(self.memoria):
            if not bloco['alocado'] and bloco['tamanho'] >= processo.tamanho:
                espaco_restante = bloco['tamanho'] - processo.tamanho
                self.memoria[i] = {
                    'pid': processo.pid,
                    'nome': processo.nome,
                    'tamanho': processo.tamanho,
                    'alocado': True
                }

                if espaco_restante > 0:
                    self.memoria.insert(i + 1, {'pid': None, 'nome': 'Livre', 'tamanho': espaco_restante, 'alocado': False})
                return True
        return False

    def compactar(self):
        print("\nEspaço contíguo insuficiente. Realizando compactação...")
        blocos_alocados = [b for b in self.memoria if b['alocado']]
        espaco_livre_total = sum(b['tamanho'] for b in self.memoria if not b['alocado'])

        self.memoria = blocos_alocados
        if espaco_livre_total > 0:
            self.memoria.append({'pid': None, 'nome': 'Livre', 'tamanho': espaco_livre_total, 'alocado': False})

    def unir_blocos_livres(self):
        nova_memoria = []
        for bloco in self.memoria:
            if nova_memoria and not nova_memoria[-1]['alocado'] and not bloco['alocado']:
                nova_memoria[-1]['tamanho'] += bloco['tamanho']
            else:
                nova_memoria.append(bloco)
        self.memoria = nova_memoria

    def swapping(self):
        blocos_alocados = [i for i, b in enumerate(self.memoria) if b['alocado']]
        if not blocos_alocados:
            return False

        idx_remover = random.choice(blocos_alocados)
        proc_removido = self.memoria[idx_remover]
        print(f"\nSWAPPING: Retirando processo '{proc_removido['nome']}' (ID: {proc_removido['pid']}) para o disco.")

        self.memoria[idx_remover] = {'pid': None, 'nome': 'Livre', 'tamanho': proc_removido['tamanho'], 'alocado': False}

        self.unir_blocos_livres()
        return True

    def alocar_processo(self, processo):
        print(f"Tentando alocar: {processo.nome} (Tamanho: {processo.tamanho} KB)")

        if self.first_fit(processo):
            print(f"Sucesso! {processo.nome} alocado diretamente.")
            return

        self.compactar()
        if self.first_fit(processo):
            print(f"Sucesso! {processo.nome} alocado após compactação.")
            return

        while not self.first_fit(processo):
            sucesso_swap = self.swapping()
            if not sucesso_swap:
                print("Erro: Memória pequena demais até para o swap deste processo.")
                break
            self.compactar()
        print(f"Sucesso! {processo.nome} alocado após Swapping.")

if __name__ == "__main__":
    tamanho_memoria = 1000
    gerenciador = GerenciadorMemoria(tamanho_memoria)
    gerenciador.exibir_estado()

    processos_para_alocar = [
        Processo(1, "Chrome", 300),
        Processo(2, "VSCode", 250),
        Processo(3, "Spotify", 200),
        Processo(4, "Docker", 400),
        Processo(5, "Terminal", 150)
    ]

    for p in processos_para_alocar:
        gerenciador.alocar_processo(p)
        gerenciador.exibir_estado()
        time.sleep(2)