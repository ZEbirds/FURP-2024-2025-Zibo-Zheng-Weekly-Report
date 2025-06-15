import open3d as o3d
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm  
from mpl_toolkits.mplot3d import Axes3D
import torch

# Initialize ZoeDepth model
def init_zoe_depth_model():
    from zoedepth.models.builder import build_model
    from zoedepth.utils.config import get_config
    
    print("Initializing ZoeDepth model...")
    conf = get_config("zoedepth", "infer")
    model = build_model(conf)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return model.to(device)

# Unify dimensions of image arrays
def unify_dimensions(images):
    return [
        img if img.ndim == 3 else np.repeat(img[:, :, np.newaxis], 3, axis=2)
        for img in images
    ]

# Visualize 2D image and depth map side-by-side
def compare_2d(images, titles):
    fig, axs = plt.subplots(1, 2, figsize=(15, 7))
    for i, (img, title) in enumerate(zip(images, titles)):
        axs[i].imshow(img)
        axs[i].set_title(title)
        axs[i].axis('off')
    plt.tight_layout()
    plt.show()

# Create 3D visualization of depth map
def visualize_3d_depth(image, depth, downsample_factor=15):
    # Downsample for performance
    depth_downsampled = depth[::downsample_factor, ::downsample_factor]
    
    # Create grid coordinates
    h, w = depth_downsampled.shape
    X = np.arange(0, w) * downsample_factor
    Y = np.arange(0, h) * downsample_factor
    X, Y = np.meshgrid(X, Y)
    Y = np.flipud(Y)  # Reverse Y-axis
    
    # Calculate Z scaling
    z_scale = 0.5 * (depth_downsampled.max() - depth_downsampled.min()) / max(w, h)
    Z = depth_downsampled * z_scale
    
    # Create color mapping
    if image.ndim == 3:
        rgb_downsampled = image[::downsample_factor, ::downsample_factor]
        colors = rgb_downsampled / 255.0
    else:
        colors = cm.viridis((depth_downsampled - depth_downsampled.min()) / 
                           (depth_downsampled.max() - depth_downsampled.min()))
    
    # 3D plotting
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1, 
                          antialiased=False, shade=False)
    
    # Set view angle and labels
    ax.view_init(elev=30, azim=-45)
    ax.set_title("3D Depth Visualization")
    ax.set_xlabel('Width')
    ax.set_ylabel('Height')
    ax.set_zlabel('Depth')
    
    # Add colorbar
    mappable = cm.ScalarMappable(cmap=cm.viridis)
    mappable.set_array(depth_downsampled)
    fig.colorbar(mappable, ax=ax, label='Depth Value')
    plt.show()

# Generate point cloud from RGB image and depth map
def create_point_cloud(rgb_img, depth_np, focal_length=525.0):
    # Create RGBD image
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color=o3d.geometry.Image(np.array(rgb_img)),
        depth=o3d.geometry.Image(depth_np),
        depth_scale=1.0,
        depth_trunc=np.percentile(depth_np, 95),  # Truncate depth values beyond 95th percentile
        convert_rgb_to_intensity=False,
    )
    
    # Estimate camera intrinsic parameters (if unknown)
    width, height = rgb_img.width, rgb_img.height
    intrinsic = o3d.camera.PinholeCameraIntrinsic(
        width=width,
        height=height,
        fx=focal_length,
        fy=focal_length,
        cx=width / 2,
        cy=height / 2
    )
    
    # Create point cloud
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intrinsic)
    
    # Coordinate transformation (to avoid upside down)
    pcd.transform([[1, 0, 0, 0], 
                   [0, -1, 0, 0], 
                   [0, 0, -1, 0], 
                   [0, 0, 0, 1]])
    return pcd

# Interactive visualization of point cloud
def visualize_point_cloud(pcd):
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='3D Point Cloud', width=1200, height=800)
    
    # Rendering settings
    render_option = vis.get_render_option()
    render_option.background_color = [0.1, 0.1, 0.1]  # Dark gray background
    render_option.point_size = 1.5  # Point size
    render_option.light_on = True
    
    vis.add_geometry(pcd)
    
    # View control
    ctr = vis.get_view_control()
    ctr.set_zoom(0.8)  # Initial zoom
    
    print("Press 'K' to toggle background color, 'S' to save point cloud")
    vis.run()
    vis.destroy_window()

# Main execution flow
if __name__ == "__main__":
    # 1. Initialize ZoeDepth model
    zoe = init_zoe_depth_model()
    
    # 2. Load image and predict depth
    image_path = "0001.png"
    rgb_image = Image.open(image_path).convert("RGB")
    depth_array = zoe.infer_pil(rgb_image)
    
    # 3. Create colorized depth map
    from zoedepth.utils.misc import colorize
    colored_depth = colorize(depth_array)
    Image.fromarray(colored_depth).save("output_colored.png")
    
    # 4. 2D comparison visualization (dimension fix applied)
    images = unify_dimensions([np.array(rgb_image), colored_depth])
    compare_2d(images, ["Original Image", "Depth Map"])
    
    # 5. 3D depth visualization
    visualize_3d_depth(np.array(rgb_image), depth_array, downsample_factor=15)
    
    # 6. Create point cloud
    point_cloud = create_point_cloud(rgb_image, depth_array)
    
    # 7. Visualize point cloud
    visualize_point_cloud(point_cloud)
    
    # 8. Save point cloud (optional)
    o3d.io.write_point_cloud("output_point_cloud.ply", point_cloud)