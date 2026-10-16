"""
Monta um conjunto de teste de detecção de ônibus a partir do PASCAL VOC 2007 (split de teste).

Saída no formato YOLO:
    <saida>/images/test/*.jpg
    <saida>/labels/test/*.txt   (uma linha por ônibus: "5 xc yc w h", normalizado)
    <saida>/voc_bus_test.yaml

Decisões (ver docs/resultados-treinamento-yolov8.md):
- Índice de classe 5 = 'bus' no COCO, para alinhar o gabarito com a saída do modelo pré-treinado.
- Objetos marcados como "difficult" no VOC são ignorados (convenção do benchmark VOC).
- Inclui imagens negativas: todas as imagens com carro e sem ônibus (distrator mais parecido)
  e uma amostra aleatória de imagens sem ônibus nem carro.

Uso:
    python tools/prepare_voc_bus.py --voc <pasta VOCdevkit/VOC2007> --saida datasets/processed/voc2007_bus
"""

import argparse
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

COCO_BUS_ID = 5

# Nomes das 80 classes do COCO, na ordem usada pelos pesos da Ultralytics.
COCO_NAMES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant",
    "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush",
]


def ler_anotacao(xml_path: Path):
    """Retorna (largura, altura, caixas_de_onibus, classes_presentes)."""
    raiz = ET.parse(xml_path).getroot()
    largura = float(raiz.find("size/width").text)
    altura = float(raiz.find("size/height").text)
    caixas, classes = [], set()
    for obj in raiz.iter("object"):
        nome = obj.find("name").text.strip()
        classes.add(nome)
        dificil = obj.find("difficult")
        if nome != "bus" or (dificil is not None and dificil.text.strip() == "1"):
            continue
        bb = obj.find("bndbox")
        xmin, ymin, xmax, ymax = (float(bb.find(k).text) for k in ("xmin", "ymin", "xmax", "ymax"))
        caixas.append((xmin, ymin, xmax, ymax))
    return largura, altura, caixas, classes


def para_yolo(caixa, largura, altura):
    """Converte (xmin, ymin, xmax, ymax) em pixels para (xc, yc, w, h) normalizados."""
    xmin, ymin, xmax, ymax = caixa
    xc = (xmin + xmax) / 2 / largura
    yc = (ymin + ymax) / 2 / altura
    w = (xmax - xmin) / largura
    h = (ymax - ymin) / altura
    return xc, yc, w, h


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--voc", required=True, type=Path, help="Pasta VOC2007 (contém Annotations/ e JPEGImages/)")
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--negativos-aleatorios", type=int, default=300)
    ap.add_argument("--semente", type=int, default=42)
    args = ap.parse_args()

    img_out = args.saida / "images" / "test"
    lbl_out = args.saida / "labels" / "test"
    img_out.mkdir(parents=True, exist_ok=True)
    lbl_out.mkdir(parents=True, exist_ok=True)

    com_onibus, com_carro, outros = [], [], []
    anotacoes = {}
    for xml_path in sorted((args.voc / "Annotations").glob("*.xml")):
        larg, alt, caixas, classes = ler_anotacao(xml_path)
        anotacoes[xml_path.stem] = (larg, alt, caixas)
        if "bus" in classes:
            com_onibus.append(xml_path.stem)
        elif "car" in classes:
            com_carro.append(xml_path.stem)
        else:
            outros.append(xml_path.stem)

    random.seed(args.semente)
    aleatorios = random.sample(outros, min(args.negativos_aleatorios, len(outros)))
    selecionadas = com_onibus + com_carro + aleatorios

    total_onibus = 0
    for stem in selecionadas:
        larg, alt, caixas = anotacoes[stem]
        shutil.copy(args.voc / "JPEGImages" / f"{stem}.jpg", img_out / f"{stem}.jpg")
        linhas = [f"{COCO_BUS_ID} " + " ".join(f"{v:.6f}" for v in para_yolo(c, larg, alt)) for c in caixas]
        (lbl_out / f"{stem}.txt").write_text("\n".join(linhas) + ("\n" if linhas else ""))
        total_onibus += len(caixas)

    yaml = args.saida / "voc_bus_test.yaml"
    nomes = "\n".join(f"  {i}: {n}" for i, n in enumerate(COCO_NAMES))
    yaml.write_text(f"path: {args.saida.resolve()}\ntrain: images/test\nval: images/test\ntest: images/test\nnames:\n{nomes}\n")

    print(f"Imagens com ônibus:            {len(com_onibus)}")
    print(f"Ônibus anotados (não difíceis): {total_onibus}")
    print(f"Negativos com carro:           {len(com_carro)}")
    print(f"Negativos aleatórios:          {len(aleatorios)}")
    print(f"Total de imagens:              {len(selecionadas)}")
    print(f"YAML: {yaml}")


if __name__ == "__main__":
    main()
