def apply_general_rules(query: str):
    q = query.lower().strip()

    rules = {
        "saludo": [
            "hola", "buenos días", "buenas tardes", "buenas noches",
            "hey", "holaa", "buenas", "buenos dias", "hola qué tal", "que mas?", "que mas ve", "como vas"
        ],
        "despedida": [
            "chao", "adiós", "hasta luego", "nos vemos", "bye", "hablamos luego", "adios"
        ],
        "agradecimiento": [
            "gracias", "muchas gracias", "te agradezco", "mil gracias", "gracias por tu ayuda", "gracias por la info"
        ]
    }

    for function_name, keywords in rules.items():
        for k in keywords:
            if k in q:
                return function_name

    return None

def apply_flight_priority_rules(query: str):
    q = query.lower()

    # 1️⃣ ACCIONES FUERTES (PRIORIDAD MÁXIMA)
    print("Aplicando reglas de prioridad de vuelos...")  # Debug statement
    print(f"Query recibida: {query}")  # Debug statement
    print(any(k in q for k in [
        "reservar", "reserva", "comprar", "compra", "pagar", "pasaje"
    ]))
    if any(k in q for k in [
        "reservar", "reserva", "comprar", "compra", "pagar", "pasaje"
    ]):
        return "crear_reserva_vuelo"

    if any(k in q for k in [
        "cancelar", "anular"
    ]):
        return "cancelar_reserva_vuelo"

    # 2️⃣ CONSULTAS INFORMATIVAS EXPLÍCITAS
    if any(k in q for k in [
        "cuánto dura", "duración", "tiempo de vuelo", "horas"
    ]):
        return "consultar_duracion_vuelo"

    if any(k in q for k in [
        "precio", "cuánto cuesta", "valor", "tarifa"
    ]):
        return "consultar_precio_vuelo"

    if any(k in q for k in [
        "horario", "hora sale", "hora llega"
    ]):
        return "consultar_horarios_vuelo"

    # 3️⃣ BÚSQUEDA GENÉRICA DE VUELOS
    if "vuelo" in q or "vuelos" in q:
        return "buscar_vuelos"

    return None


def normalize_flight_intent(query: str, predicted_function: str):
    q = query.lower()

    explicit_price = any(k in q for k in [
        "precio", "cuánto cuesta", "valor", "tarifa"
    ])

    explicit_duration = any(k in q for k in [
        "duración", "cuánto dura", "tiempo de vuelo", "horas"
    ])

    explicit_schedule = any(k in q for k in [
        "horario", "hora sale", "hora llega"
    ])

    # Si el modelo predice algo informativo
    if predicted_function == "consultar_precio_vuelo" and not explicit_price:
        return "buscar_vuelos"

    if predicted_function == "consultar_duracion_vuelo" and not explicit_duration:
        return "buscar_vuelos"

    if predicted_function == "consultar_horarios_vuelo" and not explicit_schedule:
        return "buscar_vuelos"

    return predicted_function
