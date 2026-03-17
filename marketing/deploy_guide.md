# Deploy gratuito no Railway

Railway é a melhor opção para este projeto:
- Suporta Flask nativo
- Volumes persistentes (SQLite sobrevive a restarts)
- $5 de crédito grátis/mês (suficiente para este projeto)

## Passo 1 — Arquivos de deploy (já criados)

O projeto já inclui `Procfile`, `railway.toml` e `nixpacks.toml`.

## Passo 2 — Configura o app.py para produção

Modifica o final de `src/app.py`:
```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

## Passo 3 — Deploy no Railway

1. Vai em [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Seleciona o repositório `narrative-tracker`
3. Em **Variables**, adiciona:
   ```
   ANTHROPIC_API_KEY = sk-ant-...
   PYTHONUNBUFFERED = 1
   PYTHONUTF8 = 1
   ```
4. Railway detecta o Procfile automaticamente
5. Em 3–5 minutos, o dashboard está online

## Passo 4 — Worker (atualização horária)

1. New Service → Worker
2. Mesmo repositório
3. Start command: `python src/scheduler.py`
4. Mesmas variáveis de ambiente
5. O `scheduler.py` já tem o loop de 3600s

## Passo 5 — Volume persistente (SQLite)

1. Settings → Volumes → Add Volume
2. Mount path: `/app/data`
3. Define `DB_PATH=/app/data/articles.db` nas variáveis
4. Os scripts já leem `DB_PATH` do ambiente

## Passo 6 — Seed inicial do banco

```bash
railway run python src/collector.py
railway run python src/analyzer.py
railway run python src/scorer.py
```

Ou faz upload do `articles.db` via Railway Volume.

## Resultado esperado

- Dashboard online 24/7 em `[projeto].up.railway.app`
- Novos artigos coletados a cada hora
- Análise e scores recalculados automaticamente
- **Custo estimado**: $2–4/mês

## Alternativas gratuitas

| Plataforma   | Vantagem           | Limitação                     |
|--------------|--------------------|-------------------------------|
| Railway      | Melhor para Flask  | $5 crédito/mês                |
| Render       | Totalmente grátis  | Dorme após 15min de inatividade |
| Fly.io       | Muito flexível     | Curva de aprendizado          |
| HuggingFace  | Grátis ilimitado   | Não persiste arquivos         |

Para zero custo absoluto: **Render (free tier)** — o dashboard demora ~30s para acordar após inatividade, mas funciona.
