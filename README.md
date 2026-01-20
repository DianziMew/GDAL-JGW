
# GDAL-JGW: 地理影像轻量化搬运工

[![Python](https://img.shields.io/badge/Python-3.12.4+-blue.svg)](https://www.python.org/)
[![GDAL](https://img.shields.io/badge/Powered%20by-GDAL-green.svg)](https://gdal.org/)
[![License](https://img.shields.io/badge/License-AGPL3.0-black.svg)](LICENSE)

> **“让笨重的 TIFF 变身轻盈的 JPG，同时不弄丢它的‘家’（地理坐标）。”**

---

## 📖 简介

在 GIS 开发和数据处理中，我们经常遇到巨大的 `.tif` 影像。它们虽然信息丰富，但在 Web 展示、快速预览或移动端应用中显得过于沉重。

**Geo-Tiff2JPG** 是一个 Python 自动化工具，旨在解决两个痛点：
1. **轻量化转换**：将 GB/TB 级的 TIFF 批量转为高压缩比的 JPG。
2. **基因继承**：自动提取 TIFF 内部的地理参考信息，并生成对应的 `.jgw` (World File)，确保图片在 ArcGIS、QGIS 或 Global Mapper 中依然能精准“定位”。

---

## ✨ 核心特性

* 🚀 **批量高效**：一键处理整个文件夹，告别手动一个一个导出的痛苦。
* 🌍 **坐标传承**：通过生成 `.jgw` 文件，完美保留投影和地理位置信息。
* 🎨 **智能纠偏**：针对 4 波段影像带来的“颜色变异”（CMYK 错误）进行了优化，强制回归标准 RGB。
* 🧹 **自动净化**：智能过滤并跳过 `.ovr`、`.aux.xml` 等冗余辅助文件，只处理核心影像。

---

## 🛠️ 安装要求

本项目依赖于强大的 **GDAL** 库。请确保您的 Python 环境中已安装 GDAL。

### 推荐安装方式 (Conda)
```bash
conda install gdal
