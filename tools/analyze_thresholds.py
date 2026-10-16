"""
Análise complementar à avaliação do YOLO: precisão, recall e origem dos falsos positivos
em função do limiar de confiança s_min, com casamento por IoU >= 0,5.

Classifica cada imagem em: 'onibus' (tem ônibus anotado), 'carro' (negativo com carro) ou 'outro'.
A categoria vem do arquivo de anotação VOC original.

Uso:
    python tools/analyze_thresholds.py --weights yolov8n.pt --dados <pasta voc2007_bus> --voc <pasta VOC2007>
"""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from ultralytics import YOLO

BUS = 5
LIMIARES = [0.25, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]


def iou(a, b):
    """IoU entre caixas (x1, y1, x2, y2)."""
    ix1, iy1, ix2, iy2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter)


def categoria(voc: Path, stem: str) -> str:
    nomes = {o.find("name").text.strip() for o in ET.parse(voc / "Annotations" / f"{stem}.xml").getroot().iter("object")}
    return "onibus" if "bus" in nomes else ("carro" if "car" in nomes else "outro")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--dados", required=True, type=Path)
    ap.add_argument("--voc", required=True, type=Path)
    ap.add_argument("--saida", type=Path, default=Path("analise_limiares.json"))
    args = ap.parse_args()

    modelo = YOLO(args.weights)
    imagens = sorted((args.dados / "images" / "test").glob("*.jpg"))

    registros = []  # (confiança, é_VP, categoria, stem)
    total_gt = 0
    for caminho in imagens:  # uma imagem por vez: evita carregar o conjunto inteiro na memória
        res = modelo.predict(str(caminho), conf=min(LIMIARES), classes=[BUS], verbose=False)[0]
        stem = Path(res.path).stem
        h, w = res.orig_shape
        gts = []
        for linha in (args.dados / "labels" / "test" / f"{stem}.txt").read_text().splitlines():
            _, xc, yc, bw, bh = map(float, linha.split())
            gts.append(((xc - bw / 2) * w, (yc - bh / 2) * h, (xc + bw / 2) * w, (yc + bh / 2) * h))
        total_gt += len(gts)
        cat = categoria(args.voc, stem)
        usados = set()
        ordem = sorted(zip(res.boxes.conf.tolist(), res.boxes.xyxy.tolist()), key=lambda t: -t[0])
        for conf, caixa in ordem:  # casamento guloso por confiança decrescente
            melhor, idx = 0.0, None
            for i, g in enumerate(gts):
                if i not in usados and (v := iou(caixa, g)) > melhor:
                    melhor, idx = v, i
            vp = melhor >= 0.5
            if vp:
                usados.add(idx)
            registros.append((conf, vp, cat, stem))

    tabela = []
    for s in LIMIARES:
        sel = [r for r in registros if r[0] >= s]
        vp = sum(r[1] for r in sel)
        fp = len(sel) - vp
        fp_cat = {c: sum(1 for r in sel if not r[1] and r[2] == c) for c in ("onibus", "carro", "outro")}
        fn = total_gt - vp
        tabela.append({
            "limiar": s, "VP": vp, "FP": fp, "FN": fn,
            "precisao": round(vp / (vp + fp), 4) if vp + fp else None,
            "recall": round(vp / total_gt, 4),
            "FP_em_imagens_com_onibus": fp_cat["onibus"],
            "FP_em_imagens_com_carro": fp_cat["carro"],
            "FP_em_outras": fp_cat["outro"],
        })

    print(f"Ônibus anotados (GT): {total_gt}\n")
    print(f"{'s_min':>6} {'VP':>4} {'FP':>4} {'FN':>4} {'Precisão':>9} {'Recall':>7} | FP: c/ônibus c/carro outras")
    for t in tabela:
        print(f"{t['limiar']:>6.2f} {t['VP']:>4} {t['FP']:>4} {t['FN']:>4} {t['precisao']:>9} {t['recall']:>7} |"
              f" {t['FP_em_imagens_com_onibus']:>9} {t['FP_em_imagens_com_carro']:>7} {t['FP_em_outras']:>6}")

    fps = sorted([r for r in registros if not r[1] and r[2] != "onibus"], key=lambda r: -r[0])[:6]
    args.saida.write_text(json.dumps({"tabela": tabela, "piores_fp_negativos": [{"conf": round(c, 3), "categoria": cat, "imagem": st} for c, _, cat, st in fps]}, indent=2, ensure_ascii=False))
    print("\nFalsos positivos mais confiantes em imagens SEM ônibus:")
    for c, _, cat, st in fps:
        print(f"  {st}.jpg  conf={c:.2f}  ({cat})")


if __name__ == "__main__":
    main()
