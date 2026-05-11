# 🚀 AutoContentCreator - Autonomous Media Engine

**AI-powered platform for automated content creation, publishing, and monetization across TikTok, Instagram, and YouTube.**

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Phase%202%20Beta-orange)

---

## 📋 Descripción

AutoContentCreator es un sistema multi-agente completamente autónomo que:

✅ **Detecta tendencias** en tiempo real (Google Trends API)  
✅ **Genera guiones virales** usando LLM (GPT-4 / Claude)  
✅ **Produce videos** compilados automáticamente (MoviePy + ElevenLabs)  
✅ **Publica simultáneamente** en TikTok, Instagram y YouTube  
✅ **Trackea monetización** y RPM en tiempo real  

**Costos:** €0/mes (free tier APIs)  
**ROI:** Infinito (sin costos = todo ingreso es ganancia)

---

## 🏗️ Arquitectura de Agentes

```
┌─────────────────────────────────────────────────┐
│    AUTONOMOUS MEDIA ENGINE - 5 AGENTES          │
├─────────────────────────────────────────────────┤
│                                                 │
│  Agent 1: TrendScout                            │
│  └─ Detecta tendencias trending 24h             │
│     Input: keywords[] | Output: trend_score     │
│                                                 │
│  Agent 2: Copywriter                            │
│  └─ Genera guiones viral con hooks              │
│     Input: topic | Output: script               │
│                                                 │
│  Agent 3: VideoProducer                         │
│  └─ Compila vídeos MP4 verticales               │
│     Input: script | Output: video.mp4           │
│                                                 │
│  Agent 4: Publisher                             │
│  └─ Publica en TikTok + Instagram + YouTube     │
│     Input: video_path | Output: video_urls[]    │
│                                                 │
│  Agent 5: MonetizationTracker                   │
│  └─ Trackea views, likes, RPM                   │
│     Input: video_id[] | Output: revenue, stats  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
AutoContentCreator/
├── agents/                          # 5 agentes principales
│   ├── base.py                      # Clase base para todos los agentes
│   ├── agent_1_trends.py            # Trend detection
│   ├── agent_2_script.py            # Copywriter
│   ├── agent_3_video.py             # Video production
│   ├── agent_4_publisher.py         # Multi-platform publishing
│   └── agent_5_monetization.py      # Revenue tracking
│
├── config/                          # Configuración
│   ├── settings.py                  # Pydantic settings (env vars)
│   └── youtube_secret.json          # ⚠️ GITIGNORED (OAuth)
│
├── output/                          # Outputs (generados, no en repo)
│   ├── videos/                      # MP4 compilados
│   ├── publications/                # Metadata de publicación
│   ├── monetization/                # Reports de ingresos
│   └── pipeline/                    # Logs de ejecución
│
├── run_complete_pipeline.py         # Orquestador principal
├── test_apis.py                     # Test de APIs
├── .env.example                     # Template de variables de entorno
├── .gitignore                       # Archivos a ignorar en Git
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── SETUP_APIS.md                    # Guía obtención de APIs
├── PHASE2_SUMMARY.md                # Resumen técnico Phase 2
│
├── terms_of_service.html            # Legal (público)
└── privacy_policy.html              # Legal (público)
```

---

## ⚙️ Setup & Instalación

### 1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/AutoContentCreator.git
cd AutoContentCreator
```

### 2. **Crear ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar variables de entorno**
```bash
cp .env.example .env
nano .env  # Editar con tus API keys
```

**⚠️ IMPORTANTE:** 
- NUNCA hagas commit de `.env`
- Solo edita `.env` en tu máquina local
- `.gitignore` protege `.env` automáticamente

### 5. **Configurar APIs** (Ver `SETUP_APIS.md`)
```bash
# Obtener keys de:
✅ Google (Gemini, YouTube)
✅ TikTok Developers
✅ Instagram Business
✅ ElevenLabs
✅ Pexels
```

### 6. **Test de conectividad**
```bash
python test_apis.py
```

---

## 🚀 Uso

### **Ejecutar pipeline completo** (genera 1 video diario)
```bash
python run_complete_pipeline.py
```

### **Test de agentes individuales**
```bash
# Agent 1: TrendScout
python agents/agent_1_trends.py

# Agent 3: VideoProducer
python agents/agent_3_video.py

# Agent 4: Publisher
python agents/agent_4_publisher.py

# Agent 5: MonetizationTracker
python agents/agent_5_monetization.py
```

### **Schedulear ejecución diaria** (Windows Task Scheduler)
```bash
# Crear tarea que ejecute daily:
python run_complete_pipeline.py
# Frecuencia: Diaria a las 09:00 AM
```

---

## 📊 Estimación de Ingresos

| Plataforma | Views/mes | CPM | Ingresos |
|---|---|---|---|
| TikTok | 30,000 | €0.25 | €7.50 |
| Instagram | 20,000 | €0.50 | €10.00 |
| YouTube | 5,000 | €2.00 | €10.00 |
| **TOTAL** | **55,000** | - | **€27.50/mes** |

*Con escalado a 3-5 nichos: €100-150/mes sin inversión*

---

## 🔑 API Keys Necesarias

| API | Propósito | Límite | Costo |
|---|---|---|---|
| **Google Gemini** | LLM para guiones | 60 req/min | Gratis |
| **Google YouTube** | Publishing + Analytics | 10,000 créditos/día | Gratis |
| **TikTok API v2** | Publishing + Stats | Custom | Gratis |
| **Instagram Graph** | Publishing + Stats | 200 req/hora | Gratis |
| **ElevenLabs** | Text-to-speech | 10K chars/mes | Gratis (free tier) |
| **Pexels** | Stock videos | 200 req/hora | Gratis |

**Total costo:** €0/mes ✅

---

## 📚 Documentación

- **[SETUP_APIS.md](./SETUP_APIS.md)** - Guía paso a paso para obtener APIs
- **[PHASE2_SUMMARY.md](./PHASE2_SUMMARY.md)** - Arquitectura técnica completa
- **[QUICK_START.md](./QUICK_START.md)** - Inicio rápido (5 minutos)

---

## 🔐 Seguridad

**Archivos protegidos por `.gitignore`:**
```
.env                    # Variables de entorno
config/youtube_secret.json  # OAuth credentials
*.key, *.pem           # Certificados SSL
.tiktok_tokens         # Tokens de acceso
.instagram_tokens      # Tokens de acceso
```

**Nunca subas estos archivos a Git** ⚠️

---

## 📝 Terms of Service & Privacy Policy

Para TikTok Developers, usa:
- **[Terms of Service](./terms_of_service.html)** - Políticas de uso
- **[Privacy Policy](./privacy_policy.html)** - Privacidad de datos

**URLs públicas:**
```
https://tu-dominio.com/terms_of_service.html
https://tu-dominio.com/privacy_policy.html
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Video:** MoviePy, FFmpeg
- **Audio:** ElevenLabs API
- **LLM:** Google Gemini / Claude
- **APIs:** TikTok, Instagram, YouTube
- **Data:** Pandas, NumPy
- **Async:** AsyncIO

---

## 📦 Dependencias Principales

```
pydantic-settings==2.0+
requests==2.31+
moviepy==1.0.3
elevenlabs==0.2.0
google-auth-oauthlib==1.1.0
google-api-python-client==2.99.0
pytrends==4.9.2
pandas==2.0+
```

*Ver [requirements.txt](./requirements.txt) completo*

---

## 🚀 Próximos Pasos

- [ ] Obtener APIs (ver SETUP_APIS.md)
- [ ] Configurar `.env` con tus keys
- [ ] Ejecutar `python run_complete_pipeline.py`
- [ ] Validar output en `output/` folder
- [ ] Crear cuentas TikTok/Instagram/YouTube
- [ ] Configurar scheduler diario
- [ ] Escalar a múltiples nichos

---

## 📞 Soporte

Para preguntas sobre:
- **APIs:** Ver SETUP_APIS.md
- **Arquitectura:** Ver PHASE2_SUMMARY.md
- **Quick start:** Ver QUICK_START.md

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

---

## ⚡ Status

- ✅ Phase 1: Trend detection + Copywriting
- ✅ Phase 2: Video production + Publishing + Monetization
- 🔄 Phase 3: Multi-niche scaling (Next)
- 🔄 Phase 4: Advanced A/B testing (Next)

**Current Version:** 2.0 (Phase 2 Beta)  
**Last Updated:** May 11, 2026

---

**Made with ❤️ for autonomous content creation**
