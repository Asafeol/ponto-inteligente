# Arquitetura Funcional

## Visão geral

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

## Módulos principais

| Módulo | Responsabilidade | Resultado esperado |
|---|---|---|
| Configuração | Carregar ponto, linhas, sentido, limites e mensagens | Sistema reproduzível e ajustável sem alterar código |
| Adaptador de dados | Consultar e normalizar GTFS-RT ou API REST | Objetos internos com veículo, linha, posição, direção e timestamp |
| Motor geográfico | Calcular distância, bearing, idade do feed e aproximação | Candidato classificado como relevante ou não relevante |
| Detecção visual | Localizar ônibus na imagem | Bounding box e confiança da detecção |
| Extração da ROI | Localizar e corrigir a região do letreiro | Recorte alinhado do letreiro frontal |
| Pré-processamento | Criar versões adequadas para OCR | Imagens com contraste e caracteres mais legíveis |
| OCR | Extrair texto em múltiplos frames e configurações | Texto bruto e confiança por tentativa |
| Casamento de padrão | Comparar o texto com o catálogo local | Linha ou destino provável e pontuação de correspondência |
| Fusão | Combinar evidências e aplicar máquina de estados | Decisão de anunciar, aguardar ou descartar |
| Áudio | Reproduzir mensagem e controlar repetição | Aviso compreensível, único e rastreável |
| Observabilidade | Registrar eventos, falhas e métricas | Diagnóstico e avaliação objetiva do sistema |

## Máquina de estados (Fase 6)

```
IDLE → VEÍCULO_CANDIDATO → APROXIMANDO → CONFIRMADO → ANUNCIADO → AGUARDANDO_SAÍDA → IDLE
```

Transições determinadas por: distância, direção, idade do feed, confiança visual, persistência temporal e cooldown. Telemetria, detecção visual e OCR recebem pesos separados na decisão final.

## Configuração externa ao código

A configuração deve conter, no mínimo:

- Identificador do ponto
- Raio de alerta
- Tolerância angular
- Idade máxima do feed
- Tempo de cooldown
- Linhas válidas
- Mensagens de áudio por linha

Todos os valores devem ser ajustáveis sem recompilar o sistema — ver `config/exemplo-ponto.yaml`.
