from fastapi import APIRouter
from app.schemas.requests import SelectFunctionRequest
from app.functions.selector import select_function
from app.functions.router import route_function
from app.functions.rules import apply_general_rules, apply_flight_priority_rules, normalize_flight_intent
from app.functions.high_level_intent import detect_high_level_intent
from app.state.session import get_session, mark_completed
from app.planner.planner import plan_next_step

router = APIRouter()

THRESHOLD = 0.6

HIGH_CONFIDENCE_THRESHOLD = 0.65
LOW_CONFIDENCE_THRESHOLD = 0.4


@router.post("/select")
def select(req: SelectFunctionRequest):
    
    session_id, session = get_session(req.session_id)
    completed = session["completed_steps"]
    intent, intent_score = detect_high_level_intent(req.query)

    if intent == "SOCIAL":
        return {
            "query": req.query,
            "function": "saludo",
            "response": route_function("saludo"),
            "score": intent_score,
            "source": "high_level_intent"
        }

    if intent == "OUT_OF_DOMAIN":
        return {
            "query": req.query,
            "function": "small_talk",
            "response": (
                "😄 Interesante! "
                "Si quieres, puedo ayudarte con información de vuelos."
            ),
            "score": intent_score,
            "source": "high_level_intent"
        }
    
    rule_function = apply_general_rules(req.query)
    if rule_function:
        return {
            "query": req.query,
            "function": rule_function,
            "response": route_function(rule_function),
            "score": 1.0,
            "source": "rules"
        }
        
    function_name = ""
    score = 0.0
    source = ""
    
    flight_rule = apply_flight_priority_rules(req.query)
    print(f"Función sugerida por reglas de vuelo: {flight_rule}")  # Debug statement
    if flight_rule:
        function_name = flight_rule
        score = 0.95
        source = "domain_rules"
    else:
        results = select_function(req.query, req.top_k)
        top = results[0]
        function_name = top["name"]
        score = top["score"]
        source = "embedding"
        
    
    function_name = normalize_flight_intent(req.query, function_name)
    print(f"Función después de normalización: {function_name}")  # Debug statement
    ACTION_FUNCTIONS = {
        "crear_reserva_vuelo",
        "cancelar_reserva_vuelo"
    }

    SEARCH_FUNCTIONS = {
        "buscar_vuelos",
        "consultar_horarios_vuelo",
        "consultar_precio_vuelo",
        "consultar_duracion_vuelo"
    }
    
    GENERAL_FUNCTIONS = {
        "saludo",
        "despedida",
        "agradecimiento",
        "small_talk"
    }
    

    if function_name in ACTION_FUNCTIONS and score < 0.65:
        return {
            "query": req.query,
            "function": "fallback",
            "response": (
                "Para continuar necesito un poco más de información "
                "sobre tu vuelo."
            ),
            "score": score,
            "source": "fallback"
        }

    if function_name in SEARCH_FUNCTIONS and score < 0.45:
        return {
            "query": req.query,
            "function": "fallback",
            "response": (
                "¿Podrías darme un poco más de detalle "
                "sobre el vuelo que buscas?"
            ),
            "score": score,
            "source": "fallback"
        }
        
    if function_name in GENERAL_FUNCTIONS:
        return {
            "query": req.query,
            "function": function_name,
            "response": route_function(function_name),
            "score": score,
            "source": "general_intent"
        }
    # 🔹 Planner decide el siguiente paso según Neo4j
    print(f"Planificando siguiente paso para función: {function_name}")  # Debug statement
    plan = plan_next_step(
        target_function=function_name,
        completed=completed  # luego aquí irá el estado de la conversación
    )

    print(plan["type"])
    if plan["type"] == "REQUIRE_STEP":
        required = plan["function"]
        return {
            "query": req.query,
            "function": required,
            "response": route_function(required),
            "score": score,
            "source": "planner"
        }

    if plan["type"] == "EXECUTE":
        mark_completed(session_id, function_name)
        return {
            "session_id": session_id,
            "query": req.query,
            "function": function_name,
            "response": route_function(function_name),
            "score": score,
            "source": "planner"
        }


    # fallback ultra seguro
    return {
        "query": req.query,
        "function": function_name,
        "response": route_function(function_name),
        "score": score,
        "source": source
    }