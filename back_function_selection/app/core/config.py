from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "aws-1-us-east-1.pooler.supabase.com"
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres.znkewdqukpfmzjmkfxea"
    DB_PASSWORD: str = "planificador123"
    DB_PORT: int = 5432
    NEO4J_URI: str = "neo4j://127.0.0.1:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j1234"

settings = Settings()
