# main.py
import sys
from hash_table import HashTable
from heap import MinHeap
from queue import Queue
from sort import merge_sort
from geometry import manhattan_distance

def main():
    # Leer archivo
    with open('entrada.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        return
    
    # Primera línea: F C N
    F, C, N = map(int, lines[0].split())
    idx = 1
    # Leer N elementos iniciales
    mapa = HashTable()  # clave: (fila, columna), valor: tipo
    contador_tipos = HashTable()  # clave: tipo (string), valor: entero
    
    for i in range(N):
        parts = lines[idx].split()
        fila = int(parts[0])
        columna = int(parts[1])
        tipo = parts[2]
        idx += 1
        mapa.put((fila, columna), tipo)
        # Actualizar contador
        count = contador_tipos.get(tipo)
        if count is None:
            contador_tipos.put(tipo, 1)
        else:
            contador_tipos.put(tipo, count + 1)
    
    # Siguiente línea: Q
    Q = int(lines[idx])
    idx += 1
    operaciones = lines[idx:idx+Q]
    
    # Procesar operaciones y escribir salida
    with open('salida.txt', 'w', encoding='utf-8') as out:
        for op in operaciones:
            parts = op.split()
            cmd = parts[0]
            
            if cmd == 'GET':
                f = int(parts[1])
                c = int(parts[2])
                tipo = mapa.get((f, c))
                if tipo is None:
                    out.write(f'GET {f} {c} = VACIO\n')
                else:
                    out.write(f'GET {f} {c} = {tipo}\n')
            
            elif cmd == 'SET':
                f = int(parts[1])
                c = int(parts[2])
                nuevo_tipo = parts[3]
                viejo_tipo = mapa.get((f, c))
                mapa.put((f, c), nuevo_tipo)
                # Actualizar contadores
                if viejo_tipo is not None:
                    old_count = contador_tipos.get(viejo_tipo)
                    if old_count == 1:
                        contador_tipos.delete(viejo_tipo)
                    else:
                        contador_tipos.put(viejo_tipo, old_count - 1)
                new_count = contador_tipos.get(nuevo_tipo)
                if new_count is None:
                    contador_tipos.put(nuevo_tipo, 1)
                else:
                    contador_tipos.put(nuevo_tipo, new_count + 1)
                out.write(f'SET {f} {c} = OK\n')
            
            elif cmd == 'DELETE':
                f = int(parts[1])
                c = int(parts[2])
                viejo_tipo = mapa.get((f, c))
                if viejo_tipo is not None:
                    mapa.delete((f, c))
                    # Actualizar contador
                    old_count = contador_tipos.get(viejo_tipo)
                    if old_count == 1:
                        contador_tipos.delete(viejo_tipo)
                    else:
                        contador_tipos.put(viejo_tipo, old_count - 1)
                    out.write(f'DELETE {f} {c} = OK\n')
                else:
                    out.write(f'DELETE {f} {c} = NO_EXISTE\n')
            
            elif cmd == 'COUNT_TYPE':
                tipo = parts[1]
                count = contador_tipos.get(tipo)
                if count is None:
                    count = 0
                out.write(f'COUNT_TYPE {tipo} = {count}\n')
            
            elif cmd == 'REGION_COUNT':
                f1, c1, f2, c2 = map(int, parts[1:5])
                total = 0
                for (f, c), tipo in mapa.items():
                    if f1 <= f <= f2 and c1 <= c <= c2:
                        total += 1
                out.write(f'REGION_COUNT {f1} {c1} {f2} {c2} = {total}\n')
            
            elif cmd == 'K_CERCANOS':
                fila = int(parts[1])
                columna = int(parts[2])
                k = int(parts[3])
                heap = MinHeap()
                for (f, c), t in mapa.items():
                    dist = manhattan_distance(f, c, fila, columna)
                    heap.push(dist, f, c)
                # Extraer los k más cercanos
                cercanos = []
                for _ in range(min(k, heap.size())):
                    dist, f, c = heap.pop()
                    cercanos.append((f, c))
                # Ordenar por distancia (ya vienen en orden por el heap) pero si hay empates, ordenar por fila y columna
                # Como el heap es min-heap, ya los extrajo en orden de distancia creciente. Pero para empates, no garantiza orden por fila/columna.
                # Usamos merge_sort con clave compuesta
                def clave(punto):
                    f, c = punto
                    return (manhattan_distance(f, c, fila, columna), f, c)
                cercanos_ordenados = merge_sort(cercanos, key=clave)
                out.write(f'K_CERCANOS {fila} {columna} {k} =')
                for (f, c) in cercanos_ordenados[:k]:
                    out.write(f' ({f},{c})')
                out.write('\n')
            
            elif cmd == 'COMPONENTES':
                tipo = parts[1]
                # BFS para contar componentes conexas (4 direcciones)
                visitados = HashTable()
                componentes = 0
                # Recorrer todos los elementos del tipo dado
                for (f, c), t in mapa.items():
                    if t == tipo and not visitados.get((f, c)):
                        # Nuevo componente
                        componentes += 1
                        q = Queue()
                        q.enqueue((f, c))
                        visitados.put((f, c), True)
                        while not q.is_empty():
                            cf, cc = q.dequeue()
                            # Vecinos en 4 direcciones
                            for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                                nf = cf + df
                                nc = cc + dc
                                if mapa.get((nf, nc)) == tipo and not visitados.get((nf, nc)):
                                    visitados.put((nf, nc), True)
                                    q.enqueue((nf, nc))
                out.write(f'COMPONENTES {tipo} = {componentes}\n')
            
            elif cmd == 'TIPOS_REGION':
                f1, c1, f2, c2 = map(int, parts[1:5])
                tipos_encontrados = []
                for (f, c), t in mapa.items():
                    if f1 <= f <= f2 and c1 <= c <= c2:
                        tipos_encontrados.append(t)
                # Ordenar y eliminar duplicados
                if not tipos_encontrados:
                    out.write(f'TIPOS_REGION {f1} {c1} {f2} {c2} =\n')
                else:
                    tipos_ordenados = merge_sort(tipos_encontrados)
                    # Eliminar duplicados
                    unicos = []
                    for i in range(len(tipos_ordenados)):
                        if i == 0 or tipos_ordenados[i] != tipos_ordenados[i-1]:
                            unicos.append(tipos_ordenados[i])
                    out.write(f'TIPOS_REGION {f1} {c1} {f2} {c2} = ' + ' '.join(unicos) + '\n')
            
            else:
                # Operación desconocida (por si acaso)
                out.write(f'Operacion no soportada: {cmd}\n')
    
if __name__ == '__main__':
    main()