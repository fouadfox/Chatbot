from transformers import pipeline

print("Testing Transformers pipeline...")
pipe = pipeline("text-generation", model="gpt2")
print("Pipeline loaded successfully!")

output = pipe("Hello, world!", max_length=10)
print("Generated text:", output)
