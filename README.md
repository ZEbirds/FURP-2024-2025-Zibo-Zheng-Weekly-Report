# FURP-2024-2025-Zibo-Zheng-Weekly-Report
This week, I replicated the zoeDepth algorithm for estimating the depth of images, and then combined the original image pixels with the depth map to convert and visualize the 3D point cloud.
Code could be found in /code/zoemodel blog.py

Result as shown below and also could be found in /result:
![image](https://github.com/user-attachments/assets/cf192af0-bc61-4097-8753-04fc9dbcdcbb)
![image](https://github.com/user-attachments/assets/97c3cfdc-9ef2-41a8-85be-0f4641f0c79a)
![image](https://github.com/user-attachments/assets/f718c348-34ab-4a92-8199-78112bbf15c2)


# 3D Point Cloud Generation from Monocular Images 🚀
**FURP-2024-2025 | Weekly Report: Depth Estimation & 3D Reconstruction**  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Open3D](https://img.shields.io/badge/Open3D-0.17.0-green)
![ZoeDepth](https://img.shields.io/badge/ZoeDepth-v1.0.0-orange)

<div align="center">
  <img src="https://github.com/user-attachments/assets/cf192af0-bc61-4097-8753-04fc9dbcdcbb" width="30%">
  <img src="https://github.com/user-attachments/assets/97c3cfdc-9ef2-41a8-85be-0f4641f0c79a" width="30%">
  <img src="https://github.com/user-attachments/assets/f718c348-34ab-4a92-8199-78112bbf15c2" width="30%">
</div>

## 🔍 项目概述
本项目复现了**ZoeDepth单目深度估计算法**[1](@ref)，实现了从RGB图像到3D点云的完整转换流程。核心创新点：
1. **深度图生成**：采用轻量化ZoeDepth-N模型实现实时深度预测
2. **点云转换**：结合Open3D将像素坐标映射到3D空间
3. **交互可视化**：支持动态旋转/缩放的点云探索界面

## ⚙️ 技术实现
### 算法架构
```mermaid
graph LR
A[RGB Image] --> B(ZoeDepth Model)
B --> C[Depth Map]
C --> D(Point Cloud Conversion)
D --> E[Interactive 3D Visualization]
