"""
Script de treino/fine-tuning do YOLOv8 para detecção de ônibus.

Uso:
    python tools/train_yolov8.py --data config/dataset.yaml --epochs 50 --model yolov8n.pt

Ver docs/fase-atual-deteccao-onibus-yolov8.md para o contexto completo desta etapa.
"""

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Treino/fine-tuning YOLOv8 para detecção de ônibus")
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Caminho para o arquivo YAML do dataset (formato Ultralytics)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="Pesos iniciais: 'yolov8n.pt' (pré-treinado COCO) ou caminho para checkpoint próprio",
    )
    parser.add_argument("--epochs", type=int, default=50, help="Número de épocas de treino")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamanho da imagem de entrada")
    parser.add_argument("--batch", type=int, default=16, help="Tamanho do batch")
    parser.add_argument(
        "--project",
        type=str,
        default="runs/detect",
        help="Diretório de saída dos resultados (não versionado — ver .gitignore)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="bus-detector",
        help="Nome do experimento",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(
            f"Arquivo de dataset não encontrado: {data_path}. "
            "Registre a origem do dataset em docs/DATASETS.md antes de treinar."
        )

    model = YOLO(args.model)

    results = model.train(
        data=str(data_path),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
    )

    print(f"\nTreino concluído. Resultados em: {args.project}/{args.name}")
    print("Próximo passo: rode tools/evaluate_yolov8.py e documente em docs/resultados-treinamento-yolov8.md")


if __name__ == "__main__":
    main()
