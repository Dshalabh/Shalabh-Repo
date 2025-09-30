import torch
from new_model import GPT, GPTConfig

def test_model():
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

if __name__ == '__main__':
    test_model()