def route_function(function_name: str) -> str:
    """
    Router de funciones: recibe el nombre de la función seleccionada
    y devuelve la respuesta final para el usuario.
    """

    responses = {

        # =========================
        # FUNCIONES GENERALES
        # =========================
        "saludo": (
            "¡Hola! ✈️😊\n"
            "Puedo ayudarte a buscar vuelos, consultar precios, horarios "
            "o hacer una reserva. ¿Qué deseas hacer?"
        ),

        "despedida": (
            "¡Hasta luego! 👋\n"
            "Cuando quieras volver a consultar vuelos, aquí estaré."
        ),

        "agradecimiento": (
            "¡Con gusto! 😊\n"
            "Si necesitas algo más sobre vuelos, dime."
        ),

        "small_talk": (
            "¡Todo bien! 😄\n"
            "Cuéntame, ¿te ayudo a buscar algún vuelo?"
        ),

        # =========================
        # FUNCIONES DE VUELOS
        # =========================
        "buscar_vuelos": (
            "Perfecto ✈️\n"
            "¿Desde qué ciudad sales y hacia dónde quieres viajar?"
        ),

        "consultar_precio_vuelo": (
            "Claro 💰\n"
            "Dime el origen y destino del vuelo para darte un precio aproximado."
        ),

        "consultar_horarios_vuelo": (
            "Con gusto ⏰\n"
            "¿Entre qué ciudades deseas conocer los horarios de vuelo?"
        ),

        "consultar_duracion_vuelo": (
            "Sin problema ⏱️\n"
            "Dime el origen y destino para indicarte la duración del vuelo."
        ),

      
        "crear_reserva_vuelo": (
            "Excelente ✨\n"
            "Para crear tu reserva necesito el origen, destino y fecha del vuelo."
        ),

       
        "cancelar_reserva_vuelo": (
            "Entendido ❌\n"
            "Para cancelar tu vuelo, indícame el código de la reserva."
        ),

    }

    # Respuesta por defecto
    return responses.get(
        function_name,
        "Puedo ayudarte con búsquedas y reservas de vuelos. ¿Qué deseas hacer?"
    )
