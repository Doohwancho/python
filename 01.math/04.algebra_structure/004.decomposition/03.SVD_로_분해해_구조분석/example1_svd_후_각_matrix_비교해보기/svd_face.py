import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def visualize_svd_face(image_path, n_components_to_show=8):
    """
    Visualize SVD components of a face image and its reconstructions
    
    Args:
        image_path: Path to face image
        n_components_to_show: Number of components to visualize
    """
    # Read image and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=np.float64)
    
    # Perform SVD
    U, s, Vt = np.linalg.svd(img_array, full_matrices=False)
    
    # Create figure (3 rows: U components, V components, Reconstructions)
    fig = plt.figure(figsize=(20, 12))
    
    # Plot original image
    plt.subplot(4, n_components_to_show, 1)
    plt.imshow(img_array, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    
    # Plot components and reconstructions
    for i in range(n_components_to_show):
        # Plot U component (just the i-th component)
        plt.subplot(4, n_components_to_show, i + 1 + n_components_to_show)
        u_component = U[:, i].reshape(img_array.shape[0], 1)
        plt.imshow(u_component, cmap='gray')
        plt.title(f'U{i+1}')
        plt.axis('off')
        
        # Plot V component (just the i-th component)
        plt.subplot(4, n_components_to_show, i + 1 + 2*n_components_to_show)
        v_component = Vt[i, :].reshape(1, img_array.shape[1])
        plt.imshow(v_component, cmap='gray')
        plt.title(f'V{i+1}')
        plt.axis('off')
        
        # Plot reconstruction using up to i+1 components
        plt.subplot(4, n_components_to_show, i + 1 + 3*n_components_to_show)
        reconstruction = np.zeros_like(img_array)
        for j in range(i + 1):
            reconstruction += s[j] * np.outer(U[:, j], Vt[j, :])
        reconstruction = np.clip(reconstruction, 0, 255)
        plt.imshow(reconstruction, cmap='gray')
        plt.title(f'Using 1~{i+1}')
        plt.axis('off')
    
    # Plot singular values
    plt.figure(figsize=(10, 4))
    plt.plot(s[:50], 'b-')
    plt.title('First 50 Singular Values')
    plt.xlabel('Index')
    plt.ylabel('Singular Value')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    image_path = "face.jpg"  # Replace with your face image path
    visualize_svd_face(image_path)