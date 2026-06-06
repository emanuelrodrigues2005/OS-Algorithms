import time

MIN_BLOCK = 0
MAX_BLOCK = 15
REQUEST_SEQUENCE = [3, 9, 2, 14, 7, 10]
INITIAL_HEAD = 5
DIRECTION = "up"

def scan_algorithm(requests, head, min_block, max_block, direction):
    requests = sorted(requests)
    visited = []
    total_seek = 0
    current = head

    print("\n--- SCAN (Elevador) ---")
    print(f"Posição inicial: {current}, direção: {direction}")
    
    if direction == "up":
        up_seq = [r for r in requests if r >= current]
        down_seq = [r for r in requests if r < current][::-1]
        
        for r in up_seq:
            seek = abs(current - r)
            print(f"Movendo de {current} -> {r}, seek parcial: {seek}")
            total_seek += seek
            visited.append(r)
            current = r
            time.sleep(0.5)

        seek = max_block - current
        print(f"Movendo até extremidade {max_block}, seek parcial: {seek}")
        total_seek += seek
        current = max_block
        time.sleep(0.5)

        for r in down_seq:
            seek = abs(current - r)
            print(f"Movendo de {current} -> {r}, seek parcial: {seek}")
            total_seek += seek
            visited.append(r)
            current = r
            time.sleep(0.5)
    else:
        down_seq = [r for r in requests if r <= current][::-1]
        up_seq = [r for r in requests if r > current]

        for r in down_seq:
            seek = abs(current - r)
            print(f"Movendo de {current} -> {r}, seek parcial: {seek}")
            total_seek += seek
            visited.append(r)
            current = r
            time.sleep(0.5)

        seek = current - min_block
        print(f"Movendo até extremidade {min_block}, seek parcial: {seek}")
        total_seek += seek
        current = min_block
        time.sleep(0.5)

        for r in up_seq:
            seek = abs(current - r)
            print(f"Movendo de {current} -> {r}, seek parcial: {seek}")
            total_seek += seek
            visited.append(r)
            current = r
            time.sleep(0.5)

    print(f"Ordem final de blocos visitados: {visited}")
    print(f"Tempo total de seek: {total_seek}\n")
    return visited, total_seek

def cscan_algorithm(requests, head, min_block, max_block):
    requests = sorted(requests)
    visited = []
    total_seek = 0
    current = head

    print("\n--- C-SCAN (Circular) ---")
    print(f"Posição inicial: {current}")
    
    up_seq = [r for r in requests if r >= current]
    down_seq = [r for r in requests if r < current]

    for r in up_seq:
        seek = abs(current - r)
        print(f"Movendo de {current} -> {r}, seek parcial: {seek}")
        total_seek += seek
        visited.append(r)
        current = r
        time.sleep(0.5)

    seek = max_block - current
    print(f"Movendo até extremidade {max_block}, seek parcial: {seek}")
    total_seek += seek
    current = min_block
    time.sleep(0.5)

    seek = max_block - min_block
    print(f"Retorno circular do {max_block} -> {min_block}, seek parcial: {seek}")
    total_seek += seek
    time.sleep(0.5)

    for r in down_seq:
        seek = abs(current - r)
        print(f"Movendo de {current} -> {r}, seek parcial: {seek}")
        total_seek += seek
        visited.append(r)
        current = r
        time.sleep(0.5)

    print(f"Ordem final de blocos visitados: {visited}")
    print(f"Tempo total de seek: {total_seek}\n")
    return visited, total_seek

scan_algorithm(REQUEST_SEQUENCE, INITIAL_HEAD, MIN_BLOCK, MAX_BLOCK, DIRECTION)
cscan_algorithm(REQUEST_SEQUENCE, INITIAL_HEAD, MIN_BLOCK, MAX_BLOCK)