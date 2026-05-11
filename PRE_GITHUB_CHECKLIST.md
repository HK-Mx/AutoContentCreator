# ✅ CHECKLIST PRE-GITHUB

Ejecuta esta verificación antes de hacer push a GitHub.

---

## 🔐 ARCHIVOS SENSIBLES - MUST NOT GO TO GITHUB

```bash
# Verificar que estos archivos EXISTEN localmente pero NO en git:

❌ DEBE EXISTIR PERO NO EN GIT:
.env                           (variables de entorno)
config/youtube_secret.json     (OAuth credentials)
.tiktok_tokens                 (access tokens)
.instagram_tokens              (access tokens)
.youtube_tokens                (access tokens)

# Verifica ejecutando:
git status

# Deberías ver: "nothing to commit, working tree clean"
# NUNCA deberías ver .env en "Changes to be committed"
```

---

## 📁 ESTRUCTURA DEBE VERSE ASÍ

```
AutoContentCreator/
├── .env.example           ✅ (Público - template)
├── .env                   ❌ (PRIVADO - local only)
├── .gitignore             ✅
├── .gitattributes         ✅
├── requirements.txt       ✅
├── README_GITHUB.md       ✅
├── GITHUB_SETUP.md        ✅
├── SETUP_APIS.md          ✅
├── PHASE2_SUMMARY.md      ✅
├── PRE_GITHUB_CHECKLIST.md ✅
│
├── agents/                ✅
│   ├── base.py
│   ├── agent_1_trends.py
│   ├── agent_2_script.py
│   ├── agent_3_video.py
│   ├── agent_4_publisher.py
│   └── agent_5_monetization.py
│
├── config/                ✅
│   ├── settings.py
│   └── youtube_secret.json  ❌ (PRIVADO)
│
├── terms_of_service.html  ✅ (Va a gh-pages)
├── privacy_policy.html    ✅ (Va a gh-pages)
│
└── output/                ❌ (NO COMMITEAR - generados)
    ├── videos/
    ├── publications/
    ├── monetization/
    └── pipeline/
```

---

## 🔍 VERIFICACIONES ANTES DE PUSH

### 1. Verificar .gitignore está correcto

```bash
cd AutoContentCreator

# Ver qué archivos ignorará:
git status --ignored

# Debería mostrar:
# Ignored files:
#   .env
#   config/youtube_secret.json
#   output/
#   venv/
#   __pycache__/
```

### 2. Ver qué subirá

```bash
# Ver exactamente qué irá a GitHub:
git ls-files

# NUNCA debería mostrar:
# ❌ .env
# ❌ youtube_secret.json
# ❌ .tiktok_tokens
```

### 3. Verificar que .env local existe pero no en git

```bash
# Archivo debe existir:
ls -la .env           # Debería mostrar archivo

# Pero no debe estar tracked:
git ls-files | grep .env    # No debería mostrar nada
```

---

## 📋 ÚLTIMO CHECKLIST

Ejecuta antes de hacer `git push`:

```bash
# 1. Copiar .env.example a .env (si no existe)
cp .env.example .env
nano .env  # Editar con tus valores

# 2. Verificar que .env no está en git
git status  # NO debe aparecer .env

# 3. Verificar que requirements.txt está completo
cat requirements.txt | grep moviepy    # Debe mostrar moviepy
cat requirements.txt | grep elevenlabs # Debe mostrar elevenlabs

# 4. Verificar documentos HTML existen
ls -la terms_of_service.html    # Debe existir
ls -la privacy_policy.html      # Debe existir

# 5. Listar todo lo que se subirá
git ls-files --others --exclude-standard  # Mostrar archivos nuevos

# 6. FINAL CHECK - Status debe estar limpio
git status
# Expected output:
# On branch main
# nothing to commit, working tree clean
```

---

## 🚀 SI TODO ESTÁ BIEN, PUEDES HACER PUSH

```bash
# Agregar TODO
git add .

# Commit
git commit -m "Prepare for GitHub: Phase 2 complete"

# Push (primera vez)
git push -u origin main

# Push (próximas veces)
git push
```

---

## ⚠️ SI ALGO SALIÓ MAL

### Caso: "Acidentalmente commitee .env"

```bash
# PARAR inmediatamente:
git reset --soft HEAD~1

# Remover .env del staging:
git reset .env

# Commitear sin .env:
git commit -m "Fix: Remove .env from tracking"

# Push
git push
```

### Caso: ".env fue pusheado a GitHub"

```bash
# ⚡ URGENT - Cambiar todas las API keys inmediatamente

# Luego:
git rm --cached .env
git commit -m "Remove .env from git history"
git push

# Agregar a .gitignore (ya debe estar)
# Verificar: grep .env .gitignore
```

---

## ✅ TODO LISTO CUANDO:

- ✅ `.env` existe localmente pero no está en git
- ✅ `requirements.txt` tiene todas las dependencias
- ✅ `.env.example` tiene estructura completa
- ✅ `.gitignore` protege archivos sensibles
- ✅ `README_GITHUB.md` documentación completa
- ✅ Documentos HTML listos para gh-pages
- ✅ `git status` está limpio
- ✅ `git ls-files` NO muestra .env

**Cuando TODO esté OK: `git push` 🚀**

---

## 📞 POST-PUSH

Después de hacer push a main:

```bash
# 1. Ir a GitHub - verificar que el repo está public
# 2. Crear rama gh-pages para documentos
git checkout -b gh-pages
git add terms_of_service.html privacy_policy.html
git commit -m "Add legal documents"
git push -u origin gh-pages

# 3. En GitHub Settings → Pages → Source: gh-pages → Save
# 4. Esperar 5 minutos para que GitHub Pages compile
# 5. Verificar URLs:
# https://tu-usuario.github.io/AutoContentCreator/terms_of_service.html
# https://tu-usuario.github.io/AutoContentCreator/privacy_policy.html
```

---

**¡Cuando todo esté completado, estarás listo para TikTok Developers! 🎉**
