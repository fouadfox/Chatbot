import torch
import transformers

print(torch.__version__)  # Check the installed version of PyTorch
print(transformers.__version__)  # Check the installed version of transformers

# from transformers.pipelines import PIPELINE_REGISTRY
# print(PIPELINE_REGISTRY.get_supported_tasks())



# import torch
# from sentence_transformers import SentenceTransformer

# print("Torch version:", torch.__version__)
# model = SentenceTransformer("all-MiniLM-L6-v2")
# print("SentenceTransformer loaded successfully!")

#<------------------------------------------------------------------------------>
# from transformers import pipeline

# chat_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")
# print("Pipeline setup successful!")
