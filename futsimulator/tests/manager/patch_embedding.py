import torch
import torch.nn as nn
import torchvision.transforms as transforms

class ImagePatchEmbedding(nn.Module):
    def __init__(self, image_size, patch_size, in_channels, embed_dim):
        super(ImagePatchEmbedding, self).__init__()
        self.image_size = image_size
        self.patch_size = patch_size
        self.in_channels = in_channels
        self.embed_dim = embed_dim
        
        num_patches = (image_size // patch_size) ** 2
        self.patch_embedding = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.positional_embedding = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
        
    def forward(self, x):
        # x: (batch_size, in_channels, image_size, image_size)
        patches = self.patch_embedding(x)  # (batch_size, embed_dim, num_patches_h, num_patches_w)
        patches = patches.permute(0, 2, 3, 1)  # (batch_size, num_patches_h, num_patches_w, embed_dim)
        
        batch_size, num_patches_h, num_patches_w, _ = patches.shape
        patches = patches.view(batch_size, -1, self.embed_dim)  # (batch_size, num_patches, embed_dim)
        
        # Add positional embedding
        positional_embedding = self.positional_embedding[:, :num_patches_h * num_patches_w, :]  # (1, num_patches, embed_dim)
        patches = patches + positional_embedding
        
        return patches

# Example usage:
image_size = 224  # Assuming square images
patch_size = 16
in_channels = 3  # For RGB images
embed_dim = 256
batch_size = 4

# Sample image tensor (batch_size, in_channels, image_size, image_size)
sample_image = torch.randn(batch_size, in_channels, image_size, image_size)

# Initialize ImagePatchEmbedding module
patch_embed = ImagePatchEmbedding(image_size, patch_size, in_channels, embed_dim)

# Obtain patch embeddings
patch_embeddings = patch_embed(sample_image)
print("Shape of patch embeddings:", patch_embeddings.shape)
