# Documentación del Proyecto: Motor Algorítmico para Mapas Dispersos

## Contexto del Proyecto

Este proyecto se desarrolla en el marco de la asignatura **Análisis y Diseño de Algoritmos I**. El objetivo es diseñar e implementar soluciones algorítmicas eficientes para procesar grandes volúmenes de datos dispersos o comprimidos, aplicando conceptos como:

- Estructuras de datos propias (sin usar las nativas de Python como `dict`, `set`, `heapq`, `sorted`, etc.)
- Análisis de complejidad temporal y de memoria.
- Procesamiento de archivos planos (`entrada.txt` → `salida.txt`).
- Estrategia de **dividir y vencer** en al menos una operación relevante.

El equipo ha seleccionado el **Problema 3: Compresor y analizador de mapas dispersos**. A continuación se detalla la solución implementada.

---

## Descripción del Problema

Se tiene un mapa de dimensiones potencialmente enormes (hasta \(10^9 \times 10^9\)), pero solo una cantidad limitada de posiciones contiene elementos significativos (obstáculos, recursos, enemigos, etc.). El programa debe:

- Almacenar únicamente las posiciones ocupadas.
- Responder a una serie de operaciones (consultas y modificaciones) de manera eficiente.
- Generar la salida exacta en el archivo `salida.txt`.

### Operaciones Soportadas

| Operación | Formato | Descripción | Salida |
|-----------|---------|-------------|--------|
| `GET` | `GET fila columna` | Retorna el tipo en esa posición, o `VACIO` si no hay. | `GET f c = tipo` |
| `SET` | `SET fila columna tipo` | Coloca un elemento (sobreescribe si existe). | `SET f c = OK` |
| `DELETE` | `DELETE fila columna` | Elimina el elemento en esa posición. | `DELETE f c = OK` (si existía) o `NO_EXISTE` |
| `COUNT_TYPE` | `COUNT_TYPE tipo` | Cuenta cuántos elementos de ese tipo hay en todo el mapa. | `COUNT_TYPE tipo = X` |
| `REGION_COUNT` | `REGION_COUNT f1 c1 f2 c2` | Cuenta elementos en el rectángulo [f1,f2]×[c1,c2]. | `REGION_COUNT ... = X` |
| `K_CERCANOS` | `K_CERCANOS fila columna k` | Retorna las k posiciones más cercanas (distancia Manhattan). | `K_CERCANOS ... = (f1,c1) (f2,c2) ...` |
| `COMPONENTES` | `COMPONENTES tipo` | Número de componentes conexas (4‑direcciones) de ese tipo. | `COMPONENTES tipo = X` |
| `TIPOS_REGION` | `TIPOS_REGION f1 c1 f2 c2` | Tipos distintos en la región, ordenados alfabéticamente. | `TIPOS_REGION ... = tipo1 tipo2 ...` |

---

## Solución Implementada

### Estructuras de Datos Propias

Para cumplir con las restricciones y lograr eficiencia, se implementaron manualmente las siguientes estructuras:

#### 1. Tabla Hash (`hash_table.py`)

- **Propósito**: Almacenar pares (fila, columna) → tipo, y también un contador (tipo → cantidad).
- **Implementación**:
  - Se usa una lista de `capacity` cajones (valor primo: 100003).
  - Función hash: para coordenadas → `(fila * 1000003 + columna) % capacity`; para strings (tipos) → suma ponderada de caracteres.
  - Colisiones resueltas mediante listas enlazadas (cada cajón es una lista de tuplas `(clave, valor)`).
- **Complejidad**: Inserción, búsqueda y eliminación en promedio \(O(1)\).

#### 2. Min‑Heap (`heap.py`)

- **Propósito**: Mantener los k elementos más cercanos en la operación `K_CERCANOS` sin ordenar todos.
- **Implementación**:
  - Árbol binario representado como lista.
  - Métodos `push` (inserción con flotación hacia arriba) y `pop` (extracción del mínimo con hundimiento).
  - Se almacenan tuplas `(distancia, fila, columna)`.
- **Complejidad**: Inserción y extracción \(O(\log n)\).

#### 3. Cola (`queue.py`)

- **Propósito**: Recorrido BFS para calcular componentes conexas (`COMPONENTES`).
- **Implementación**:
  - Lista dinámica con índice `front` para evitar desplazamientos.
  - Métodos `enqueue`, `dequeue`, `is_empty`.
- **Complejidad**: Operaciones \(O(1)\) amortizado.

#### 4. Merge Sort (`sort.py`)

- **Propósito**: Ordenar listas sin usar `sorted` ni `list.sort`; es la base de la estrategia de **dividir y vencer**.
- **Implementación**:
  - Función `merge_sort(arr, key=None)` recursiva.
  - Divide la lista en dos mitades, ordena cada una recursivamente y combina (`merge`) usando la clave de ordenamiento.
- **Complejidad**: \(O(n \log n)\) en el peor caso.

### Flujo General del Programa (`main.py`)

1. **Lectura** de `entrada.txt`:
   - Primera línea: dimensiones `F, C, N` (las dimensiones no se almacenan, solo se usan para validación, pero el mapa es conceptualmente infinito).
   - Siguientes `N` líneas: se insertan en la tabla hash `mapa` y se actualiza el contador `contador_tipos`.
   - Se lee `Q` y las operaciones.

2. **Procesamiento de cada operación**:
   - Se ejecuta la lógica específica usando las estructuras implementadas.
   - Cada operación que produce salida escribe una línea formateada en `salida.txt`.

3. **Escritura** del archivo `salida.txt` con los resultados exactos.

---

## Detalle de Cada Operación

### `GET fila columna`
- Se consulta `mapa.get((fila, columna))`.
- Si devuelve `None` → se escribe `VACIO`; en caso contrario se escribe el tipo.

### `SET fila columna tipo`
- Se obtiene el tipo anterior (si existe).
- Se llama a `mapa.put(...)` para insertar o reemplazar.
- Se actualiza el contador:
  - Si existía anterior, se decrementa su contador (y se elimina la clave si llega a 0).
  - Se incrementa el contador del nuevo tipo.
- Salida: `SET ... = OK`.

### `DELETE fila columna`
- Se obtiene el tipo actual.
- Si existe, se elimina de `mapa` y se actualiza el contador (decremento o eliminación de clave).
- Salida: `DELETE ... = OK` si existía, o `NO_EXISTE` en caso contrario.

### `COUNT_TYPE tipo`
- Se consulta `contador_tipos.get(tipo)`. Si es `None` se retorna 0.
- Salida: `COUNT_TYPE tipo = X`.

### `REGION_COUNT f1 c1 f2 c2`
- Se recorre **todos los elementos** del mapa (con `mapa.items()`) y se cuentan aquellos cuya fila y columna están dentro del rectángulo.
- **Nota de eficiencia**: Esta operación es \(O(N)\). Para mapas con \(N\) grande (millones) y muchas consultas, podría volverse lenta. Una mejora posible es mantener una lista ordenada y usar búsqueda binaria (no implementada por simplicidad, pero se menciona en el documento técnico como posible optimización).

### `K_CERCANOS fila columna k`
1. Se crea un `MinHeap`.
2. Se recorre todo el mapa y para cada elemento se calcula la distancia Manhattan y se inserta en el heap.
3. Se extraen hasta `k` elementos del heap (los de menor distancia).
4. Los puntos extraídos se ordenan con `merge_sort` usando una clave `(distancia, fila, columna)` para respetar los criterios de desempate.
5. Salida: lista de coordenadas en el formato `(fila,columna)`.

### `COMPONENTES tipo`
1. Se crea una tabla hash `visitados` para marcar coordenadas ya procesadas.
2. Se recorre el mapa completo; por cada elemento del tipo solicitado no visitado:
   - Se incrementa el contador de componentes.
   - Se realiza un BFS usando la `Queue` implementada:
     - Se encola la posición actual.
     - Se marcan como visitados sus vecinos (arriba, abajo, izquierda, derecha) que también sean del mismo tipo y no visitados.
3. Salida: número de componentes.

### `TIPOS_REGION f1 c1 f2 c2`
1. Se recorre el mapa y se agregan a una lista `tipos` aquellos elementos cuya coordenada esté dentro del rectángulo.
2. Se ordena la lista con `merge_sort`.
3. Se eliminan duplicados consecutivos.
4. Salida: lista de tipos únicos separados por espacios.

---

## Estrategia de Dividir y Vencer

La estrategia de **dividir y vencer** se aplica en el ordenamiento de listas mediante **merge sort**. Específicamente:

- **Operación**: `TIPOS_REGION` (también se usa indirectamente en `K_CERCANOS` para ordenar los puntos).
- **Problema que resuelve**: Ordenar una lista de strings (tipos) o de tuplas (coordenadas) de manera eficiente.
- **Caso base**: Lista de tamaño 0 o 1, ya ordenada.
- **División**: La lista se parte en dos mitades aproximadamente iguales.
- **Combinación**: Se mezclan (merge) las dos mitades ordenadas en una nueva lista ordenada.
- **Complejidad**: \(T(n) = 2T(n/2) + O(n)\) → \(O(n \log n)\).
- **Ventaja sobre solución ingenua**: Una solución ingenua como el ordenamiento por burbuja o inserción tendría complejidad \(O(n^2)\), inaceptable para listas grandes.

Esta implementación es puramente propia, sin usar `sorted` ni `list.sort`.

---

## Análisis de Complejidad (Resumen)

| Operación | Complejidad Esperada | Justificación |
|-----------|----------------------|----------------|
| `GET` | \(O(1)\) promedio | Tabla hash |
| `SET` | \(O(1)\) promedio | Tabla hash + contador |
| `DELETE` | \(O(1)\) promedio | Tabla hash |
| `COUNT_TYPE` | \(O(1)\) | Tabla hash del contador |
| `REGION_COUNT` | \(O(N)\) | Recorrido completo del mapa |
| `K_CERCANOS` | \(O(N \log k + k \log k)\) | Heap + ordenamiento final |
| `COMPONENTES` | \(O(M)\) | BFS sobre elementos del tipo (M) |
| `TIPOS_REGION` | \(O(N + t \log t)\) | Recorrido + ordenamiento (t tipos únicos en la región) |

Donde:
- \(N\): número total de elementos en el mapa.
- \(M\): número de elementos del tipo consultado.
- \(k\): número de cercanos solicitado.
- \(t\): número de tipos distintos en la región.

**Memoria**: \(O(N)\) para la tabla hash principal, más estructuras auxiliares transitorias.

---

## Instrucciones de Ejecución

1. Asegurar Python 3.6+.
2. Colocar `entrada.txt` en el mismo directorio que los archivos `.py`.
3. Ejecutar:
   ```bash
   python main.py
