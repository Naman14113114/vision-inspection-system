import json
import shutil
from pathlib import Path


CLASS_MAP = {
    "scratch": 0,
    "Black Marker": 1,
    "Corner Defect": 2,
    "Side Defect": 3,
}


def convert_split(source_root: Path, output_root: Path, split: str) -> None:
    split_source = source_root / split
    annotation_file = split_source / "_annotations.coco.json"

    with annotation_file.open("r", encoding="utf-8") as f:
        coco = json.load(f)

    categories = {
        category["id"]: category["name"]
        for category in coco["categories"]
    }

    images = {
        image["id"]: image
        for image in coco["images"]
    }

    annotations_by_image = {}
    for annotation in coco["annotations"]:
        annotations_by_image.setdefault(
            annotation["image_id"], []
        ).append(annotation)

    output_images = output_root / split / "images"
    output_labels = output_root / split / "labels"

    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    converted_annotations = 0

    for image_id, image_info in images.items():
        filename = image_info["file_name"]
        width = image_info["width"]
        height = image_info["height"]

        source_image = split_source / filename

        if not source_image.exists():
            raise FileNotFoundError(
                f"Image referenced by COCO file does not exist: {source_image}"
            )

        shutil.copy2(
            source_image,
            output_images / filename,
        )

        label_file = output_labels / f"{Path(filename).stem}.txt"

        lines = []

        for annotation in annotations_by_image.get(image_id, []):
            category_name = categories[annotation["category_id"]]

            # Ignore the unused COCO "Alumunium" category.
            if category_name not in CLASS_MAP:
                continue

            segmentation = annotation.get("segmentation")

            if (
                not isinstance(segmentation, list)
                or not segmentation
                or not isinstance(segmentation[0], list)
            ):
                raise ValueError(
                    f"Invalid polygon segmentation in "
                    f"{split}/{filename}"
                )

            # COCO polygons are stored as:
            # [x1, y1, x2, y2, ...]
            polygon = segmentation[0]

            if len(polygon) < 6 or len(polygon) % 2 != 0:
                raise ValueError(
                    f"Invalid polygon coordinate count in "
                    f"{split}/{filename}"
                )

            normalized = []

            for index, coordinate in enumerate(polygon):
                if index % 2 == 0:
                    normalized.append(coordinate / width)
                else:
                    normalized.append(coordinate / height)

            class_id = CLASS_MAP[category_name]

            line = " ".join(
                [str(class_id)]
                + [f"{value:.6f}" for value in normalized]
            )

            lines.append(line)
            converted_annotations += 1

        label_file.write_text(
            "\n".join(lines) + ("\n" if lines else ""),
            encoding="utf-8",
        )

    print(
        f"{split}: {len(images)} images, "
        f"{converted_annotations} annotations converted"
    )


def main():
    project_root = Path(__file__).resolve().parents[2]

    source_root = (
        project_root
        / "data"
        / "raw"
        / "aluminium_defects"
    )

    output_root = (
        project_root
        / "data"
        / "processed"
        / "rgb_defects"
    )

    for split in ("train", "valid", "test"):
        convert_split(
            source_root,
            output_root,
            split,
        )

    print("COCO → YOLO segmentation conversion complete.")
    print(f"Output: {output_root}")


if __name__ == "__main__":
    main()