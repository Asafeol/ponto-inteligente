"""
Script de avaliação do modelo YOLOv8 de detecção de ônibus.

Uso:
    python tools/evaluate_yolov8.py --weights models/bus-detector-v0.pt --data config/dataset.yaml

Gera métricas (mAP, precisão, recall) sobre o conjunto de teste definido no dataset.
Ver docs/fase-atual-deteccao-onibus-yolov8.md, seção 5-7, para os critérios de passagem.
"""

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Avaliação do modelo YOLOv8 de detecção de ônibus")
    parser.add_argument(
        "--weights",
        type=str,
        required=True,
        help="Caminho para os pesos treinados (.pt)",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Caminho para o arquivo YAML do dataset",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Tamanho da imagem de entrada")
    parser.add_argument(
        "--split",
        type=str,
        default="test",
        choices=["val", "test"],
        help="Qual split do dataset avaliar",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    weights_path = Path(args.weights)
    if not weights_path.exists():
        raise FileNotFoundError(f"Pesos não encontrados: {weights_path}")

    model = YOLO(str(weights_path))

    metrics = model.val(data=args.data, imgsz=args.imgsz, split=args.split)

    print("\n--- Resumo das métricas ---")
    print(f"mAP50:    {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Precisão: {metrics.box.mp:.4f}")
    print(f"Recall:   {metrics.box.mr:.4f}")
    print(
        "\nLembre-se de registrar esses valores, exemplos de acerto/erro e condições de falha "
        "em docs/resultados-treinamento-yolov8.md antes de avançar de fase."
    )


if __name__ == "__main__":
    main()
