"""
Full definition of a GPT Language Model, all of it in this single file.
References:
1) the official GPT-2 TensorFlow implementation released by OpenAI:
https://github.com/openai/gpt-2/blob/master/src/model.py
2) huggingface/transformers PyTorch implementation:
https://github.com/huggingface/transformers/blob/main/src/transformers/models/gpt2/modeling_gpt2.py
"""

import math
import inspect
from dataclasses import dataclass

import torch
import torch.nn as nn
from torch.nn import functional as F

# [Previous code...]
[Rest of the file content...]

# Add test code
if __name__ == '__main__':
    # Create a small test configuration
    config = GPTConfig(
        block_size=128,
        vocab_size=100,
        n_layer=4,
        n_head=4,
        n_embd=128,
        dropout=0.0,
        bias=True
    )
    
    # Create model
    model = GPT(config)
    print("Model created successfully!")
    
    # Create a small test input
    batch_size = 2
    seq_length = 16
    test_input = torch.randint(0, config.vocab_size, (batch_size, seq_length))
    
    # Run a forward pass
    logits, loss = model(test_input)
    print(f"\nTest forward pass successful!")
    print(f"Output shape: {logits.shape}")