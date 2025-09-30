"""
Simple test script for students to test the trained model
"""
import os
import pickle
import torch
from model import GPTConfig, GPT

# Set device
device = 'cpu'  # Safe for all students
torch.manual_seed(1337)

# Load meta.pkl to understand the data encoding
meta_path = os.path.join('data', 'meta.pkl')
print(f"Looking for meta file at: {meta_path}")

if os.path.exists(meta_path):
    with open(meta_path, 'rb') as f:
        meta = pickle.load(f)
    # Get the mapping dictionaries
    stoi, itos = meta['stoi'], meta['itos']
    encode = lambda s: [stoi[c] for c in s]
    decode = lambda l: ''.join([itos[i] for i in l])
    vocab_size = len(itos)
    print(f"Found meta.pkl, vocabulary size: {vocab_size}")
else:
    print("No meta.pkl found")
    exit(1)

# Load the trained model
checkpoint_path = os.path.join('model_output', 'ckpt.pt')
print(f"Loading model from: {checkpoint_path}")

checkpoint = torch.load(checkpoint_path, map_location=device)
print("Checkpoint keys:", list(checkpoint.keys()))

# Extract configuration from checkpoint
model_args = checkpoint['model_args'] 
print("Model configuration:", model_args)

# Create model with the exact same config as training
gptconf = GPTConfig(**model_args)
model = GPT(gptconf)

# Load the model weights
state_dict = checkpoint['model']
model.load_state_dict(state_dict)
model.eval()
model.to(device)

print(f"Model loaded successfully. Parameters: {sum(p.numel() for p in model.parameters())/1e6:.2f}M")

# Generate some text
prompt = "ROMEO:"
context = encode(prompt)
x = torch.tensor(context, dtype=torch.long, device=device).unsqueeze(0)

print(f"\nPrompt: '{prompt}'")
print("Generated text:")
print("-" * 40)

# Generate
with torch.no_grad():
    for i in range(3):  # Generate 3 samples
        y = model.generate(x, max_new_tokens=100, temperature=0.8, top_k=200)
        generated_text = decode(y[0].tolist())
        print(f"Sample {i+1}:")
        print(generated_text)
        print("-" * 40)

print("\nModel test completed successfully!")