import os
from osgeo import gdal #GDAL 地理数据抽象库

def batch_tif_to_jpg_with_jgw(input_dir, output_dir):
    # 如果输出目录不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历文件夹中所有的 .tif 文件
    tif_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.tif') or f.lower().endswith('.tiff')]

    print(f"找到 {len(tif_files)} 个文件，准备开始转换...")

    for filename in tif_files:
        input_path = os.path.join(input_dir, filename)
        # 生成输出文件名（去除扩展名后加 .jpg）
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, base_name + ".jpg")

        # 配置转换参数
        # format='JPEG' 指定输出格式
        # creationOptions=['WORLDFILE=YES'] 这行最关键，它会自动生成坐标辅助文件
        # options = gdal.TranslateOptions(
        #    format='JPEG',
        #    creationOptions=['WORLDFILE=YES']
        #)
        #这里这么做的原因是4通道多了个透明通道 ->

        # 配置转换参数
        options = gdal.TranslateOptions(
            format='JPEG',
            # 关键修改：强制只提取前三个波段，避免出现 CMYK 错误
            bandList=[1, 2, 3],
            creationOptions=['WORLDFILE=YES', 'QUALITY=90']
        )

        try:
            gdal.Translate(output_path, input_path, options=options)

            # GDAL 默认生成的后缀可能是 .wld 或 .jpgw
            # 我们将其统一重命名为 .jgw
            possible_wld = output_path.replace(".jpg", ".wld")
            possible_jpgw = output_path.replace(".jpg", ".jpgw")
            target_jgw = output_path.replace(".jpg", ".jgw")

            if os.path.exists(possible_wld):
                os.rename(possible_wld, target_jgw)
            elif os.path.exists(possible_jpgw):
                os.rename(possible_jpgw, target_jgw)

            print(f"成功: {filename} -> {base_name}.jpg & .jgw")
        except Exception as e:
            print(f"错误: 转换 {filename} 失败: {e}")


# --- 使用示例 ---
input_folder = 'E:\南通融信信息\测试JPG与JGW转换1月17日\转换层'  # 替换为你的输入文件夹路径
output_folder = 'E:\南通融信信息\测试JPG与JGW转换1月17日\测试层\存放'  # 替换为你的输出文件夹路径

batch_tif_to_jpg_with_jgw(input_folder, output_folder)

# --- 使用示例 ---
# input_folder = 'path/to/your/tifs'  # 替换为你的输入文件夹路径
# output_folder = 'path/to/output'  # 替换为你的输出文件夹路径
#
# batch_tif_to_jpg_with_jgw(input_folder, output_folder)
