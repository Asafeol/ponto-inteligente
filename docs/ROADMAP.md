# Roadmap — Plano de Execução por Fases

Este documento consolida o plano de execução do projeto, originalmente detalhado no documento de planejamento (v1.0). Cada fase tem finalidade, atividades, entregáveis e um **critério de passagem** — a condição objetiva que precisa ser satisfeita antes de avançar.

> **Nota:** a ordem de implementação foi ligeiramente adaptada na prática. Ver [`fase-atual-deteccao-onibus-yolov8.md`](fase-atual-deteccao-onibus-yolov8.md) para o registro da etapa em andamento.

---

## Fase 0 — Preparação, escopo e critérios de sucesso

**Finalidade.** Transformar a ideia em uma especificação executável e evitar que o primeiro protótipo fique amplo demais.

**Atividades.** Definir a cidade e o ponto de teste. Escolher as linhas e o sentido. Identificar usuários envolvidos, incluindo pessoas com deficiência visual ou organizações de acessibilidade. Definir as mensagens de áudio. Registrar restrições de energia, conectividade, instalação e privacidade. Estabelecer as métricas de sucesso antes de implementar.

**Entregáveis.** Documento de requisitos · Mapa do fluxo principal · Lista de premissas · Catálogo inicial de linhas e mensagens · Matriz de riscos · Plano de coleta de dados.

**Critério de passagem.** Existe um cenário de teste concreto, com entradas conhecidas e uma definição objetiva de "anúncio correto".

**Status:** ✅ Concluída (documento de planejamento v1.0)

---

## Fase 1 — Levantamento da fonte de transporte

**Finalidade.** Verificar se a telemetria pública é realmente utilizável no local escolhido.

**Atividades.** Localizar GTFS estático, GTFS-RT e APIs municipais. Confirmar autenticação, limites, frequência de atualização e licenças de uso. Identificar campos disponíveis (`vehicle_id`, `trip_id`, `route_id`, posição, bearing, velocidade, timestamp). Medir atrasos, lacunas e inconsistências. Baixar uma amostra para análise offline.

**Entregáveis.** Relatório da fonte de dados · Adaptador inicial · Amostras anonimizadas do feed · Mapa entre identificadores da API e o catálogo local.

**Critério de passagem.** A fonte fornece dados recentes o suficiente para o cenário, ou a decisão de usar visão como solução principal fica documentada.

**Status:** ⬜ Não iniciada

---

## Fase 2 — Protótipo do motor geográfico

**Finalidade.** Determinar se o sistema consegue distinguir ônibus relevantes de ônibus que passam no sentido oposto ou por vias próximas.

**Atividades.** Implementar a fórmula de Haversine com latitude e longitude em radianos. Implementar bearing e diferença angular normalizada. Comparar a posição do veículo com o ponto e, quando disponível, com a geometria da rota. Incorporar a idade máxima do feed. Criar filtros de velocidade, distância e direção. Reproduzir feeds gravados em modo simulação.

**Entregáveis.** Biblioteca ou módulo geográfico · Configuração do ponto · Logs de classificação · Relatório de falsos positivos e falsos negativos.

**Critério de passagem.** O motor classifica corretamente um conjunto de trajetórias reais ou simuladas e não trata dados antigos como se fossem atuais.

**Status:** ⬜ Não iniciada

---

## Fase 3 — Coleta e anotação de dados visuais

**Finalidade.** Criar evidência real para decidir se a câmera consegue complementar a telemetria.

**Atividades.** Gravar vídeos autorizados em horários e condições variadas. Registrar distância aproximada, iluminação, chuva, velocidade e linha conhecida. Extrair frames e recortes do letreiro. Anotar bounding boxes, região do letreiro, texto correto e qualidade da imagem. Remover dados não necessários ao treinamento e à avaliação.

**Entregáveis.** Dataset versionado · Guia de anotação · Divisão treino/validação/teste · Relatório de condições ambientais.

**Critério de passagem.** Existe uma base representativa das situações principais, sem misturar imagens quase idênticas entre treino e teste.

**Status:** 🟡 **Versão adaptada em andamento** — ver [documento da fase atual](fase-atual-deteccao-onibus-yolov8.md). Iniciando com datasets públicos (COCO, Roboflow, BDD100K) antes da coleta própria com vídeo autorizado.

---

## Fase 4 — Pipeline visual e pré-processamento

**Finalidade.** Medir a qualidade da imagem antes de investir no OCR.

**Atividades.** Testar detecção de ônibus com um modelo leve (**YOLOv8** — em andamento na fase atual). Iniciar com ROI proporcional à bounding box quando a câmera for fixa. Testar correção de perspectiva. Gerar versões em escala de cinza, com normalização de contraste, gamma, Otsu e limiar adaptativo. Comparar abertura, fechamento e dilatação com elementos estruturantes de tamanhos diferentes. Testar o efeito de vários frames consecutivos.

**Entregáveis.** Pipeline reproduzível · Galeria de exemplos antes/depois · Configuração de pré-processamento · Relatório de impacto por condição ambiental.

**Critério de passagem.** O pipeline melhora ou preserva a legibilidade em uma parcela significativa do dataset e não funde caracteres de modo excessivo.

**Status:** 🟡 Parcialmente em andamento (detecção YOLOv8)

---

## Fase 5 — OCR e casamento com catálogo local

**Finalidade.** Converter o letreiro em uma identificação confiável da linha ou destino.

**Atividades.** Avaliar PaddleOCR, CRNN ou outro OCR leve compatível com o hardware. Executar OCR em múltiplas versões de cada recorte. Fazer votação temporal entre frames. Normalizar caixa, espaços, acentos e abreviações. Comparar o resultado com o catálogo local usando distância de Levenshtein e regras específicas.

**Entregáveis.** Módulo OCR · Catálogo local · Função de pontuação · Matriz de confusão por linha · Lista de erros recorrentes.

**Critério de passagem.** O sistema consegue identificar as linhas do MVP com confiança suficiente para não gerar anúncios indevidos no teste controlado.

**Status:** ⬜ Não iniciada

---

## Fase 6 — Máquina de estados e fusão de evidências

**Finalidade.** Converter sinais instáveis em decisões consistentes e evitar anúncios repetidos.

**Atividades.** Implementar os estados `IDLE`, `VEÍCULO_CANDIDATO`, `APROXIMANDO`, `CONFIRMADO`, `ANUNCIADO` e `AGUARDANDO_SAÍDA`. Definir transições por distância, direção, idade do feed, confiança visual, persistência temporal e cooldown. Dar pesos separados para telemetria, detecção e OCR. Definir comportamento quando os sensores discordarem.

**Entregáveis.** Máquina de estados · Tabela de regras · Casos de teste · Logs de transição · Política de fallback.

**Critério de passagem.** O sistema anuncia no máximo uma vez por evento de aproximação e retorna ao estado inicial após a saída do veículo.

**Status:** ⬜ Não iniciada

---

## Fase 7 — Áudio, usabilidade e acessibilidade

**Finalidade.** Garantir que a informação seja percebida e útil para o público-alvo.

**Atividades.** Selecionar voz e velocidade. Definir volume e posicionamento do alto-falante. Criar mensagens curtas e consistentes. Testar repetição, inteligibilidade, ruído urbano. Realizar sessões com usuários ou especialistas em acessibilidade.

**Entregáveis.** Biblioteca de mensagens · Configuração de áudio · Relatório de testes de compreensão · Requisitos de interação física e sonora.

**Critério de passagem.** Os usuários conseguem compreender a mensagem em condições representativas e não consideram o comportamento excessivamente repetitivo ou confuso.

**Status:** ⬜ Não iniciada

---

## Fase 8 — Integração em hardware e operação degradada

**Finalidade.** Verificar se o protótipo funciona fora do computador de desenvolvimento.

**Atividades.** Executar o pipeline no hardware final. Medir latência, uso de CPU, memória, temperatura, consumo e estabilidade. Configurar reinicialização automática. Testar perda de internet, feed atrasado, câmera desconectada, falha de áudio, falta de energia.

**Entregáveis.** Imagem ou pacote instalável · Arquivo de configuração · Procedimento de instalação · Checklist de operação · Plano de recuperação.

**Critério de passagem.** O sistema permanece seguro e diagnosticável após falhas previsíveis e consegue retornar à operação sem intervenção frequente.

**Status:** ⬜ Não iniciada

---

## Fase 9 — Piloto controlado

**Finalidade.** Validar o comportamento completo em um ambiente real antes de qualquer expansão.

**Atividades.** Instalar o protótipo com autorização. Operar inicialmente sem áudio público, usando logs ou áudio monitorado. Corrigir parâmetros de distância, direção, confiança e cooldown. Liberar anúncios em horários controlados. Coletar feedback.

**Entregáveis.** Relatório do piloto · Lista priorizada de problemas · Versão candidata à operação · Decisão de continuar, ajustar ou interromper.

**Critério de passagem.** Os indicadores de precisão, disponibilidade, latência e usabilidade atingem os limites definidos na Fase 0.

**Status:** ⬜ Não iniciada

---

## Fase 10 — Encerramento do MVP e plano de escala

**Finalidade.** Consolidar o que foi aprendido e decidir se a solução está pronta para uma segunda implantação.

**Atividades.** Revisar métricas e riscos. Congelar a versão do modelo e da configuração. Documentar limitações. Estimar custos de hardware, instalação, conectividade e manutenção.

**Entregáveis.** Relatório final do MVP · Manual técnico · Manual operacional · Backlog da próxima versão · Decisão de escala.

**Critério de passagem.** Existe evidência suficiente para justificar a expansão ou uma decisão fundamentada de redesenho.

**Status:** ⬜ Não iniciada

---

## Critérios de decisão ao final de cada fase

| Decisão | Quando usar |
|---|---|
| **Prosseguir** | O critério de passagem foi atingido e os riscos restantes são controláveis |
| **Ajustar** | O conceito continua válido, mas os parâmetros ou componentes precisam ser alterados |
| **Reduzir escopo** | O resultado é promissor, mas a abrangência planejada é maior do que a capacidade atual |
| **Substituir componente** | Um fornecedor, modelo ou fonte de dados não atende aos requisitos |
| **Interromper** | Os dados demonstram que o cenário não é viável ou seguro nas condições atuais |
