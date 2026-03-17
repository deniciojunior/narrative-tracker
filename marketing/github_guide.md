# Como publicar o projeto no GitHub

## 1. Prepara o repositório local
```bash
git init
git add .
git commit -m "feat: initial release — narrative tracker v1.0"
```

## 2. Cria o repositório no GitHub
- Vai em github.com/new
- Nome: `narrative-tracker`
- Descrição: AI-powered media framing analysis of the US-Israel-Iran War 2026
- Público ✓
- NÃO inicializa com README (já temos)

## 3. Conecta e faz push
```bash
git remote add origin https://github.com/[SEU_USER]/narrative-tracker.git
git branch -M main
git push -u origin main
```

## 4. Configura o GitHub
- About: adiciona descrição + website (URL do deploy)
- Topics: `python` `media-analysis` `ai` `flask` `middle-east` `journalism` `claude` `gdelt` `data-visualization`
- Releases → cria release `v1.0.0`

## 5. Verifica o .gitignore
- `articles.db` NÃO foi commitado (dados locais)
- `.env` NÃO foi commitado (API key)
- `marketing/slides/*.png` NÃO foi commitado (gera localmente)
