# Solución

## 1. Diseño arquitectura

Por los requisitos que se piden, la arquitectura que mejor se adecúa es una de microservicios, ahora mismo conformada
sólo por 3 servicios:

- API (Django)
- SPA (Vue)
- DB

```
    +-----+            +-----------------+            +-----+
    |     |            |                 |            |     |
    | SPA | <--------> | API Microservice| <--------> |  DB |
    |     |   HTTP/S   |                 |    SQL     |     |
    +-----+            +-----------------+            +-----+
```

Esta arquitectura es altamente recomendada si se busca escalar rapidamente.

### 1.1 API

Django sigue un patron MVC, y evita salirte de ahí... todas las baterías incluidas de Django giran en torno a este
patrón, por lo que su desarrollo es bastante directo. Con REST no cambia demasiado, se añaden los serializadores, pero
el renderizado de las vistas sigue la misma lógica.

Además de servir los datos directamente desde DB, contiene el algoritmo para normalizar y clasificar los asteroides (que
explico más adelante).

### 1.2 SPA

Opté por una clean architecture. Siguiendo la filosofía de los microservicios, este tipo de arquitecturas ayudan a que
el código sea más mantenible y escalable a lo largo del tiempo. Por contra, llevan más tiempo de desarrollar, y por eso
no ha quedado del todo pulido. La idea es crear capas, donde cada una ejerce una función y solo se puede comunicar con
las inferiores, pero nunca con las superiores, siguiendo el principio de 'separation of concerns', el codigo se vuelve
mucho mas legible. En este repositorio esa comunicacion sería:

```
+--------+        +-----+
| Views  | <----- | API |
|        |        |     |
+--------+        +-----+
(Controllers)    (Services/Repositories)

```

Todas las vistas cargan de forma asíncrona.

## 2. Algoritmo de clasificación de asteroides

Reside en la API, en el archivo `services.py` (aunque probablemente sea más adecuado use case), con el nombre
de `MatrixService`.

Toma como entradas dos valores: la matriz 'vectorizada' (como una unica cadena de texto) y el numero de columnas que la
conforman. Y su cometido principal es devolver la matriz del asteroide normalizada. Es decir, que siguiendo el ejemplo
del pdf, pasar de esto:

```
0 0 0
0 0 0
1 0 0
1 0 0
1 1 0
1 1 0
0 0 0
```

A esto:

```
1 0 
1 0 
1 1 
1 1 
```

Porque sabemos que, a pesar de las diferentes resoluciones de los dispositivos de los observatorios, la forma del
asteroide es siempre la misma. Por tanto tendremos que normalizar nuestra matriz eliminando las vacias adyacentes.

Al instanciar nuestro servicio con los valores dados, se configuran varias cosas, pero lo más importante es el parseo de
los datos:

```python
class MatrixService:

    def __init__(self, vectorized_matrix: str, n_cols: int):
        self.matrix = self.parse_vector(vectorized_matrix, n_cols)
        self.cols = len(self.matrix[0])
        self.rows = len(self.matrix)
```

Esto deja nuestro servicio preparado para trabajar sobre la matrix numerica, en nuestro caso, para ejecutar el siguiente
metodo:

```python
def normalize(self) -> None:
    normalized_matrix = self.matrix
    top, right, bottom, left = self._get_matrix_limit_indexes()

    normalized_matrix = normalized_matrix[top:bottom + 1]
    normalized_matrix = [row[left:right + 1] for row in normalized_matrix]

    self.rows = len(normalized_matrix)
    self.cols = len(normalized_matrix[0])

    self.matrix = normalized_matrix
    self.vector = self.matrix_to_vector(normalized_matrix)
```

Para eliminar las celdas vacias adyacentes, lo que hace es obtener la posicion de limites de nuestro asteroide, es
decir, ¿en que filas hay valores desde arriba y abajo? ¿en qué columnas hay valores desde izquierda y derecha?

```
left = 0
|
0 0 0
0 0 0
1 0 0 <-- top = 2
1 0 0
1 1 0
1 1 0 <-- bottom = 5
0 0 0
  |
  right = 1
```

A partir de aqui, es facil indexar nuestra matriz para obtener solo el asteroide:

```python
normalized_matrix = normalized_matrix[top:bottom + 1]
normalized_matrix = [row[left:right + 1] for row in normalized_matrix]  
```

Y hacer con ella lo que queramos. Por mantener consistencia con la device matrix, decidí transformarla nuevamente en una
cadena de texto.

La razón por la que no se ejecuta esta normalización al instanciar `MatrixService` es porque se sigue un patrón **Single
Responsibility Principle** (SOLID). Instanciar tiene como unico objetivo configurar los ajustes y dependencias
necesarios para realizar el unico trabajo que tiene este servicio: normalizar (normalmente se le llama `execute`).

## 3. Views y models

En esta parte se han asumido varias cosas debido a la falta de tiempo. Por ejemplo, con matrices tan pequeñas, podría
darse el caso de asteroides repetidos, y como no hay identificador, se asume que es la matriz lo que los hace únicos.

Con el algoritmo preparado, crear las vistas para controlar el flujo es bastante directo. Desde las vistas vamos a
gestionar la logica de negocio (normalmente añado una capa de servicios por debajo). Aquí las de mayor relevancia son
las de crear y subir avistamientos, que hacen lo siguiente:

- Se crea u obtiene el observatorio dado el codigo
- Se crea u obtiene el dispositivo dado el codigo
- Se registra el avistamiento: datetime, observatorio, dispositivo, matriz. El conjunto es unico de sus valores, por
  tanto detecta si ya se ha subido un avistamiento con la mismas caracteristicas, en cuyo caso saltara un error.
- Si el avistamiento tiene un asteroide en la matriz (a traves de una property), ejecuta el algoritmo de clasificacion
- Se crea u obtiene el asteroide dada su matriz normalizada