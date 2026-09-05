from pathlib import Path


ROOT = Path("data/processed/rgb_defects")
VALID_CLASSES = {0, 1, 2, 3}

total_files = 0
total_lines = 0
errors = []

for label_file in ROOT.rglob("labels/*.txt"):
    total_files += 1

    for line_number, line in enumerate(
        label_file.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        total_lines += 1
        values = line.split()

        try:
            class_id = int(values[0])
            coordinates = [float(value) for value in values[1:]]
        except ValueError:
            errors.append(
                f"{label_file}:{line_number} invalid numeric value"
            )
            continue

        if class_id not in VALID_CLASSES:
            errors.append(
                f"{label_file}:{line_number} invalid class ID {class_id}"
            )

        if len(coordinates) < 6 or len(coordinates) % 2 != 0:
            errors.append(
                f"{label_file}:{line_number} invalid polygon coordinate count"
            )

        if any(value < 0 or value > 1 for value in coordinates):
            errors.append(
                f"{label_file}:{line_number} coordinate outside [0, 1]"
            )


print(f"Label files checked: {total_files}")
print(f"Annotation lines checked: {total_lines}")
print(f"Errors: {len(errors)}")

if errors:
    print("\nFirst 20 errors:")
    for error in errors[:20]:
        print(error)
else:
    print("YOLO segmentation labels: VALID")