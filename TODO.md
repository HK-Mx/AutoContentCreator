# 📋 TODO: Ruta de Implementación Progresiva

**Estado**: 🔴 EN CONSTRUCCIÓN  
**Próximo Paso**: Fase 1 - Agent 1 (Trends)

---

## 📍 FASE 1: AGENT 1 - TREND SCOUT 🔍

**Objetivo**: Que el sistema pueda buscar y filtrar trending topics reales.

**Archivo Principal**: `agents/agent_1_trends.py`

### 1.1 Preparación

- [ ] **API Key de Tavily**: 
  - [ ] Ir a https://tavily.com/
  - [ ] Crear cuenta (gratis)
  - [ ] Copiar API key
  - [ ] Pegar en `.env` como `TAVILY_API_KEY=xxx`

- [ ] **Test de configuración**:
  ```bash
  python -c "from config.settings import settings; print(settings.TAVILY_API_KEY)"
  ```
  Debe mostrar tu key (no "xxx")

### 1.2 Implementación Real

**Archivo**: `agents/agent_1_trends.py`

**Búscar**: Línea ~70 (`async def _search_tavily`)

**Reemplazar TODO con código real**:

```python
# BORRAR ESTO:
mock_trends = [...]

# REEMPLAZAR CON ESTO:
from tavily import TavilyClient

client = TavilyClient(api_key=self.tavily_api_key)
response = client.search(
    f"trending topics {self.region} last 24 hours",
    max_results=10,
    include_answer=True
)

trends = []
for result in response.get("results", []):
    trends.append({
        "title": result["title"],
        "url": result["url"],
        "content": result.get("content", ""),
        "source": result.get("source", "web")
    })

return trends
```

### 1.3 Filtrado con Ollama

**Búscar**: Línea ~130 (`async def _filter_with_ollama`)

**Reemplazar TODO con**:

```python
import httpx

filtered = []
async with httpx.AsyncClient() as client:
    for trend in trends:
        prompt = f'''
        Trend: {trend['title']}

        Rate (0-1): ¿Es monetizable en YouTube/TikTok/Instagram?
        Considera: viralidad potencial, demanda, competencia.
        Solo responde número.
        '''

        response = await client.post(
            f"{self.ollama_host}/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=10
        )

        score_text = response.json()["response"].strip()
        try:
            score = float(score_text)
            if score >= min_score:
                trend["monetization_score"] = score
                trend["discovered_at"] = datetime.now().isoformat()
                trend["region"] = self.region
                filtered.append(trend)
        except ValueError:
            continue

return filtered
```

### 1.4 Testing

```bash
# Test simple
python agents/agent_1_trends.py

# Deberías ver output como:
# 🔍 TREND SCOUT TEST RESULT
# Status: success
# Trends encontrados: 3
# 
# 1. OpenAI lanza GPT-5...
#    Score: 0.92
#    Source: techcrunch
```

### 1.5 ✅ Fase 1 Completa Cuando:

- [ ] Test local pasa sin errores
- [ ] Ves trends reales (no mocks)
- [ ] Scores varían según trend (no todos iguales)
- [ ] Sin errores de API

---

## 📍 FASE 2: AGENT 2 - SCRIPT MASTER ✍️

**Objetivo**: Generar guiones que no parezcan IA.

**Archivo Principal**: `agents/agent_2_script.py`

### 2.1 Obtener API Keys

- [ ] **Gemini API**:
  - [ ] Ir a https://makersuite.google.com/app/apikey
  - [ ] Crear proyecto
  - [ ] Copiar key → `.env` como `GEMINI_API_KEY=xxx`

- [ ] **Claude API**:
  - [ ] Ir a https://console.anthropic.com/account/keys
  - [ ] Crear key
  - [ ] Copiar → `.env` como `CLAUDE_API_KEY=xxx`

### 2.2 Implementación Gemini

**Búscar**: Línea ~100 en `agent_2_script.py` (`async def _generate_with_gemini`)

**Código real**:

```python
genai.configure(api_key=self.gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

system_prompt = f'''
Eres un guionista viral experto en {platform}.
Creas contenido que explota (viralidad) sin parecer IA.

TÉCNICAS ANTI-IA:
1. Variación sintáctica (oraciones cortas y largas)
2. Humanización (contracciones, exclamaciones, typos sutiles)
3. Breaking patterns (cambios de ritmo, capitalizaciones)
4. Cultural references (memes, slang local de {self.region})

VIRAL FRAMEWORK:
- Hook (0-3s): Pregunta o shock
- Loop (3-{duration-5}s): Mantén atención
- CTA ({duration-5}s final): Like, comment, follow
'''

response = model.generate_content([system_prompt, user_prompt])
return response.text
```

### 2.3 Implementación Claude

**Búscar**: Línea ~140 (`async def _validate_with_claude`)

**Código real**:

```python
client = anthropic.Anthropic(api_key=self.claude_api_key)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": f'''
        Revisa este guión y mejóralo si es necesario.

        Trend: {trend_title}
        Platform: {platform}

        GUIÓN ORIGINAL:
        {script}

        Mejora si:
        1. No es viral (falta hook, CTA, loop)
        2. Parece generado por IA
        3. Tiene issues de compliance

        Devuelve solo el guión final.
        '''
    }]
)

return response.content[0].text
```

### 2.4 Testing

```bash
python agents/agent_2_script.py

# Esperado:
# ✍️ SCRIPT MASTER TEST RESULT
# Status: success
# Platform: tiktok
# 
# [Voiceover]
# ¿Sabías que OpenAI...
```

### 2.5 ✅ Fase 2 Completa Cuando:

- [ ] Gemini genera scripts variados
- [ ] Claude valida y mejora
- [ ] Sin errores de API
- [ ] Scripts tienen estructura (Hook, Loop, CTA)

---

## 📍 FASE 3: AGENT 3 - VIDEO PRODUCER 🎬

**Objetivo**: Generar video con voz + background.

**Dependencia**: Fase 2 debe estar completa (necesita script)

### 3.1 API Keys

- [ ] **ElevenLabs**:
  - [ ] Ir a https://elevenlabs.io/
  - [ ] Crear cuenta (free: 10k caracteres)
  - [ ] API key → `.env` como `ELEVENLABS_API_KEY=xxx`

- [ ] **AWS S3** (para almacenamiento):
  - [ ] Crear cuenta AWS (free tier: 5GB)
  - [ ] IAM keys → `.env`
  - [ ] Crear bucket `autonomous-agents-videos`

### 3.2 Implementación ElevenLabs

**Búscar**: Línea ~90 en `agent_3_video.py` (`async def _generate_audio`)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=self.elevenlabs_api_key)

# Extraer voiceover del script
import re
voiceover_match = re.search(r'\[Voiceover Script\](.*?)\[', script, re.DOTALL)
voiceover_text = voiceover_match.group(1).strip() if voiceover_match else script

audio_data = client.text_to_speech(
    text=voiceover_text,
    voice_id="default",
    model_id="eleven_turbo_v2"
)

audio_path = f"/tmp/audio_{datetime.now().timestamp()}.mp3"
with open(audio_path, "wb") as f:
    f.write(audio_data)

return audio_path
```

### 3.3 Implementación MoviePy

**Búscar**: Línea ~120 (`async def _edit_video`)

```python
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

# Para testing: descargar video gratis
import requests
from io import BytesIO

# O usar un video local para testing
bg_video_path = "test_video.mp4"  # Descarga uno gratis de Pexels

video = VideoFileClip(bg_video_path)
audio = AudioFileClip(audio_path)

# Sincronizar duración
video = video.subclipped(0, min(video.duration, audio.duration))

# Exportar
output_path = f"/tmp/video_{trend_id}.mp4"
final_video = video.set_audio(audio)
final_video.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    verbose=False,
    logger=None
)

return output_path
```

### 3.4 Testing

```bash
python agents/agent_3_video.py

# Deberías ver:
# 🎬 VIDEO PRODUCER TEST RESULT
# Status: success
# Video URL: s3://...
# Duration: 60s
# Size: 25MB
```

### 3.5 ✅ Fase 3 Completa Cuando:

- [ ] ElevenLabs genera audio sin errores
- [ ] MoviePy edita video correctamente
- [ ] S3 upload funciona
- [ ] Tienes video final de ~25MB

---

## 📍 FASE 4: AGENT 4 - MULTI-PUBLISHER 📱

**Objetivo**: Publicar en Instagram, TikTok, YouTube.

**Dependencia**: Fase 3 debe estar completa

### 4.1 Credenciales (IMPORTANTE - Leer primero)

Tienes 2 opciones:

**Opción A: Simular publicaciones (recomendado para inicio)**
- No necesitas credenciales reales
- Devuelve URLs mock
- Útil para testing sin riesgo

**Opción B: Publicar real**
- Requiere credenciales reales de cada plataforma
- Más complejo de configurar
- Esperar a que esté todo probado

**Para ahora**: Usa Opción A (mock)

### 4.2 Testing

```bash
python agents/agent_4_publisher.py

# Output esperado:
# 📱 MULTI-PUBLISHER TEST RESULT
# Status: success
# 
# INSTAGRAM: published
#   URL: https://instagram.com/p/MOCK_...
# TIKTOK: published
#   URL: https://tiktok.com/@user/video/MOCK_...
# YOUTUBE: published
#   URL: https://youtube.com/shorts/MOCK_...
```

### 4.3 ✅ Fase 4 Completa Cuando:

- [ ] Mock publicaciones funciones
- [ ] URLs generadas correctamente
- [ ] No hay errores

---

## 📍 FASE 5: PIPELINE COMPLETO 🤖

**Objetivo**: Ejecutar todas las fases juntas.

### 5.1 Test del Orquestador

```bash
python core/orchestrator.py

# Deberías ver:
# 🤖 ORCHESTRATOR TEST RESULT
# Status: success
# 
# Metrics:
#   Trends: 5
#   Scripts: 5
#   Videos: 5
#   Publications: 15
#   Duration: 45.3s
#   Cost: €0.75
```

### 5.2 Test del Entry Point

```bash
python scripts/run_daily.py --test

# Deberías ver log completo con todas las fases
```

### 5.3 ✅ Fase 5 Completa Cuando:

- [ ] Pipeline ejecuta sin errores
- [ ] Todas las métricas se calculan correctamente
- [ ] Logs son claros y detallados

---

## 📍 FASE 6: DEPLOYMENT & AUTOMATIZACIÓN

### 6.1 Logs y Monitorización

```bash
# Crear carpeta de logs
mkdir -p logs

# Ver logs
tail -f logs/pipeline.log
```

### 6.2 Configurar Cron (Ejecución Diaria)

```bash
# Editar crontab
crontab -e

# Agregar esta línea (09:00 AM cada día):
0 9 * * * cd /path/to/AutoContentCreator && python scripts/run_daily.py >> logs/cron.log 2>&1
```

### 6.3 Email Reports (TODO)

**Archivo**: `scripts/generate_report.py` (crear)

Enviar resumen diario a `ADMIN_EMAIL`

### 6.4 Dashboard (TODO)

**Archivo**: `dashboard/server.py` (crear)

Servir HTML en `http://localhost:8000/dashboard`

---

## 🎯 Resumen de Progreso

```
Fase 1: Agent 1 (Trends)     [████░░░░░░] 40%
Fase 2: Agent 2 (Script)     [░░░░░░░░░░] 0%
Fase 3: Agent 3 (Video)      [░░░░░░░░░░] 0%
Fase 4: Agent 4 (Publisher)  [░░░░░░░░░░] 0%
Fase 5: Pipeline Completo    [░░░░░░░░░░] 0%
Fase 6: Deployment           [░░░░░░░░░░] 0%
```

---

## 🚀 Próximo Paso (AHORA MISMO)

1. **Editar `.env`**:
   ```bash
   cp .env.example .env
   nano .env  # Pega tu TAVILY_API_KEY
   ```

2. **Test Agent 1**:
   ```bash
   python agents/agent_1_trends.py
   ```

3. **Reporta aquí** qué funcionó y qué no.

---

## 📞 Soporte durante Implementación

Para cada fase que completes, **dile a Claude** exactamente:
- ✅ Qué funcionó
- ❌ Qué error viste
- 🤔 Qué no entiendes

Y seguiremos rellenando en orden. ¡Adelante! 🚀
