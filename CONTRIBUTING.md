# Contribuindo com o Projeto

Este é um projeto de acessibilidade em fase de prototipagem. As diretrizes abaixo existem para manter o histórico rastreável e as decisões documentadas — mesmo em um projeto de autoria individual, isso facilita retomar o trabalho depois de um tempo parado.

## Fluxo de trabalho

1. **Toda mudança relevante parte de uma hipótese.** Antes de implementar, registre em uma issue ou no início do commit: o que você espera que aconteça e como vai testar.
2. **Branches por fase ou funcionalidade.** Ex: `fase-atual/treino-yolov8`, `feature/motor-geografico`, `fix/bearing-normalizacao`.
3. **Commits pequenos e descritivos.** Prefira várias mudanças pequenas e testáveis a uma única mudança grande.
4. **Toda mudança de modelo ou dataset deve ser registrada** em `docs/DATASETS.md` ou `docs/resultados-treinamento-yolov8.md`, conforme o caso.

## Padrão de commits

```
tipo(escopo): descrição curta no imperativo

Corpo explicando o quê e o porquê, se necessário.
```

Tipos sugeridos: `feat`, `fix`, `docs`, `test`, `refactor`, `data`, `model`.

Exemplos:
```
feat(vision): adiciona script de treino YOLOv8 com dataset COCO
docs(datasets): registra licença do dataset BDD100K
data(annotations): adiciona anotações de bounding box para lote 3
```

## Antes de abrir um Pull Request (ou finalizar uma etapa, se solo)

- [ ] O critério de passagem da fase está documentado e satisfeito (ver `docs/ROADMAP.md`)
- [ ] Nenhum dado sensível ou bruto foi versionado (`datasets/raw/` deve estar vazio no Git)
- [ ] Testes relevantes foram executados (`pytest tests/`)
- [ ] A documentação afetada foi atualizada (README, ROADMAP ou documento da fase)

## Dados e privacidade

Nunca versionar vídeos, imagens brutas com pessoas identificáveis, placas de veículos ou qualquer dado que não seja estritamente necessário ao treinamento/avaliação. Ver princípio de "Privacidade por padrão" no README.
