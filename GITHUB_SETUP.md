# 🚀 Setup para GitHub y Deploy

Guía completa para subir tu proyecto a GitHub y usar documentos legales online.

---

## 📤 PASO 1: CREAR REPOSITORIO EN GITHUB

### 1.1 Crear el repo
```bash
1. Ve a: https://github.com/new
2. Repository name: AutoContentCreator
3. Description: "AI-powered autonomous content creation platform"
4. Visibility: Public (para URLs públicas fáciles)
5. Click "Create repository"
```

### 1.2 Inicializar Git localmente
```bash
cd C:\Users\maxi\DATA SCIENCE\AutoContentCreator

# Inicializar repositorio
git init

# Agregar todas las carpetas excepto lo que está en .gitignore
git add .

# Commit inicial
git commit -m "Initial commit: Phase 2 complete - Autonomous Media Engine"

# Conectar con GitHub
git remote add origin https://github.com/TU-USUARIO/AutoContentCreator.git

# Push a main
git branch -M main
git push -u origin main
```

---

## 🔒 VERIFICAR QUE NO SUBES ARCHIVOS SENSIBLES

```bash
# Antes de hacer push, VERIFICA que .env NO esté incluido:
git status

# Debería mostrar:
# On branch main
# Your branch is ahead of 'origin/main' by X commits
# nothing to commit, working tree clean

# NUNCA debería mostrar .env en "Changes to be committed"
```

---

## 📄 PASO 2: HOSTEAR DOCUMENTOS LEGALES ONLINE

### Opción A: GitHub Pages (RECOMENDADO - Gratis, Permanente)

```bash
# 1. Crea una rama para documentos
git checkout -b gh-pages

# 2. Sube solo los HTMLs
git add terms_of_service.html privacy_policy.html
git commit -m "Add legal documents for TikTok"
git push -u origin gh-pages

# 3. En GitHub:
#    Settings → Pages → Source: gh-pages branch → Save

# 4. URLs públicas (en 3-5 minutos):
https://tu-usuario.github.io/AutoContentCreator/terms_of_service.html
https://tu-usuario.github.io/AutoContentCreator/privacy_policy.html
```

### Opción B: Netlify (Alternativa, Muy Fácil)

```bash
# 1. Ve a: https://app.netlify.com/
# 2. Conecta tu repositorio GitHub
# 3. Selecciona: AutoContentCreator repo
# 4. Build command: (dejar en blanco)
# 5. Publish directory: . (root)
# 6. Deploy

# URLs automáticas:
https://tuproyecto.netlify.app/terms_of_service.html
https://tuproyecto.netlify.app/privacy_policy.html
```

### Opción C: Vercel (Alternativa)

```bash
# 1. Ve a: https://vercel.com/
# 2. Import project → GitHub → AutoContentCreator
# 3. Deploy
# 4. URLs automáticas generadas
```

---

## 🔗 PASO 3: USAR URLS EN TIKTOK DEVELOPERS

Una vez que tengas los URLs públicos:

### En TikTok Developers:

```
Formulario "App Details":

Terms of Service URL:
https://tu-usuario.github.io/AutoContentCreator/terms_of_service.html

Privacy Policy URL:
https://tu-usuario.github.io/AutoContentCreator/privacy_policy.html
```

✅ **TikTok aceptará estos URLs sin problemas**

---

## 📋 CHECKLIST FINAL

```
ANTES de hacer push a GitHub:

Security:
☐ .env NO está en git (git status debe estar limpio)
☐ config/youtube_secret.json NO está en git
☐ Ninguna API key visible en archivos

Structure:
☐ requirements.txt tiene todas las dependencias
☐ .env.example tiene estructura completa
☐ .gitignore protege archivos sensibles
☐ README.md tiene instrucciones claras

Legal:
☐ terms_of_service.html está en rama gh-pages
☐ privacy_policy.html está en rama gh-pages
☐ URLs públicas funcionan en navegador

Documentation:
☐ README_GITHUB.md está completo
☐ SETUP_APIS.md tiene pasos claros
☐ PHASE2_SUMMARY.md está actualizado
```

---

## 🔄 FLUJO DIARIO

Después del setup inicial:

```bash
# Editar código localmente
nano agents/agent_1_trends.py

# Hacer commit
git add agents/agent_1_trends.py
git commit -m "Improve trend detection algorithm"

# Push a GitHub
git push

# (Los documentos en gh-pages se actualizan automáticamente)
```

---

## 📞 TROUBLESHOOTING

### Problema: "fatal: Could not read from remote repository"
```bash
# Solución: Verificar que tengas acceso SSH/HTTPS
git remote set-url origin https://github.com/tu-usuario/AutoContentCreator.git
git push
```

### Problema: ".env sigue en GitHub"
```bash
# Solución: Remover del historial
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

### Problema: Las URLs de GitHub Pages no funcionan
```bash
# Esperar 5-10 minutos después de push a gh-pages
# Si sigue sin funcionar, ir a Settings → Pages → cambiar source a "main" y volver a "gh-pages"
```

---

## 📊 ESTRUCTURA FINAL EN GITHUB

```
AutoContentCreator/
├── main branch
│   ├── agents/
│   ├── config/
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── README_GITHUB.md
│   └── (todo código)
│
└── gh-pages branch
    ├── terms_of_service.html
    └── privacy_policy.html
    └── (documentos legales públicos)
```

---

## 🎯 URLS FINALES

Después de todo:

```
Código: https://github.com/tu-usuario/AutoContentCreator
Terms: https://tu-usuario.github.io/AutoContentCreator/terms_of_service.html
Privacy: https://tu-usuario.github.io/AutoContentCreator/privacy_policy.html
TikTok App: (conectado con URLs de Terms y Privacy)
```

---

## ✅ Estás listo para:

1. ✅ Compartir código públicamente (sin secrets)
2. ✅ Colaborar con otros developers
3. ✅ Usar documentos legales en TikTok Developers
4. ✅ Escalar el proyecto

**Next: Configura APIs en .env y ejecuta `python run_complete_pipeline.py` 🚀**
