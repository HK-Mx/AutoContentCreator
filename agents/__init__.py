"""
Módulo de Agentes: 4 agentes especializados para generación de contenido viral.

Agent 1: TrendScout 🔍 - Descubre trending topics
Agent 2: ScriptMaster ✍️ - Genera guiones virales
Agent 3: VideoProducer 🎬 - Produce video
Agent 4: MultiPublisher 📱 - Publica en redes
"""

from agents.base import BaseAgent
from agents.agent_1_trends import TrendScout
from agents.agent_2_script import ScriptMaster
from agents.agent_3_video import VideoProducer
from agents.agent_4_publisher import MultiPublisher

__all__ = [
    "BaseAgent",
    "TrendScout",
    "ScriptMaster",
    "VideoProducer",
    "MultiPublisher"
]
