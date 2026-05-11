"""
Configuración centralizada usando Pydantic Settings.
Todas las variables de entorno se validan aquí.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """
    Variables de entorno + configuración por defecto.

    Usar: from config.settings import settings
    """

    # ========== APIs - LLMs ==========
    GEMINI_API_KEY: str
    CLAUDE_API_KEY: str
    ELEVENLABS_API_KEY: str
    TAVILY_API_KEY: str

    # ========== APIs - Social Media & Stock ==========
    TIKTOK_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    YOUTUBE_ACCESS_TOKEN: Optional[str] = None
    YOUTUBE_CLIENT_SECRET_PATH: Optional[str] = None
    PEXELS_API_KEY: Optional[str] = None

    # ========== AWS S3 ==========
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "eu-west-1"
    S3_BUCKET_NAME: str = "autonomous-agents-videos"

    # ========== Database ==========
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/autonomous_agents"
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None

    # ========== Cache ==========
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hora

    # ========== Email ==========
    ADMIN_EMAIL: str = "maxivivas211@gmail.com"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # ========== App Config ==========
    OLLAMA_HOST: str = "http://localhost:11434"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"

    # ========== Features ==========
    ENABLE_MULTI_TENANT: bool = True
    DEFAULT_REGION: str = "es"
    SUPPORTED_REGIONS: str = "es,us,mx,br,fr"
    ENABLE_VERBOSE_LOGGING: bool = False

    # ========== Timeouts ==========
    API_TIMEOUT_SECONDS: int = 30
    VIDEO_GENERATION_TIMEOUT: int = 600  # 10 minutos

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def supported_regions_list(self) -> List[str]:
        """Parse SUPPORTED_REGIONS string to list"""
        return [r.strip() for r in self.SUPPORTED_REGIONS.split(",")]

    def validate_apis(self) -> bool:
        """Valida que las APIs críticas estén configuradas"""
        required = [
            self.GEMINI_API_KEY,
            self.CLAUDE_API_KEY,
            self.ELEVENLABS_API_KEY,
            self.TAVILY_API_KEY
        ]
        return all(required)


# Crear instancia global
settings = Settings()

# Validación inicial
if not settings.validate_apis():
    print("⚠️ ADVERTENCIA: APIs no configuradas. Muchas funciones no funcionarán.")
    print("   Edita .env con tus claves de API.")
