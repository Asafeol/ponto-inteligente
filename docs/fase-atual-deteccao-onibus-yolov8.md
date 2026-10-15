# Fase Atual — Treinamento de Detecção de Ônibus com YOLOv8

**Status:** 🟡 Em andamento
**Módulo relacionado:** `src/vision/`
**Pré-requisito para:** Fase 4 (Pipeline visual) e Fase 5 (OCR) do [ROADMAP](ROADMAP.md)

---

## 1. Objetivo desta etapa

Antes de instalar qualquer câmera apontada para a rua, este projeto precisa responder uma pergunta mais simples e barata de validar:

> **Um modelo de detecção consegue localizar um ônibus dentro de uma imagem com confiabilidade suficiente para, depois, recortar a região do letreiro?**

Por isso, a primeira etapa prática do projeto **não usa captura ao vivo**. Em vez disso, treina e avalia um modelo **YOLOv8** de detecção de objetos usando **datasets já existentes**, disponíveis publicamente ou gerados a partir de vídeos de teste controlados.

### Por que começar assim (e não pela câmera ao vivo)

| Motivo | Explicação |
|---|---|
| Custo de validação menor | Um dataset já anotado permite testar a viabilidade do modelo em horas, não em semanas de coleta de campo |
| Sem dependência de autorização/instalação | Câmera ao vivo em via pública exige autorizações que ainda não foram tratadas (ver Fase 0 do planejamento) |
| Isola a variável em teste | Permite responder “o modelo consegue detectar ônibus?” sem misturar problemas de instalação, energia ou conectividade |
| Alinhado ao princípio de escopo incremental | Evita investir cedo em componentes difíceis de validar (ver seção 10 do plano de execução) |

Esta decisão **antecipa parte da Fase 3/4** do roadmap original, mas de forma deliberadamente reduzida: o objetivo aqui é apenas provar a detecção do veículo, não ainda o letreiro nem o OCR.

---

## 2. Escopo desta etapa

**Dentro do escopo:**
- Treinar ou fazer fine-tuning de um modelo YOLOv8 para a classe `bus` (ônibus)
- Avaliar métricas de detecção (precisão, recall, mAP) em um conjunto de teste
- Documentar o desempenho do modelo em diferentes condições (ângulo, distância, iluminação, oclusão parcial)

**Fora do escopo (por enquanto):**
- Captura ao vivo de câmera real no ponto de ônibus
- Extração e leitura do letreiro (isso é a Fase 4/5)
- Qualquer processamento em tempo real ou hardware embarcado

---

## 3. Fontes de dados candidatas

O YOLOv8 já possui suporte nativo à classe `bus` através do dataset **COCO** (Common Objects in Context), que pode servir como ponto de partida com pesos pré-treinados (`yolov8n.pt`, `yolov8s.pt`, etc. da Ultralytics).

Datasets adicionais recomendados para fine-tuning e maior especificidade ao contexto de transporte urbano:

| Dataset | Observação |
|---|---|
| **COCO** (classe `bus`) | Já incluso nos pesos pré-treinados da Ultralytics — ponto de partida imediato, sem necessidade de treino do zero |
| **Roboflow Universe** (busca por "bus detection") | Diversos datasets já anotados no formato YOLO, prontos para download; verificar licença de cada um |
| **BDD100K** (Berkeley DeepDrive) | Dataset de condução urbana com múltiplas classes de veículos, incluindo ônibus, em variadas condições de iluminação e clima |
| **Open Images Dataset (classe Bus)** | Grande volume de imagens anotadas, permite filtrar apenas a classe de interesse |
| Vídeos autorizados próprios (fase futura) | Conforme protocolo de coleta a ser definido na Fase 3 completa do roadmap |

> **Nota de licenciamento:** ao escolher um dataset, registrar a licença de uso em `docs/DATASETS.md` (ver seção 6) antes de baixar ou versionar qualquer arquivo.

---

## 4. Ambiente e dependências

```
ultralytics>=8.1.0      # framework YOLOv8
torch                   # backend de treino/inferência
opencv-python           # manipulação de imagens
pyyaml                  # arquivos de configuração do dataset
```

Ver `requirements.txt` na raiz do repositório para a lista completa.

---

## 5. Passo a passo desta etapa

1. **Escolher e baixar o dataset inicial** (recomendação: começar pelos pesos COCO pré-treinados da Ultralytics, que já reconhecem `bus`, antes de investir em fine-tuning)
2. **Organizar os dados no formato YOLO**, com estrutura `images/` e `labels/` separadas em `train/`, `val/` e `test/`
3. **Registrar a origem e licença do dataset** em `docs/DATASETS.md`
4. **Rodar uma inferência inicial** com os pesos pré-treinados (`yolov8n.pt`) sobre uma amostra de imagens de ônibus, sem treino adicional, para estabelecer uma linha de base (*baseline*)
5. **Avaliar a linha de base**: registrar mAP, precisão e recall na amostra de teste
6. **Decidir se fine-tuning é necessário**: se a linha de base já for suficiente para o contexto do projeto (ônibus urbanos brasileiros, ângulos de ponto de ônibus), avançar direto para a Fase 4. Caso contrário, fazer fine-tuning com dataset adicional (Roboflow/BDD100K)
7. **Documentar os resultados** em `docs/resultados-treinamento-yolov8.md`, incluindo matriz de confusão, exemplos de acerto e erro, e condições onde o modelo falha

---

## 6. Entregáveis desta etapa

- [ ] `docs/DATASETS.md` com fontes, licenças e critérios de seleção
- [ ] `tools/train_yolov8.py` — script de treino/fine-tuning reprodutível
- [ ] `tools/evaluate_yolov8.py` — script de avaliação com métricas
- [ ] `models/bus-detector-v0.pt` — pesos do modelo treinado (ou referência de release, se muito grande para o Git)
- [ ] `docs/resultados-treinamento-yolov8.md` — relatório de métricas e exemplos visuais
- [ ] Registro de decisão: seguir com este modelo, ajustar dataset, ou trocar de abordagem

---

## 7. Critério de passagem para a próxima etapa

Esta etapa é considerada concluída quando:

- O modelo detecta corretamente ônibus em uma amostra de teste representativa (múltiplos ângulos, distâncias e condições de iluminação), com métricas registradas (não apenas "parece funcionar");
- As limitações conhecidas do modelo estão documentadas (ex: baixo desempenho à noite, com chuva, ou em ângulos muito laterais);
- Existe uma decisão registrada sobre qual conjunto de pesos seguirá para a próxima fase.

Somente após esse critério, o projeto avança para a **Fase 4 (Pipeline visual e pré-processamento)**, que já trabalha com a região do letreiro — e, mais adiante, para a captura de vídeo real (Fase 3 completa do roadmap original).

---

## 8. Relação com o roadmap completo

Este documento cobre uma versão adaptada e antecipada das Fases 3 e 4 descritas em [`ROADMAP.md`](ROADMAP.md). A ordem completa recomendada no planejamento original permanece válida — a mudança aqui é apenas de **sequenciamento tático**: provar a detecção do veículo com dados já existentes antes de partir para coleta própria e instalação de câmera real.
