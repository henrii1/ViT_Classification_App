#import moudules
import gradio as gr
import os
import torch

from model import create_vit_model1
from timeit import default_timer as timer
from typing import Tuple, Dict

#setup class names
class_names = ["pizza", "steak", "sushi", "Tacos"]

#model and transform preparation

#create model
vit, vit_transforms1 = create_vit_model1(num_classes = 4)

#load saved weights
vit.load_state_dict(torch.load(f= 'models/pretrained_vit_feature_extractor_pizza_steak_sushi_tacos_20_percent.pth',
                                map_location = torch.device("cpu") )

)

#predict function
def predict(img) -> Tuple[Dict, float]:
  """Transforms and performs a prediction on img and returns prediction and time taken.
  """
  # start the timer
  start_time = timer()

  #Transform the target image and add a batch dimension
  img = vit_transforms1(img).unsqueeze(0)

  #put model into evaluation mode and turn on inference model
  vit.eval()
  with torch.inference_mode():
    #pass the transformed image throug the model and turn prediction to probabilites
    pred_probs = torch.softmax(vit(img), dim = 1)

  #create a prediction label and prediction probability dic for each class, as required by gradio
  pred_labels_and_probs = {class_names[i]: float(pred_probs[0][i] ) for i in range(len(class_names))}

  #Calculate the prediction time
  pred_time = round(timer() - start_time, 5)

  return pred_labels_and_probs, pred_time



#Gradio App

#create title, description and article strings

title = "FoodClassifier Mini"
description = "A ViT feature extractor computer vision model to classify images of food as pizza, steak, sushi or Tacos"
article = created by [Emerald Henry](https://henrii1.github.io)

example_list = [["examples/" + example] for example in os.listdir("examples")]

#create the gradio demo

demo = gr. Interface(fn= predict, 
                      inputs = gr.Image(type = "pil,
                      outpus = [gr.Label(num_top_classes = 4, label='Preciction,
                                gr.Number(label = "Prediction time (s,
                      examples = example_list,
                      title = title,
                      description = description,
                      article = article)
demo.launch()
