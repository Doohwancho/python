import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def compress_image_with_svd(image_path, k):
    """
    Compress image using SVD by keeping only top k singular values
    """
    # Read image and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=np.float64)  # Convert to float64
    
    # Perform SVD
    U, singular_values, Vt = np.linalg.svd(img_array)
    
    # Reconstruct image using only k components
    compressed_img = np.zeros_like(img_array, dtype=np.float64)  # Use float64
    for i in range(k):
        compressed_img += singular_values[i] * np.outer(U[:, i], Vt[i, :])
    
    # Clip values to valid range and convert back to uint8
    compressed_img = np.clip(compressed_img, 0, 255).astype(np.uint8)
    
    # Calculate compression ratio
    original_size = img_array.shape[0] * img_array.shape[1]
    compressed_size = k * (img_array.shape[0] + img_array.shape[1] + 1)
    compression_ratio = original_size / compressed_size
    
    # Calculate error
    error = np.sum((img_array - compressed_img) ** 2)
    
    return compressed_img, compression_ratio, error, singular_values



def compress_color_image_with_svd(image_path, k):
    """
    Compress color image using SVD
    """
    # Read color image
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Process each color channel separately
    compressed_channels = []
    
    for channel in range(3):
        # Extract channel
        channel_data = img_array[:, :, channel]
        
        # Perform SVD
        U, s, Vt = np.linalg.svd(channel_data)
        
        # Reconstruct using k components
        compressed_channel = np.zeros_like(channel_data)
        for i in range(k):
            compressed_channel += s[i] * np.outer(U[:, i], Vt[i, :])
            
        compressed_channels.append(compressed_channel)
    
    # Combine channels
    compressed_img = np.stack(compressed_channels, axis=2)
    
    # Ensure values are in valid range
    compressed_img = np.clip(compressed_img, 0, 255).astype(np.uint8)
    
    # Calculate compression ratio
    original_size = img_array.shape[0] * img_array.shape[1] * 3
    compressed_size = k * (img_array.shape[0] + img_array.shape[1] + 1) * 3
    compression_ratio = original_size / compressed_size
    
    return compressed_img, compression_ratio

# Example usage for color images
def demonstrate_color_compression():
    image_path = "color_example.jpg"
    k_values = [5, 20, 50, 100]
    
    plt.figure(figsize=(15, 10))
    
    # Original image
    plt.subplot(2, 2, 1)
    original_img = Image.open(image_path)
    plt.imshow(original_img)
    plt.title('Original')
    
    # Compressed images
    for idx, k in enumerate(k_values[:3]):
        compressed, ratio = compress_color_image_with_svd(image_path, k)
        
        plt.subplot(2, 2, idx + 2)
        plt.imshow(compressed)
        plt.title(f'k={k}\nCompression Ratio: {ratio:.2f}x')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load an example image
    image_path = "example.jpg"  # Make sure this file exists
    
    # Try different compression levels
    k_values = [5, 20, 50, 100]
    
    # Create subplot
    plt.figure(figsize=(15, 10))
    
    # Original image
    plt.subplot(2, 3, 1)
    original_img = Image.open(image_path).convert('L')
    plt.imshow(original_img, cmap='gray')
    plt.title('Original')
    
    # Plot compressed images
    for idx, k in enumerate(k_values):
        compressed, ratio, error, singular_values = compress_image_with_svd(image_path, k)
        
        plt.subplot(2, 3, idx + 2)
        plt.imshow(compressed, cmap='gray')
        plt.title(f'k={k}\nCompression Ratio: {ratio:.2f}x\nError: {error:.2e}')
    
    # Plot singular values
    plt.subplot(2, 3, 6)
    plt.semilogy(singular_values[:100])
    plt.title('First 100 Singular Values')
    plt.xlabel('Index')
    plt.ylabel('Singular Value (log scale)')
    
    plt.tight_layout()
    plt.show()