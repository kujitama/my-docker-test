import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
import numpy as np


if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
        
checkpoint = "sam2/checkpoints/sam2.1_hiera_tiny.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_t.yaml"

predictor = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint, device=device), device=device)

def predict(image, point_coords):
    with torch.inference_mode(), torch.autocast(device.type, dtype=torch.bfloat16 if device.type == "cuda" else torch.float32):
        predictor.set_image(image)
        masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=[1] * len(point_coords), multimask_output=False)
        mask = masks[0].astype(np.bool)
    return mask