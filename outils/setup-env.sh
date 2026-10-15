#!/usr/bin/env bash
# Installe l'environnement Python nécessaire aux outils du projet (lettrage, détourage, assemblage).
# Idempotent : à relancer si l'environnement du bac à sable a été réinitialisé.
set -euo pipefail
PIP="pip install --quiet --break-system-packages"
# Pillow + NumPy < 2 (contrainte MediaPipe 0.10.x) + OpenCV headless (sans libGL)
$PIP "numpy<2" pillow "opencv-contrib-python-headless<4.13"
# MediaPipe 0.10.21 : embarque ses modèles (segmentation personne, détection et maillage du visage)
# --no-deps pour éviter l'OpenCV non-headless ; dépendances utiles installées à la main.
$PIP --no-deps "mediapipe==0.10.21"
$PIP absl-py attrs flatbuffers "protobuf>=4.25.3,<5" sentencepiece matplotlib
python3 - <<'EOF'
import numpy, PIL, cv2, mediapipe as mp
print("numpy", numpy.__version__, "| pillow", PIL.__version__, "| cv2", cv2.__version__, "| mediapipe", mp.__version__)
print("segmentation :", mp.solutions.selfie_segmentation.SelfieSegmentation)
print("face mesh    :", mp.solutions.face_mesh.FaceMesh)
EOF
