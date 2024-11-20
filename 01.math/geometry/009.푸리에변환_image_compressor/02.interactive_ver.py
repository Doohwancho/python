import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class InteractiveFftCompressor:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Interactive FFT Image Compression")

        # Load and process image
        self.img = Image.open(image_path).convert('L')
        self.img_array = np.array(self.img)
        self.fft = np.fft.fft2(self.img_array)
        self.fft_shifted = np.fft.fftshift(self.fft)
        self.rows, self.cols = self.img_array.shape

        # Create matplotlib figure
        self.fig = Figure(figsize=(15, 10))

        # Create slider
        self.slider_frame = ttk.Frame(root)
        self.slider_frame.pack(pady=10)

        ttk.Label(self.slider_frame, text="Compression Ratio:").pack(side=tk.LEFT, padx=5)
        self.slider = ttk.Scale(
            self.slider_frame,
            from_=0.01,
            to=0.5,
            orient=tk.HORIZONTAL,
            length=200,
            value=0.1
        )
        self.slider.pack(side=tk.LEFT, padx=5)
        self.slider.bind("<ButtonRelease-1>", self.update_compression)

        # Add value label
        self.value_label = ttk.Label(self.slider_frame, text="0.10")
        self.value_label.pack(side=tk.LEFT, padx=5)

        # Add metrics labels
        self.metrics_frame = ttk.Frame(root)
        self.metrics_frame.pack(pady=5)
        self.compression_label = ttk.Label(self.metrics_frame, text="")
        self.compression_label.pack()
        self.mse_label = ttk.Label(self.metrics_frame, text="")
        self.mse_label.pack()
        self.psnr_label = ttk.Label(self.metrics_frame, text="")
        self.psnr_label.pack()

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial compression
        self.update_compression()

    def compress_and_show(self, compression_ratio):
        # Clear previous plots
        self.fig.clear()

        # Create mask
        crow, ccol = self.rows//2, self.cols//2
        mask = np.zeros((self.rows, self.cols), dtype=bool)
        r = int(min(self.rows, self.cols) * compression_ratio)
        mask[crow-r:crow+r, ccol-r:ccol+r] = True

        # Apply compression
        fft_compressed = self.fft_shifted * mask
        ifft_shifted = np.fft.ifftshift(fft_compressed)
        img_restored = np.abs(np.fft.ifft2(ifft_shifted))

        # Prepare visualizations
        fft_viz = np.log1p(np.abs(self.fft_shifted))
        fft_viz_compressed = np.log1p(np.abs(fft_compressed))

        # Normalize images
        def normalize_image(img):
            return ((img - img.min()) * (255.0 / (img.max() - img.min()))).astype(np.uint8)

        img_array_norm = normalize_image(self.img_array)
        fft_viz_norm = normalize_image(fft_viz)
        fft_viz_compressed_norm = normalize_image(fft_viz_compressed)
        img_restored_norm = normalize_image(img_restored)

        # Create subplots
        gs = self.fig.add_gridspec(2, 3)

        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.imshow(img_array_norm, cmap='gray')
        ax1.set_title('Original Image')
        ax1.axis('off')

        ax2 = self.fig.add_subplot(gs[0, 1])
        ax2.imshow(fft_viz_norm, cmap='gray')
        ax2.set_title('FFT Spectrum')
        ax2.axis('off')

        ax3 = self.fig.add_subplot(gs[0, 2])
        ax3.imshow(mask, cmap='gray')
        ax3.set_title(f'Compression Mask\n({compression_ratio*100:.1f}% data)')
        ax3.axis('off')

        ax4 = self.fig.add_subplot(gs[1, 0])
        ax4.imshow(fft_viz_compressed_norm, cmap='gray')
        ax4.set_title('Compressed FFT')
        ax4.axis('off')

        ax5 = self.fig.add_subplot(gs[1, 1])
        ax5.imshow(img_restored_norm, cmap='gray')
        ax5.set_title('Reconstructed')
        ax5.axis('off')

        ax6 = self.fig.add_subplot(gs[1, 2])
        im = ax6.imshow(np.abs(img_array_norm - img_restored_norm), cmap='hot')
        ax6.set_title('Error Map')
        self.fig.colorbar(im, ax=ax6)
        ax6.axis('off')

        self.fig.tight_layout()

        # Update metrics
        mse = np.mean((img_array_norm - img_restored_norm) ** 2)
        psnr = 20 * np.log10(255) - 10 * np.log10(mse)
        compression = np.count_nonzero(mask)/mask.size

        self.compression_label.config(text=f'Compression: {compression:.2%}')
        self.mse_label.config(text=f'MSE: {mse:.2f}')
        self.psnr_label.config(text=f'PSNR: {psnr:.2f} dB')

        # Redraw canvas
        self.canvas.draw()

    def update_compression(self, event=None):
        value = self.slider.get()
        self.value_label.config(text=f"{value:.2f}")
        self.compress_and_show(value)

def main():
    root = tk.Tk()
    root.state('zoomed')  # Maximize window
    app = InteractiveFftCompressor(root, "moon.jpg")  # Replace with your image path
    root.mainloop()

if __name__ == "__main__":
    main()
