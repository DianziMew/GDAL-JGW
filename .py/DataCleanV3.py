import os
import tkinter as tk
from tkinter import filedialog, messagebox
from osgeo import gdal
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed


# 将转换逻辑封装成一个独立的函数，供进程池调用
def convert_single_file(file_info):
    input_path, output_path, options_dict = file_info
    try:
        # 在多进程中，GDAL 选项需要通过字典或参数传递
        options = gdal.TranslateOptions(**options_dict)
        gdal.Translate(output_path, input_path, options=options)

        # 辅助文件重命名逻辑 (.wld/.jpgw -> .jgw)
        for ext in [".wld", ".jpgw"]:
            possible_file = output_path.replace(".jpg", ext)
            target_jgw = output_path.replace(".jpg", ".jgw")

            if os.path.exists(possible_file):
                if os.path.exists(target_jgw):
                    os.remove(target_jgw)
                os.rename(possible_file, target_jgw)
        return True, None
    except Exception as e:
        return False, f"错误: {os.path.basename(input_path)} - {str(e)}"


def batch_tif_to_jpg_parallel():
    # 1. GUI 选择目录
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    input_dir = filedialog.askdirectory(title="选择输入文件夹")
    if not input_dir: return
    output_dir = filedialog.askdirectory(title="选择输出文件夹")
    if not output_dir: return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. 准备文件列表
    tif_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.tif', '.tiff'))]
    total_count = len(tif_files)
    if total_count == 0:
        messagebox.showinfo("提示", "未找到 TIF 文件")
        return

    # 3. 准备进程池参数
    # 9950X 有 16 核 32 线程，建议开启 16-24 个进程，预留一点给系统 IO
    max_workers = min(os.cpu_count(), 24)

    tasks = []
    for filename in tif_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".jpg")
        # GDAL 配置参数
        options_dict = {
            'format': 'JPEG',
            'bandList': [1, 2, 3],
            'creationOptions': ['WORLDFILE=YES', 'QUALITY=90']
        }
        tasks.append((input_path, output_path, options_dict))

    print(f"检测到 CPU 核心数: {os.cpu_count()}, 启动进程数: {max_workers}")
    print(f"开始并行转换 {total_count} 个文件...")

    # 4. 使用进程池执行任务
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # 使用 list 让任务提交并获取 future 对象
        futures = [executor.submit(convert_single_file, t) for t in tasks]

        # tqdm 结合 as_completed 实时更新进度条
        with tqdm(total=total_count, desc="并行转换中", unit="file") as pbar:
            for future in as_completed(futures):
                success, error_msg = future.result()
                if not success:
                    tqdm.write(error_msg)
                pbar.update(1)

    messagebox.showinfo("完成", f"任务已处理完毕！\n处理总数：{total_count}")


if __name__ == "__main__":
    # 注意：在 Windows 下使用多进程，必须放在 if __name__ == "__main__": 下
    batch_tif_to_jpg_parallel()