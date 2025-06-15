# 3D Point Cloud Generation from Monocular Images 🚀  

**FURP-2024-2025 | Week 2 Report: Depth Estimation & 3D Reconstruction** 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Open3D](https://img.shields.io/badge/Open3D-0.17.0-green)
![ZoeDepth](https://img.shields.io/badge/ZoeDepth-v1.0.0-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1.1-red)

<div align="center">
  <img src="https://github.com/user-attachments/assets/cf192af0-bc61-4097-8753-04fc9dbcdcbb" width="30%">
  <img src="https://github.com/user-attachments/assets/97c3cfdc-9ef2-41a8-85be-0f4641f0c79a" width="30%">
  <img src="https://github.com/user-attachments/assets/f718c348-34ab-4a92-8199-78112bbf15c2" width="30%">
</div>

## 🔍 Project Overview  
This project implements the **ZoeDepth monocular depth estimation algorithm** (https://github.com/isl-org/ZoeDepth), achieving a complete pipeline from RGB images to 3D point clouds. Core innovations include:  
1. **Depth Map Generation**: Real-time prediction using lightweight ZoeDepth-N model  
2. **Point Cloud Conversion**: Mapping pixels to 3D space via Open3D  
3. **Interactive Visualization**: Dynamic rotation/zooming of point clouds  

## ⚙️ Technical Implementation
### Algorithm Architecture
```mermaid
graph LR
A[RGB Image] --> B(ZoeDepth Model)
B --> C[Depth Map]
C --> D(Point Cloud Conversion)
D --> E[Interactive 3D Visualization]
