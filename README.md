# Ponto de Ônibus Inteligente para Acessibilidade

> Dispositivo que identifica ônibus se aproximando de um ponto e anuncia a informação por áudio, combinando telemetria pública de transporte e visão computacional local — projetado para apoiar pessoas com deficiência visual.

[![Status](https://img.shields.io/badge/status-planejamento%20inicial-yellow)]()
[![Fase Atual](https://img.shields.io/badge/fase%20atual-treinamento%20YOLOv8-blue)]()
[![Licença](https://img.shields.io/badge/licença-MIT-green)]()

---

## Sobre o projeto

Pessoas com deficiência visual enfrentam uma barreira simples e recorrente: saber qual ônibus está chegando ao ponto, e se é o ônibus certo. Este projeto propõe um dispositivo instalado no próprio ponto, capaz de:

- Identificar veículos que se aproximam usando **telemetria pública** (GTFS estático, GTFS-RT ou API municipal) como sinal principal;
- Confirmar visualmente o veículo com uma **câmera local e visão computacional**, atuando também como alternativa quando os dados públicos estiverem indisponíveis;
- Anunciar a informação por **áudio (TTS)**, de forma clara, sem repetições e sem anúncios indevidos.

O desenvolvimento segue um plano de execução por fases, cada uma com objetivo, atividades, entregáveis e critério de passagem — evitando que o primeiro protótipo tente resolver tudo de uma vez. O plano completo está em [`docs/ROADMAP.md`](docs/ROADMAP.md).

**Princípio central:** o sucesso deste projeto não é medido pela quantidade de modelos de IA utilizados, mas pela confiabilidade do serviço prestado ao usuário final.

---

## Estado atual do projeto

🟡 **Planejamento inicial concluído → Iniciando Fase de dados visuais (adaptada)**

A primeira etapa prática escolhida foge levemente da ordem recomendada no roadmap original: em vez de partir direto para uma câmera ao vivo apontada para a rua, o projeto está começando pelo **treinamento de um modelo YOLOv8 de detecção de ônibus usando datasets já existentes**. A justificativa e o detalhamento dessa decisão estão documentados em [`docs/fase-atual-deteccao-onibus-yolov8.md`](docs/fase-atual-deteccao-onibus-yolov8.md).

Isso permite validar a viabilidade técnica da detecção visual **antes** de investir em coleta de vídeo própria, hardware de campo e autorizações de instalação.

---

## Arquitetura funcional

```
                 ┌──────────────────────────┐
                 │ GTFS estático / GTFS-RT  │
                 │ ou API municipal         │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Adaptador de telemetria  │
                 └────────────┬─────────────┘
                              │
                              ▼
┌──────────────┐    ┌──────────────────────────┐    ┌──────────────┐
│ Câmera local ├───►│ Motor de fusão e estados ├───►│ TTS / áudio  │
└──────┬───────┘    └────────────┬─────────────┘    └──────────────┘
       │                         │
       ▼                         ▼
┌──────────────┐    ┌──────────────────────────┐
│ Visão e OCR  │    │ Logs, métricas e saúde   │
└──────────────┘    └──────────────────────────┘
```

| Módulo | Responsabilidade |
|---|---|
| Configuração | Carrega ponto, linhas, sentido, limites e mensagens — sistema reproduzível sem alterar código |
| Adaptador de dados | Consulta e normaliza GTFS-RT ou API REST |
| Motor geográfico | Calcula distância, bearing, idade do feed e aproximação |
| Detecção visual | Localiza o ônibus na imagem (**YOLOv8** — fase atual) |
| Extração da ROI | Localiza e corrige a região do letreiro |
| Pré-processamento | Gera versões mais legíveis para o OCR |
| OCR | Extrai texto do letreiro em múltiplos frames |
| Casamento de padrão | Compara o texto com o catálogo local de linhas |
| Fusão | Combina telemetria e visão via máquina de estados |
| Áudio | Reproduz mensagem TTS, controla repetição |
| Observabilidade | Registra eventos, falhas e métricas |

Detalhes de cada módulo em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).

---

## Estrutura do repositório

```
ponto-onibus-inteligente/
├── docs/                    # Documentação técnica e de planejamento
├── config/                  # Configurações externas ao código (ponto, linhas, mensagens)
├── src/
│   ├── telemetry/           # Adaptador GTFS-RT / API municipal
│   ├── geo/                 # Motor geográfico (Haversine, bearing, aproximação)
│   ├── vision/               # Detecção do ônibus (YOLOv8) — em desenvolvimento
│   ├── ocr/                  # Reconhecimento do letreiro
│   ├── fusion/               # Máquina de estados e fusão de evidências
│   └── audio/                # TTS e controle de repetição
├── tests/                   # Testes automatizados
├── tools/                   # Scripts auxiliares (treino, avaliação, simulação)
├── datasets/
│   ├── raw/                  # Dados brutos (NÃO versionado — ver .gitignore)
│   ├── processed/            # Dados processados para treino/avaliação
│   └── annotations/           # Anotações (bounding boxes, labels)
├── models/                   # Pesos de modelos treinados (versionados via Git LFS ou release)
└── README.md
```

---

## Como começar (fase atual)

```bash
# Clonar o repositório
git clone https://github.com/Asafeol/ponto-inteligente.git
cd ponto-inteligente

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Ver o guia da fase atual (treinamento YOLOv8)
cat docs/fase-atual-deteccao-onibus-yolov8.md
```

Requisitos detalhados em [`requirements.txt`](requirements.txt).

---

## Roadmap

O plano completo de execução (11 fases, da preparação ao piloto controlado) está documentado em [`docs/ROADMAP.md`](docs/ROADMAP.md). Resumo das próximas etapas imediatas:

- [x] Fase 0 — Planejamento, escopo e critérios de sucesso
- [ ] **Fase 3/4 (adaptada) — Treinamento inicial de detecção YOLOv8 com dataset** ⬅ *em andamento*
- [ ] Fase 1 — Levantamento da fonte de transporte (GTFS-RT / API municipal)
- [ ] Fase 2 — Protótipo do motor geográfico
- [ ] Fase 5 — OCR e casamento com catálogo local
- [ ] Fase 6 — Máquina de estados e fusão de evidências
- [ ] Fase 7 — Áudio, usabilidade e acessibilidade
- [ ] Fase 8 — Integração em hardware e operação degradada
- [ ] Fase 9 — Piloto controlado

## Princípios de projeto

| Princípio | Aplicação prática |
|---|---|
| Privacidade por padrão | Processar frames localmente; não armazenar rostos ou placas como parte do funcionamento normal |
| Falha segura | Na dúvida, não anunciar uma linha específica |
| Sensores complementares | Telemetria e câmera se confirmam ou se substituem parcialmente |
| Observabilidade | Registrar decisões, idade dos dados, confiança e falhas |
| Escopo incremental | Validar um ponto e poucas linhas antes de ampliar |
| Operação offline parcial | Visão, regras locais e áudio funcionam sem internet |
| Configuração externa ao código | Ponto, linhas, raios e mensagens em arquivos de configuração |

## Contribuindo

Consulte [`CONTRIBUTING.md`](CONTRIBUTING.md) para o fluxo de commits, branches e critérios de revisão.

## Licença

Este projeto está licenciado sob os termos da licença MIT — veja [`LICENSE`](LICENSE) para detalhes.

---

<p align="center"><i>Projeto de acessibilidade desenvolvido de forma independente — em fase de planejamento e prototipagem.</i></p>
