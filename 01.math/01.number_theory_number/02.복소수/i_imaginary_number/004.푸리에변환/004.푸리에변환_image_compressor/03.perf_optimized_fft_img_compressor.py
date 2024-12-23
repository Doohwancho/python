import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


# process

# Original JPEG (3MB)
#   ↓ [Convert to raw pixels]
# Raw Image Data (3MB)
#   ↓ [FFT Transform → Complex Numbers]
# Complex FFT Data (48MB)
#   ↓ [Keep only 2.66% of coefficients]
# Compressed FFT Data (10MB)
#   ↓ [Save as NPZ]
# Compressed NPZ File (10MB)
#   ↓ [Decompress and reconstruct]
# Reconstructed Image (3MB)
#   ↓ [Save as JPEG]
# Final JPEG (2.1MB)


# Q. why compressed .npz larger than original picture size?
# A. Even keeping only 2.66% of coefficients still results in large files due to complex number size


# console.log

# Compressing with ratio: 0.05
# Files saved in output:
# 1. Compressed FFT data: output/moon_compressed_0.05.npz
# 2. Reconstructed image: output/moon_reconstructed_0.05.png
# 3. Visualization: moon_visualization_0.05.png

# Statistics:
# Original size: 2942.15 KB
# Compressed size: 2453.66 KB
# Compression ratio: 83.40%
# Data retained: 0.66%

# Compressing with ratio: 0.1
# Files saved in output:
# 1. Compressed FFT data: output/moon_compressed_0.10.npz
# 2. Reconstructed image: output/moon_reconstructed_0.10.png
# 3. Visualization: moon_visualization_0.10.png

# Statistics:
# Original size: 2942.15 KB
# Compressed size: 9845.44 KB
# Compression ratio: 334.63%
# Data retained: 2.66%

# Compressing with ratio: 0.2
# Files saved in output:
# 1. Compressed FFT data: output/moon_compressed_0.20.npz
# 2. Reconstructed image: output/moon_reconstructed_0.20.png
# 3. Visualization: moon_visualization_0.20.png

# Statistics:
# Original size: 2942.15 KB
# Compressed size: 39272.74 KB
# Compression ratio: 1334.83%
# Data retained: 10.66%



def compress_image_fft(image_path, compression_ratio=0.1, save_dir="output"):
    os.makedirs(save_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Read image and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)

    # Apply 2D FFT
    fft = np.fft.fft2(img_array)
    fft_shifted = np.fft.fftshift(fft)

    # Create mask for compression
    rows, cols = img_array.shape
    crow, ccol = rows//2, cols//2
    mask = np.zeros((rows, cols), dtype=bool)
    r = int(min(rows, cols) * compression_ratio)
    mask[crow-r:crow+r, ccol-r:ccol+r] = True

    # Get only the necessary FFT coefficients
    fft_compressed = fft_shifted * mask
    nonzero_indices = np.nonzero(mask)
    compressed_values = fft_compressed[nonzero_indices]

    # Save only the nonzero values and their positions
    compressed_data = {
        'values': compressed_values,
        'indices': np.array(nonzero_indices),
        'shape': img_array.shape,
        'compression_ratio': compression_ratio
    }
    compressed_filename = os.path.join(save_dir, f"{base_name}_compressed_{compression_ratio:.2f}.npz")
    np.savez_compressed(compressed_filename, **compressed_data)

    # Reconstruct image
    ifft_shifted = np.fft.ifftshift(fft_compressed)
    img_restored = np.abs(np.fft.ifft2(ifft_shifted))

    # Normalize reconstructed image
    img_restored_normalized = ((img_restored - img_restored.min()) *
                             (255.0 / (img_restored.max() - img_restored.min()))).astype(np.uint8)

    # Save reconstructed image
    reconstructed_filename = os.path.join(save_dir, f"{base_name}_reconstructed_{compression_ratio:.2f}.png")
    Image.fromarray(img_restored_normalized).save(reconstructed_filename)

    # Create visualization (same as before...)
    plt.figure(figsize=(15, 10))

    plt.subplot(231)
    plt.imshow(img_array, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(232)
    plt.imshow(np.log1p(np.abs(fft_shifted)), cmap='gray')
    plt.title('FFT Magnitude Spectrum')
    plt.axis('off')

    plt.subplot(233)
    plt.imshow(mask, cmap='gray')
    plt.title(f'Compression Mask\n(keeping {compression_ratio*100:.1f}% of data)')
    plt.axis('off')

    plt.subplot(234)
    plt.imshow(np.log1p(np.abs(fft_compressed)), cmap='gray')
    plt.title('Compressed FFT Spectrum')
    plt.axis('off')

    plt.subplot(235)
    plt.imshow(img_restored_normalized, cmap='gray')
    plt.title('Reconstructed Image')
    plt.axis('off')

    difference = np.abs(img_array - img_restored_normalized)
    plt.subplot(236)
    plt.imshow(difference, cmap='hot')
    plt.title('Difference (Error)')
    plt.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{base_name}_visualization_{compression_ratio:.2f}.png"))
    plt.close()

    # Calculate and print statistics
    original_size = os.path.getsize(image_path)
    compressed_size = os.path.getsize(compressed_filename)
    actual_compression_ratio = compressed_size / original_size

    print(f"Files saved in {save_dir}:")
    print(f"1. Compressed FFT data: {compressed_filename}")
    print(f"2. Reconstructed image: {reconstructed_filename}")
    print(f"3. Visualization: {base_name}_visualization_{compression_ratio:.2f}.png")
    print("\nStatistics:")
    print(f'Original size: {original_size/1024:.2f} KB')
    print(f'Compressed size: {compressed_size/1024:.2f} KB')
    print(f'Compression ratio: {actual_compression_ratio:.2%}')
    print(f'Data retained: {np.count_nonzero(mask)/mask.size:.2%}')

    return compressed_filename, reconstructed_filename

def decompress_fft_file(compressed_file):
    """Decompress an FFT-compressed file back to an image"""
    # Load compressed data
    data = np.load(compressed_file)
    values = data['values']
    indices = data['indices']
    shape = data['shape']

    # Reconstruct FFT array
    fft_compressed = np.zeros(shape, dtype=complex)
    fft_compressed[tuple(indices)] = values

    # Reconstruct image
    ifft_shifted = np.fft.ifftshift(fft_compressed)
    img_restored = np.abs(np.fft.ifft2(ifft_shifted))

    # Normalize
    img_restored_normalized = ((img_restored - img_restored.min()) *
                             (255.0 / (img_restored.max() - img_restored.min()))).astype(np.uint8)

    # Save decompressed image
    output_path = compressed_file.replace('.npz', '_decompressed.png')
    Image.fromarray(img_restored_normalized).save(output_path)

    return output_path

# Example usage
if __name__ == "__main__":
    image_path = "moon.jpg"  # Replace with your image path
    for ratio in [0.05, 0.1, 0.2]:
        print(f"\nCompressing with ratio: {ratio}")
        compress_image_fft(image_path, ratio)
