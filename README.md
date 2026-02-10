# Agente Inteligente para Planificación y Gestión de Vuelos

## Resumen

Este proyecto implementa un agente conversacional inteligente orientado a la búsqueda y reserva de vuelos. A diferencia de los chatbots tradicionales basados únicamente en clasificación de intenciones, el sistema incorpora planificación explícita de acciones, gestión de estado conversacional y razonamiento secuencial.

El agente combina reglas de negocio, selección de funciones mediante embeddings semánticos, un planner basado en grafos (Neo4j) y un modelo de lenguaje gratuito para la extracción de información desde texto natural. Esto permite guiar al usuario paso a paso hasta completar tareas complejas como la reserva de un vuelo, solicitando únicamente la información necesaria en cada etapa.

---

## Stack de Librerías y Tecnologías

- **Lenguaje:** Python 3.9  
- **Framework Backend:** FastAPI  
- **Base de Datos Relacional:** PostgreSQL / SQLite  
- **Base de Datos de Grafos:** Neo4j  
- **Embeddings Semánticos:** Sentence Transformers (all-MiniLM-L6-v2)  
- **LLM Gratuito:** Ollama (LLaMA 3 / Mistral)  
- **Persistencia de Estado:** Sesiones en memoria (session_id)  
- **Arquitectura:** Modular (rules + embeddings + planner + execution)  

---

## Flujo del Proceso del Agente

### Diagrama del Flujo

```mermaid
flowchart TD
    U[Usuario] --> Q[Query en lenguaje natural]

    Q --> HL[High-Level Intent Detection]
    HL -->|Social / Out of Domain| S[Respuesta social]

    HL -->|Dominio vuelos| R[Reglas generales y de dominio]

    R -->|Regla aplicada| F1[Función seleccionada]
    R -->|Sin regla| E[Selección por embeddings]

    E --> F1[Función seleccionada]

    F1 --> N[Normalización de intención]
    N --> P[Planner (Neo4j)]

    P -->|Paso previo requerido| PR[Solicitar información faltante]
    P -->|Puede ejecutar| EX[Ejecución de función]

    PR --> ST[Actualizar estado de sesión]
    EX --> ST[Actualizar estado de sesión]

    ST --> DB[(Base de datos)]
    ST --> LLM[LLM gratuito<br/>(extracción / lenguaje natural)]

    DB --> RES[Respuesta al usuario]
    LLM --> RES[Respuesta al usuario]
```

### Explicación del Flujo

1. El usuario envía una consulta en lenguaje natural.
2. Se identifica si la consulta corresponde a una intención social, fuera de dominio o relacionada con vuelos.
3. Se aplican reglas explícitas para casos prioritarios.
4. Si no hay reglas aplicables, se selecciona la función más relevante mediante similitud semántica.
5. El planner consulta el grafo de dependencias en Neo4j para determinar el siguiente paso necesario.
6. Se ejecuta la función correspondiente y se actualiza el estado de la conversación.
7. Se genera una respuesta natural y se continúa el flujo hasta completar la tarea.

---

## Conclusiones

El proyecto demuestra que la combinación de técnicas simbólicas y modelos de lenguaje permite construir agentes conversacionales más robustos y controlables. El uso de un planner basado en grafos garantiza la correcta secuencia de acciones, mientras que el LLM gratuito mejora la comprensión del lenguaje natural sin depender de servicios de pago. Esta arquitectura es escalable y puede extenderse fácilmente a otros dominios.

---

## Autores

- Paul Naspud  
- Camila Ramírez

---

## Información de Contacto

- 📧 Email: naspud972012@gmail.com, jr.6311.camm@gmail.com
- 🌐 GitHub: https://github.com/PaulSebastian9720, https://github.com/jennyfer04ramirez  
- 🏫 Proyecto académico universitario
