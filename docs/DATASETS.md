# Registro de Datasets

Todo dataset usado no projeto — público ou coletado internamente — deve ser registrado aqui antes de ser baixado ou versionado, com sua origem e licença de uso.

## Datasets em avaliação (Fase atual — detecção YOLOv8)

| Dataset | Origem | Licença | Classes usadas | Status |
|---|---|---|---|---|
| PASCAL VOC 2007 (split de teste) | http://host.robots.ox.ac.uk/pascal/VOC/voc2007/ (cópia da Ultralytics no GitHub) | Imagens do Flickr: uso para pesquisa e avaliação; não redistribuir | `bus` (+ negativos com `car`) | ✅ Usado na linha de base v0 (16/10/2026) |
| COCO (pesos pré-treinados Ultralytics) | https://cocodataset.org | CC BY 4.0 (anotações) | `bus` | ✅ Origem dos pesos `yolov8n.pt`; não usado como teste, para evitar vazamento de dados |
| Roboflow Universe — "bus detection" | https://universe.roboflow.com | Variável por dataset — conferir individualmente | `bus` | ⬜ A avaliar |
| BDD100K | https://bdd-data.berkeley.edu | BDD100K License (uso não comercial/pesquisa) | `bus` | ⬜ A avaliar |
| Open Images Dataset (classe Bus) | https://storage.googleapis.com/openimages | CC BY 4.0 | `Bus` | ⬜ A avaliar |
| Vídeos autorizados próprios | A definir (Fase 3 completa) | Uso interno — ver protocolo de coleta | `bus`, letreiro | ⬜ Futuro |

## Critérios de seleção

- Licença compatível com o uso pretendido do projeto (verificar antes de treinar, não depois)
- Diversidade de ângulos, distâncias e condições de iluminação
- Presença de ônibus urbanos (não apenas ônibus escolares ou rodoviários, dependendo do contexto do MVP)
- Volume suficiente para fine-tuning sem overfitting

## Divisão treino / validação / teste

Ao consolidar o dataset final para treino, documentar aqui:

- Proporção usada (ex: 70/20/10)
- Critério de divisão (aleatório, por vídeo de origem, por condição ambiental)
- Garantia de que não há vazamento de frames quase idênticos entre os conjuntos

## Dados brutos — política de versionamento

`datasets/raw/` **não deve ser versionado** no Git (ver `.gitignore`). Apenas `datasets/annotations/` e amostras pequenas de referência podem ser versionadas diretamente; datasets grandes devem ser referenciados por link de download ou Git LFS/DVC.
