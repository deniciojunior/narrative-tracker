# LinkedIn Post — Narrative Tracker

---

## POST PT-BR (principal)

**717 artigos. 17 fontes. 1 guerra. Narrativas completamente diferentes.**

Analisei com IA como cada grande veículo de mídia está cobrindo a Guerra EUA-Israel-Irã 2026 — e os resultados revelam algo que todo profissional de dados precisa ver.

O projeto usa Claude Haiku para classificar cada manchete em 7 frames narrativos e calcular um score de divergência (0–100) baseado na distância de Bhattacharyya.

**O que encontrei:**

→ **Press TV** tem score médio de 44.7 — o mais distante da narrativa global
→ **NYT** tem score 12.2 — o mais próximo do consenso entre as 17 fontes
→ **38.5%** dos artigos usam o frame "military" — o dominante no período
→ **44.9%** dos artigos têm tom neutro — mas 16% são alarmistas e 8.5% propagandísticos
→ Palavras características reveladoras: Press TV usa "agenda", "promise", "imminent" | NY Post usa "mehrabad", "crush", "despicable"

O mais fascinante: divergência ≠ viés. Uma fonte pode ter score alto sendo mais precisa — ou mais tendenciosa. O score mede *diferença*, não *qualidade*.

Todo o pipeline — coleta via RSS+GDELT, análise com IA, score de Bhattacharyya, dashboard Flask — custou menos de **$0.03** em tokens da API.

Isso é BI aplicado ao jornalismo. E está 100% aberto no GitHub.

🔗 Dashboard ao vivo → https://web-production-8d4b.up.railway.app
📦 GitHub → github.com/deniciojunior/narrative-tracker

Você leria as notícias diferente se soubesse o score de divergência de cada fonte?

#AnalíseDeMídia #InteligênciaArtificial #DataJournalism #OpenSource #NarrativeTracker #BI #DataScience #Jornalismo

---

## VERSÃO EN (first pinned comment)

**Same war. 17 narratives. Here's what the data shows.**

I built an open-source pipeline to analyze how major media outlets frame the US-Israel-Iran War 2026 using Claude Haiku AI.

After processing 717 articles from 17 sources (March 1–17, 2026):

- Most divergent source: Press TV (score 44.7/100)
- Most consensus-aligned: NYT (score 12.2/100)
- Dominant narrative frame: "military" (38.5% of all articles)
- Characteristic vocabulary reveals editorial choices that raw coverage hides

The full stack — RSS/GDELT collection, AI classification, Bhattacharyya divergence scoring, Flask dashboard — costs under $0.03 to run.

Live dashboard → https://web-production-8d4b.up.railway.app
Open source on GitHub → github.com/deniciojunior/narrative-tracker

Would you read news differently if every outlet had a divergence score?

#MediaAnalysis #AI #DataJournalism #OpenSource #NarrativeTracker

---

## VARIAÇÃO ALTERNATIVA (sem carrossel)

**O que descobri analisando 717 artigos de 17 fontes sobre a Guerra EUA-Israel-Irã:**

1. **Press TV diverge 44.7/100 da narrativa global** — o veículo mais distante do consenso entre todas as fontes monitoradas. NYT tem apenas 12.2.

2. **38.5% de todos os artigos usam o frame "militar"** — mas a mesma guerra é enquadrada como geopolítica (36.4%), humanitária (17%) ou diplomática (5.2%) dependendo de quem escreve.

3. **O vocabulário entrega a narrativa** — Press TV usa "agenda", "promise", "imminent". NY Post usa "mehrabad", "crush", "despicable". As palavras escolhidas revelam o frame antes de ler o texto.

4. **44.9% dos artigos são classificados como "neutros"** — mas 15.9% são alarmistas, 9.5% emocionais e 8.5% propagandísticos. Neutralidade é minoria mesmo entre as maiores redações.

5. **O custo total da análise foi menor que $0.03** — 717 artigos analisados com Claude Haiku via API. IA para análise de mídia em escala está ao alcance de qualquer desenvolvedor.

Todo o código está aberto no GitHub. Dashboard interativo com filtros por fonte, frame e data.

Qual dessas descobertas te surpreendeu mais?

#AnalíseDeMídia #IA #DataJournalism #OpenSource #NarrativeTracker #BI #DataScience #Jornalismo
