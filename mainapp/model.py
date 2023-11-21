import torch
import torchvision

from torch import nn

def create_vit_model1(num_classes: int = 4,
                      seed: int =42)
  """Creates an ViT feature extractor model and transforms.

  Args:
        num_classes (int, optional): number of classes in the classifier head. 
            Defaults to 4.
        seed (int, optional): random seed value. Defaults to 42.

  Returns:
        model (torch.nn.Module): ViT feature extractor model. 
        transforms (torchvision.transforms): ViT image transforms.
  """ 
  #create vit pretrained weights and transforms and model
  weights =torchvision.models.ViT_B_16_Weights.DEFAULT
  transforms = weights.transforms()
  model = torchvision.models.vit_b_16(weights = weights)

  # Freeze all layers in base model
  for param in model.parameters():
      param.requires_grad = False

  #Change classifier head with random seed for reproducibility
  torch.manual_seed(seed)
  model.classifier = nn.Sequential(nn.Dropout(p=0.3, inplace = True),
                                    nn.Linear(in_features = 1408, out_features = num_classes))
  return model, transforms
