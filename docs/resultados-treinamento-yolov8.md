# Resultados — Detecção de Ônibus com YOLOv8

> Manter o histórico: cada nova rodada entra como uma nova versão, sem sobrescrever as anteriores.

## Versão v0 — Linha de base (pesos pré-treinados COCO, sem fine-tuning)

**Data:** 16/10/2026
**Pesos:** `yolov8n.pt` (Ultralytics 8.4.177, pré-treinado no COCO; classe 5 = `bus`)
**Hardware:** CPU (Intel Xeon 2,8 GHz, 2 núcleos), sem GPU
**Conjunto de teste:** PASCAL VOC 2007, split de teste, montado com `tools/prepare_voc_bus.py` (ver `docs/DATASETS.md`)

| Composição do conjunto | Quantidade |
|---|---|
| Imagens com ônibus | 183 |
| Ônibus anotados (excluindo os marcados como *difficult*) | 213 |
| Imagens negativas com carro (distrator) | 704 |
| Imagens negativas aleatórias | 300 |
| Total de imagens | 1187 |

### Métricas globais (`tools/evaluate_yolov8.py`)

| Métrica | Valor |
|---|---|
| mAP50 | 0,931 |
| mAP50-95 | 0,815 |
| Precisão (no ponto de operação escolhido pelo YOLO) | 0,862 |
| Recall (no mesmo ponto) | 0,878 |
| Tempo de inferência | ≈ 95 ms/imagem em CPU |

### Precisão e recall por limiar de confiança (`tools/analyze_thresholds.py`, IoU ≥ 0,5)

| $s_{\min}$ | VP | FP | FN | Precisão | Recall | FP em imagens com ônibus | FP em imagens com carro | FP em outras |
|---|---|---|---|---|---|---|---|---|
| 0,25 | 194 | 49 | 19 | 0,798 | 0,911 | 28 | 21 | 0 |
| 0,40 | 190 | 26 | 23 | 0,880 | 0,892 | 18 | 8 | 0 |
| 0,50 | 177 | 22 | 36 | 0,889 | 0,831 | 14 | 8 | 0 |
| 0,60 | 164 | 13 | 49 | 0,927 | 0,770 | 10 | 3 | 0 |
| 0,70 | 154 | 8 | 59 | 0,951 | 0,723 | 7 | 1 | 0 |
| 0,80 | 125 | 4 | 88 | 0,969 | 0,587 | 3 | 1 | 0 |
| 0,90 | 74 | 1 | 139 | 0,987 | 0,347 | 1 | 0 | 0 |

### Observações qualitativas

- **Nenhum falso positivo em cenas sem veículos** (300 imagens aleatórias): o modelo não "inventa" ônibus no vazio. Todos os erros acontecem perto de outros veículos.
- **O distrator é real:** nas imagens com carro e sem ônibus surgem falsos positivos com confiança alta. Os três mais confiantes foram:
  - `007507.jpg` (0,83): um **bonde** (VLT) em trilhos urbanos, veículo genuinamente parecido com ônibus.
  - `008035.jpg` (0,68): um veículo longo atrás de uma grade, que parece de fato um ônibus ou trem e não está anotado. Pode ser **ruído de anotação** do próprio dataset, e não erro do modelo.
  - `000271.jpg` (0,63): um **carro pequeno**, distante, em ângulo frontal. Este é um erro claro do modelo.
- Uma parte dos falsos positivos em imagens com ônibus vem de ônibus marcados como *difficult* (parcialmente ocultos), que excluímos do gabarito por convenção do VOC. Nesses casos, o modelo "acerta", mas o benchmark conta como erro.
- O recall cai rápido acima de $s_{\min} = 0{,}7$: ônibus pequenos, distantes ou parcialmente ocultos recebem confiança moderada.

### Limitações desta avaliação

- Fotos do Flickr de 2007, com ônibus majoritariamente europeus e ângulos variados. **Não representa o cenário de um ponto de ônibus brasileiro.** O resultado mede a capacidade geral do modelo, não o desempenho no ponto.
- A avaliação usa imagens isoladas. No sistema real, o ônibus aparece em vários quadros consecutivos, e a persistência temporal (Fase 6) deve reduzir ainda mais os falsos positivos.

### Decisão

- [x] **A linha de base é suficiente para seguir.** Com mAP50 de 0,93 e zero falsos positivos em cenas sem veículos, o detector genérico já localiza ônibus bem. O fine-tuning **não** se justifica com dados genéricos: o próximo ganho real depende de imagens do nosso domínio.
- **Ponto de operação provisório:** $s_{\min} = 0{,}6$ (precisão 0,93 e recall 0,77), coerente com o princípio de priorizar a precisão. Será reavaliado com dados reais.
- **Próximos passos:** coletar imagens de ônibus brasileiros vistos de frente (opção de fotos próprias ou dataset nacional) para medir o deslocamento de domínio e então decidir sobre o fine-tuning.

---

## Versão v1 — Fine-tuning (se aplicável)

_Preencher quando esta etapa ocorrer._
