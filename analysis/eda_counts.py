from pathlib import Path
import csv
import sys
import os

# GUI 없는 환경에서도 렌더링 가능하도록
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def find_root(data_base: Path) -> Path:
    """
    Kaggle 'chest-xray-pneumonia' 구조는 보통
    data/chest-xray/chest_xray/{train,val,test}/NORMAL,PNEUMONIA
    형태입니다. 최상위 'chest_xray' 폴더 유무를 감지합니다.
    """
    direct = data_base / "train"
    nested = data_base / "chest_xray" / "train"
    if direct.exists():
        return data_base
    if nested.exists():
        return data_base / "chest_xray"
    raise RuntimeError("train/val/test 디렉터리를 찾을 수 없습니다.")

def count_images(split_dir: Path):
    counts = {}
    if not split_dir.exists():
        return counts
    for label_dir in split_dir.iterdir():
        if label_dir.is_dir():
            c = sum(1 for p in label_dir.glob("*") if p.is_file())
            counts[label_dir.name] = c
    return counts

def main():
    repo_root = Path(__file__).resolve().parents[1]
    data_base = repo_root / "analysis" / "data" / "chest-xray"
    out_dir = repo_root / "analysis" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    root = find_root(data_base)
    results = []  # rows: split,label,count

    for split in ["train", "val", "test"]:
        split_dir = root / split
        split_counts = count_images(split_dir)
        for label, count in split_counts.items():
            results.append((split, label, count))

    # CSV 저장
    csv_path = out_dir / "counts.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["split", "label", "count"])
        wr.writerows(results)

    # 시각화 (split 별 label 분포)
    # 데이터를 {split: {label: count}}로 재구성
    splits = ["train", "val", "test"]
    labels = sorted({r[1] for r in results})
    data_map = {s: {l: 0 for l in labels} for s in splits}
    for s, l, c in results:
        data_map[s][l] = c

    # 막대그래프
    fig = plt.figure(figsize=(8, 5))
    x = range(len(splits))
    width = 0.35

    # 두 라벨만 존재한다는 가정(NORMAL, PNEUMONIA). 라벨 수가 달라도 동작 가능.
    for idx, label in enumerate(labels):
        y = [data_map[s][label] for s in splits]
        plt.bar([i + idx*width for i in x], y, width=width, label=label)

    plt.xticks([i + width/2 for i in x], splits)
    plt.ylabel("count")
    plt.title("Chest X-ray label distribution by split")
    plt.legend()
    plt.tight_layout()

    fig_path = out_dir / "label_distribution.png"
    plt.savefig(fig_path, dpi=150)

    print(f"[OK] Wrote: {csv_path}")
    print(f"[OK] Wrote: {fig_path}")

if __name__ == "__main__":
    main()