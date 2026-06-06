package main

import (
	"fmt"
	"sync"
	"time"
)

type Bomba struct {
	ID      int
	Ocupada bool
	Mutex   sync.Mutex
}

func main() {
	fmt.Println("-------------------------------------------------------")
	fmt.Println("SIMULAÇÃO DE CONCORRÊNCIA E EXCLUSÃO MÚTUA")
	fmt.Println("Cenário: 5 Threads (Carros) e 2 Recursos (Bombas)")
	fmt.Println("-------------------------------------------------------")

	bombas := []*Bomba{{ID: 1}, {ID: 2}}
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go tentarAbastecer(i, bombas, &wg)
		time.Sleep(500 * time.Millisecond)
	}

	wg.Wait()

	fmt.Println("\n-------------------------------------------------------")
	fmt.Println("SIMULAÇÃO CONCLUÍDA: Todos os processos finalizados.")
	fmt.Println("-------------------------------------------------------")
}

func tentarAbastecer(idCarro int, bombas []*Bomba, wg *sync.WaitGroup) {
	defer wg.Done()

	fmt.Printf("[Carro %d] Status: Aguardando bomba disponível...\n", idCarro)
	var bombaUsada *Bomba

	for {
		for _, bomba := range bombas {
			bomba.Mutex.Lock()

			if !bomba.Ocupada {
				bomba.Ocupada = true
				bombaUsada = bomba
				bomba.Mutex.Unlock()
				break
			}

			bomba.Mutex.Unlock()
		}

		if bombaUsada != nil {
			break
		}

		time.Sleep(100 * time.Millisecond)
	}

	fmt.Printf("[Carro %d] Status: Bomba %d adquirida. Iniciando preparação...\n", idCarro, bombaUsada.ID)
	time.Sleep(500 * time.Millisecond)

	fmt.Printf("[Carro %d] Status: Consumindo bomba %d (Duração: 3 segundos)...\n", idCarro, bombaUsada.ID)
	time.Sleep(3 * time.Second)

	fmt.Printf("[Carro %d] Status: Processamento concluído. Liberando bomba %d.\n", idCarro, bombaUsada.ID)
	
	bombaUsada.Mutex.Lock()
	bombaUsada.Ocupada = false
	bombaUsada.Mutex.Unlock()
}