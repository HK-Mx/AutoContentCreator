# 🤖 AutoContentCreator - Sistema Multi-Agente de Generación Viral

Sistema **100% automático** de generación de contenido viral usando múltiples agentes IA en Python.

**Arquitectura**: Trends → Guión → Voz → Video → Publicación (4 agentes paralelos)

---

## ⚡ Setup Rápido (5 minutos)

### 1️⃣ Crear Virtual Environment

```bash
cd C:\Users\maxi\DATA\ SCIENCE\AutoContentCreator

python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Mac/Linux

pip install -r requirements.txt
```

### 2️⃣ Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env en VS Code y pegar tus API keys
```

### 3️⃣ Levantar Servicios (Docker)

```bash
docker-compose up -d
```

Espera ~30 segundos a que levanten. Verifica:
```bash
docker-compose ps
```

Deberías ver 4 servicios en estado "healthy":
- ollama ✅
- postgres ✅
- redis ✅
- app ✅

### 4️⃣ Descargar Modelo Ollama (1ª vez, ~10min)

```bash
docker exec autocontent-ollama ollama pull mistral
```

### 5️⃣ Inicializar Base de Datos

```bash
python scripts/setup_db.py
```

### 6️⃣ Ejecutar Test

```bash
python scripts/run_daily.py --test
```

Verás output como:
```
[2026-05-05 14:22:30] 🤖 Iniciando pipeline (test=True)...
[2026-05-05 14:22:31] 📍 Step 1/4: Descubriendo trends...
[2026-05-05 14:22:35] ✅ 1 trend encontrado
[2026-05-05 14:22:36] 📍 Step 2/4: Generando scripts...
[2026-05-05 14:22:45] ✅ 1 script generado
...
[2026-05-05 14:23:10] ✅ Pipeline terminado en 40.2s
```

### 7️⃣ Ver Dashboard

```bash
python dashboard/server.py
```

Abre: **http://localhost:8000/dashboard**

---

## 📁 Estructura del Proyecto

```
AutoContentCreator/
├── .env.example              ← Copiar a .env y rellenar
├── docker-compose.yml        ← Servicios locales
├── Dockerfile                ← Containerización
├── requirements.txt          ← Dependencias
├── README.md                 ← Este archivo
│
├── agents/                   ← 4 Agentes (TODO: rellenar)
│   ├── __init__.py
│   ├── base.py               ← Clase base para agentes
│   ├── agent_1_trends.py     ← 🔍 Descubre trending topics
│   ├── agent_2_script.py     ← ✍️ Genera guiones virales
│   ├── agent_3_video.py      ← 🎬 Produce video (voz + edición)
│   └── agent_4_publisher.py  ← 📱 Publica en redes
│
├── core/                     ← Módulos centrales
│   ├── orchestrator.py       ← Orquestador principal
│   ├── database.py           ← Conexión a Supabase/PostgreSQL
│   ├── storage.py            ← S3 wrapper (upload/download)
│   ├── compliance.py         ← RGPD + Legal + VPN
│   └── monitoring.py         ← Logs, métricas, errores
│
├── api/                      ← FastAPI
│   ├── main.py               ← App principal
│   ├── routes/
│   │   ├── health.py
│   │   ├── trigger.py        ← POST /trigger
│   │   ├── status.py         ← GET /status/{job_id}
│   │   ├── metrics.py        ← GET /metrics
│   │   └── webhooks.py       ← Callbacks
│   └── auth.py               ← JWT + multi-tenant
│
├── config/                   ← Configuración
│   ├── settings.py           ← Pydantic settings
│   ├── prompts/              ← System prompts
│   │   ├── trends_scout.md
│   │   ├── script_master.md
│   │   ├── video_producer.md
│   │   └── multi_publisher.md
│   └── legal/                ← Templates legales
│       ├── rgpd_notice.txt
│       ├── ai_disclosure.txt
│       └── vpn_terms.txt
│
├── scripts/                  ← Scripts utilitarios
│   ├── run_daily.py          ← Entry point principal
│   ├── setup_db.py           ← Inicializar BD
│   ├── test_agents.py        ← Tests
│   └── generate_report.py    ← Reportes email
│
├── dashboard/                ← Frontend + WebSocket
│   ├── index.html            ← UI (Make.com-like)
│   ├── server.py             ← Backend dashboard
│   └── assets/
│       ├── style.css
│       └── chart.js
│
├── migrations/               ← SQL migraciones
│   ├── 001_initial_schema.sql
│   └── 002_vpn_compliance.sql
│
└── tests/                    ← Tests unitarios
    ├── test_agents.py
    ├── test_compliance.py
    └── test_orchestration.py
```

---

## 🔑 APIs Requeridas (Presupuesto €100/mes)

| API | Costo | Límite | Uso |
|-----|-------|--------|-----|
| **Gemini 1.5 Flash** | Gratis | 100 req/min | Guiones |
| **Claude Sonnet** | ~€10/mes | 100k tokens | Validación |
| **ElevenLabs** | ~€15/mes | 10k chars | Voz TTS |
| **Tavily** | Gratis | Ilimitado | Trending topics |
| **Ollama** | €0 | Local | Orquestación |
| **AWS S3** | ~€15/mes | 1000 videos | Almacenamiento |
| **Supabase** | Gratis | 500k rows | Base de datos |
| **Redis** | €0 | Local | Cache |

**Total**: ~€40-60/mes (€100 de margen de seguridad)

---

## 📋 Próximos Pasos

### Fase 1: Rellenar Agent 1 (Trends) ← 🔴 AQUÍ ESTAMOS
1. [ ] Entender flujo de Agent 1
2. [ ] Rellenar con Tavily API
3. [ ] Testear con trending topics reales
4. [ ] Guardar en BD

### Fase 2: Rellenar Agent 2 (Script)
1. [ ] Integrar Gemini 1.5 Flash
2. [ ] Integrar Claude Sonnet (validación)
3. [ ] Implementar anti-IA bypass
4. [ ] Testear con 5 trends

### Fase 3: Rellenar Agent 3 (Video)
1. [ ] Integrar ElevenLabs TTS
2. [ ] Integrar MoviePy
3. [ ] Generar video de ejemplo
4. [ ] Subir a S3

### Fase 4: Rellenar Agent 4 (Publisher)
1. [ ] Integrar APIs de redes
2. [ ] Publicar test videos
3. [ ] Trackear engagement

### Fase 5: Production
1. [ ] Cron diario
2. [ ] Dashboard conectado
3. [ ] Email reports
4. [ ] Deploy en VPS

---

## 🧪 Testing

```bash
# Test de estructura (verifica que todo levanta)
python scripts/run_daily.py --test

# Test con debug verbose
python scripts/run_daily.py --test --verbose

# Tests unitarios
pytest tests/ -v
```

---

## 📊 Monitorización

### Dashboard
```
http://localhost:8000/dashboard
```

Muestra:
- 📈 Videos producidos
- 💰 ROI estimado
- 🔋 Tokens consumidos
- ⚠️ Error rate
- 📱 Engagement por plataforma

### Email Reports (Diarios)
Se envían automáticamente a `ADMIN_EMAIL` cada mañana a las 09:30

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
# En Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# En Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### "Ollama not responding"
```bash
docker-compose logs ollama
docker-compose restart ollama
# Esperar 30s y reintentar
```

### "Database connection failed"
```bash
# Verificar que postgres está healthy
docker-compose logs postgres

# Reiniciar todo
docker-compose down
docker-compose up -d
```

---

## 🚀 Deployment

### En VPS (Linode/DigitalOcean) - €5/mes
```bash
ssh root@tu-ip
git clone <repo>
cd AutoContentCreator
cp .env.example .env  # Editar con tus claves
docker-compose up -d

# Cron diario (09:00 AM)
(crontab -l 2>/dev/null; echo "0 9 * * * cd /root/AutoContentCreator && docker-compose exec -T app python scripts/run_daily.py") | crontab -
```

Dashboard: `http://tu-ip:8000/dashboard`

---

## 📞 Soporte

Para cualquier duda sobre los agentes, compliance, o deployment:
→ Consulta `SKILL.md` en la carpeta outputs/

---

**Made for Data Scientists. Python only. No Make.com.**

🚀 **¡Vamos a por ello!**
"# AutoContentCreator" 
