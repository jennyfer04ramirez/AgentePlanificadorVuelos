from app.core.neo4j import driver

def get_required_steps(function_name: str) -> list[str]:
    query = """
    MATCH (prev:Function)-[:PRECEDE*]->(target:Function {name: $function})
    RETURN DISTINCT prev.name AS step
    """

    with driver.session() as session:
        result = session.run(query, function=function_name)
        return [r["step"] for r in result]


def plan_next_step(target_function: str, completed: set[str]) -> dict:
    required = set(get_required_steps(target_function))
    print(f"Función objetivo: {target_function}")
    print(f"Requisitos para {target_function}: {required}")
    missing = required - completed

    if not missing:
        return {
            "type": "EXECUTE",
            "function": target_function,
            "missing": []
        }

    return {
        "type": "REQUIRE_STEP",
        "function": sorted(missing)[0],
        "missing": list(missing)
    }