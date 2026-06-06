import math

from security.security_breaker import Security

MEMORY_SIZE = 256
BLOCK_SIZE = 16
TOTAL_BLOCKS = MEMORY_SIZE // BLOCK_SIZE
NUM_DISKS_RAID0 = 2 

disk = [False] * TOTAL_BLOCKS
disks = [[False] * TOTAL_BLOCKS for _ in range(NUM_DISKS_RAID0)]
entries = []

class Entry:
    def __init__(self, name, is_dir, size, start, length, parent):
        self.name = name
        self.is_dir = is_dir
        self.size = size
        self.start = start
        self.length = length
        self.parent = parent

def find_entry(name, parent=None):
    if parent is None:
        return next((e for e in entries if e.name == name), None)
    return next((e for e in entries if e.name == name and e.parent == parent), None)

def list_dir(dir_name):
    target = find_entry(dir_name, "root") if dir_name != "root" else find_entry("root")
    if not target or not target.is_dir:
        print("Erro: Diretorio nao encontrado.")
        return
    if target.name != "root" and target.parent != "root":
        print("Erro: Hierarquia invalida.")
        return

    if hasattr(target, "hashed_password"):
        input_pwd = input("Senha necessária para acessar este diretório: ")
        if Security.hash_password_sha256(input_pwd) != target.hashed_password:
            print("Senha incorreta! Acesso negado.")
            return

    children = [e for e in entries if e.parent == target.name]
    print(f"\n--- Lista de {target.name} ---")
    if not children:
        print("(vazio)")
    else:
        for e in children:
            if e.is_dir:
                print(f"[DIR] {e.name}")
            else:
                end_block = e.start + e.length - 1
                senha_info = " (protegido)" if hasattr(e, "hashed_password") else ""
                print(f"[ARQ]{senha_info} {e.name} | {e.size} KB | blocos {e.start}-{end_block}")
    print("-------------------------\n")

def mkdir(name, password=None):
    if find_entry(name, "root"):
        print("Erro: Nome ja existe no diretorio root.")
        return
    
    hashed_pwd = None
    if password:
        hashed_pwd = Security.hash_password_sha256(password)
    
    entry = Entry(name, True, 0, -1, 0, "root")
    if hashed_pwd:
        entry.hashed_password = hashed_pwd 
    entries.append(entry)
    
    print(f"Diretorio '{name}' criado em root.")

def mkfile(parent_name, name, size_str, password=None):
    if parent_name == "root":
        print("Erro: Arquivos devem ficar dentro de um diretorio (apenas dois niveis).")
        return
    parent = find_entry(parent_name, "root")
    if not parent or not parent.is_dir:
        print("Erro: Diretorio pai nao encontrado.")
        return
    if find_entry(name, parent_name):
        print("Erro: Nome ja existe neste diretorio.")
        return

    try:
        size = int(size_str)
    except ValueError:
        print("Erro: Tamanho invalido.")
        return
    if size <= 0:
        print("Erro: Tamanho deve ser maior que zero.")
        return

    blocks_needed = math.ceil(size / BLOCK_SIZE)

    start_block = -1
    free_count = 0

    for i in range(TOTAL_BLOCKS):
        if not disk[i]:
            if free_count == 0: start_block = i
            free_count += 1
            if free_count == blocks_needed: break
        else:
            free_count = 0

    if free_count < blocks_needed:
        total_free = disk.count(False)
        print(f"Erro: Espaço contíguo insuficiente.")
        if total_free >= blocks_needed:
            print(f"-> FRAGMENTAÇÃO EXTERNA DETECTADA! Temos {total_free} blocos livres no total, mas eles não estão juntos.")
        return

    for i in range(start_block, start_block + blocks_needed):
        disk[i] = True

    entry = Entry(name, False, size, start_block, blocks_needed, parent_name)

    if password:
        entry.hashed_password = Security.hash_password_sha256(password)

    entries.append(entry)
    print(f"Arquivo '{name}' salvo nos blocos {start_block} até {start_block + blocks_needed - 1}.")
    print(f"-> Fragmentação Interna: {(blocks_needed * BLOCK_SIZE) - size} KB.")

def rm(name, parent_name=None):
    if name == "root":
        print("Erro: Nao e permitido remover root.")
        return
    entry = find_entry(name, parent_name) if parent_name else find_entry(name)
    if not entry:
        print("Erro: Entrada nao encontrada.")
        return

    if entry.is_dir:
        if any(e.parent == entry.name for e in entries):
            print("Erro: Diretorio nao esta vazio.")
            return
        entries.remove(entry)
        print(f"Diretorio '{name}' excluido.")
        return

    for i in range(entry.start, entry.start + entry.length):
        disk[i] = False
    entries.remove(entry)
    print(f"Arquivo '{name}' excluido.")
    
def mkfile_raid0(parent_name, name, size_str):
    """
    Cria arquivo usando RAID 0 (striping).
    parent_name: nome do diretório pai
    name: nome do arquivo
    size_str: tamanho em KB (string)
    """
    parent = find_entry(parent_name, "root")
    if not parent:
        print("Erro: Diretorio pai não encontrado.")
        return

    try:
        size = int(size_str)
    except ValueError:
        print("Erro: Tamanho inválido.")
        return

    blocks_needed = math.ceil(size / BLOCK_SIZE)
    disk_index = 0
    allocated = []

    for _ in range(blocks_needed):
        # encontra próximo bloco livre no disco atual
        start_block = 0
        found = False
        while start_block < TOTAL_BLOCKS:
            if not disks[disk_index][start_block]:
                disks[disk_index][start_block] = True
                allocated.append((disk_index, start_block))
                found = True
                break
            start_block += 1
        if not found:
            print(f"Erro: Espaço insuficiente no disco {disk_index}")
            return
        disk_index = (disk_index + 1) % NUM_DISKS_RAID0

    entries.append(Entry(name, False, size, allocated[0][1], blocks_needed, parent_name))
    print(f"Arquivo '{name}' alocado em RAID 0:")
    for d, b in allocated:
        print(f"  Disco {d}: bloco {b}")

def print_map_raid0():
    print("\n--- Mapa de Discos (RAID 0) ---")
    for d_index, d in enumerate(disks):
        print(f"Disco {d_index}:")
        for i, b in enumerate(d):
            status = "[Ocupado]" if b else "[Livre]"
            print(f"  Bloco {i:02d}: {status}")
    print("-------------------------------\n")

def main():
    entries.append(Entry("root", True, 0, -1, 0, ""))
    current_dir = "root"

    def get_pwd():
        return "/root" if current_dir == "root" else f"/root/{current_dir}"

    print("=== Simulador Contíguo (Python) ===")
    while True:
        cmd = input(f"\nroot@simulador:{get_pwd()}$ ").strip().split()
        if not cmd:
            continue

        if cmd[0] == "mkdir" and len(cmd) == 2:
            pwd = input("Digite uma senha para proteger este diretório (ou pressione Enter para nenhuma): ")
            pwd = pwd if pwd else None
            mkdir(cmd[1], pwd)

        elif cmd[0] == "mkfile" and len(cmd) in (3, 4):
            dir_name = current_dir if len(cmd) == 3 else cmd[1]
            file_name = cmd[1] if len(cmd) == 3 else cmd[2]
            file_size = cmd[2] if len(cmd) == 3 else cmd[3]
            pwd = input("Digite uma senha para proteger este arquivo (ou pressione Enter para nenhuma): ")
            pwd = pwd if pwd else None
            mkfile_raid0(dir_name, file_name, file_size, pwd)

        elif cmd[0] == "mkfile" and len(cmd) == 3:
            if current_dir == "root":
                print("Erro: Arquivos devem ficar dentro de um diretorio (apenas dois niveis).")
            else:
                pwd = input("Digite uma senha para proteger este arquivo (ou pressione Enter para nenhuma): ")
                pwd = pwd if pwd else None
                mkfile(current_dir, cmd[1], cmd[2], pwd)

        elif cmd[0] == "rm" and len(cmd) in (2, 3):
            parent_arg = cmd[2] if len(cmd) == 3 else (None if current_dir == "root" else current_dir)
            rm(cmd[1], parent_arg)

        elif cmd[0] == "ls" and len(cmd) in (1, 2):
            list_dir(cmd[1] if len(cmd) == 2 else current_dir)

        elif cmd[0] == "map":
            print_map_raid0()

        elif cmd[0] == "cd" and len(cmd) == 2:
            target = cmd[1]
            if target in ("/", "root") or target == "..":
                current_dir = "root"
            else:
                entry = find_entry(target, "root")
                if entry and entry.is_dir:
                    if hasattr(entry, "hashed_password"):
                        input_pwd = input("Senha necessária para acessar este diretório: ")
                        if Security.hash_password_sha256(input_pwd) != entry.hashed_password:
                            print("Senha incorreta! Acesso negado.")
                            continue
                    current_dir = entry.name
                else:
                    print("Erro: Diretorio nao encontrado.")

        # Mostrar caminho atual
        elif cmd[0] == "pwd" and len(cmd) == 1:
            print(get_pwd())

        # Sair
        elif cmd[0] == "exit":
            break

        else:
            print("Comando invalido. Use: mkdir <dir> | mkfile <dir> <nome> <tamanho> | mkfile <nome> <tamanho> | rm <nome> [dir] | ls [dir] | cd <dir|..|/> | map | pwd | exit")
            
if __name__ == "__main__":
    main()