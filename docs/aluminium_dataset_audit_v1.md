# Aluminium Defect Detection — Dataset Audit v1

Source: Roboflow Universe — Aluminium Defect Detection
Task: Instance Segmentation
Total images: 480
Train: 335 images, 836 annotations
Validation: 95 images, 235 annotations
Test: 50 images, 122 annotations
Image size: 640x640

Classes:
- scratch
- Black Marker
- Corner Defect
- Side Defect

Notes:
- The COCO files define an additional "Alumunium" category, but it has no annotations.
- All 480 images contain at least one annotation.
- Multiple classes can occur in the same image.
- Multiple scratch and Black Marker instances can occur in one image.
- Training bounding boxes checked: 0 invalid.
- Training segmentation polygons checked: 0 malformed/out-of-bounds.
- Training duplicate annotations checked: 0.
- Black Marker is retained as a separate source label and is not merged with scratch.
- No assumption is made that all four classes represent naturally occurring physical defects.
