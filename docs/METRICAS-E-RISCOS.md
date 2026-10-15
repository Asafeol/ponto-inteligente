# Métricas de Sucesso e Riscos

A avaliação deve priorizar **eventos de anúncio**, não apenas resultados de frames individuais. Como regra de produto: **o limite de falsos anúncios deve ser mais rigoroso do que o limite de perda de anúncios**, porque a confiabilidade percebida é essencial para a acessibilidade.

## Métricas de sucesso

| Categoria | Métrica | Como medir |
|---|---|---|
| Identificação | Precisão por linha | Anúncios corretos ÷ total de anúncios da linha |
| Segurança | Falsos anúncios por hora | Quantidade de anúncios incorretos no período de teste |
| Cobertura | Taxa de detecção | Veículos relevantes anunciados ÷ veículos relevantes observados |
| Direção | Falsos positivos por sentido | Veículos do sentido oposto classificados como candidatos |
| Temporal | Latência de anúncio | Tempo entre entrada na zona configurada e o anúncio |
| Repetição | Anúncios duplicados por evento | Repetições não solicitadas para o mesmo veículo/viagem |
| Dados | Idade média do feed | Diferença entre horário atual e timestamp recebido |
| Visão | Confiança de OCR por evento | Maior ou média ponderada das leituras consistentes entre frames |
| Plataforma | Disponibilidade | Tempo em que o sistema permanece apto a operar |
| Usabilidade | Compreensão da mensagem | % de usuários que entendem corretamente o anúncio |

*Os valores-alvo específicos devem ser definidos após a coleta inicial de dados.*

## Riscos e mitigação

| Risco | Impacto | Probabilidade inicial | Mitigação |
|---|---|---|---|
| Feed público indisponível | Alto | Média | Adaptador substituível; manter visão como fallback |
| Feed atrasado ou inconsistente | Alto | Média | Validar timestamp, impor idade máxima, registrar qualidade |
| Letreiro ilegível | Alto | Alta | Múltiplos frames, ajuste óptico, pré-processamento, catálogo local |
| Falsos anúncios | Alto | Média | Persistência temporal, sentido correto, limiar de confiança |
| Ônibus de modelos diferentes | Médio | Alta | Coletar diversidade; começar por modelos frequentes no ponto |
| Chuva, noite e reflexos | Médio | Alta | Avaliar condições separadamente; ajustar câmera e exposição |
| Custo computacional | Médio | Média | Modelo leve, resolução reduzida, avaliar acelerador |
| Falha de energia/conectividade | Alto | Média | Reinicialização automática; operação degradada local |
| Ruído urbano | Alto | Alta | Testar alto-falante, volume, mensagens e posicionamento |
| Privacidade e autorização | Alto | Média | Processamento local, minimizar retenção, autorizações antes do piloto |
| Vandalismo e intempéries | Alto | Média | Caixa protegida, fixação adequada, plano de manutenção |
