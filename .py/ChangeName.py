import os
import shutil
from tkinter import filedialog, Tk


def batch_rename_process():
    # 初始化Tkinter，用于弹出文件夹选择框
    root = Tk()
    root.withdraw()

    print("--- 批量重命名工具 ---")

    # 1. 选择源文件夹
    src_dir = filedialog.askdirectory(title="第一步：选择包含原始文件的文件夹")
    if not src_dir:
        print("未选择源目录，程序退出。")
        return

    # 2. 选择输出文件夹
    dst_dir = filedialog.askdirectory(title="第二步：选择重命名后的输出文件夹")
    if not dst_dir:
        print("未选择输出目录，程序退出。")
        return

    # 如果输出目录不存在，则创建
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # 3. 遍历并处理文件
    files = os.listdir(src_dir)
    success_count = 0

    for filename in files:
        # 仅处理符合条件的文件扩展名
        if filename.lower().endswith(('.jpg', '.jgw','.xml')):
            if '-' in filename:
                # 逻辑：将 filename 分为两部分
                # 例如: "3516.000" 和 "40634.000.jpg"
                parts = filename.split('-')

                if len(parts) == 2:
                    prefix = parts[0]
                    suffix = parts[1]

                    # 关键逻辑：根据你的例子，去掉后缀部分的 "40"
                    # 如果你的逻辑是固定去掉前两个数字，可以使用 suffix[2:]
                    if suffix.startswith('40'):
                        new_suffix = suffix[2:]  # 去掉开头的 "40"
                        new_filename = f"{prefix}-{new_suffix}"

                        src_path = os.path.join(src_dir, filename)
                        dst_path = os.path.join(dst_dir, new_filename)

                        # 复制并重命名到新目录（更安全）
                        shutil.copy2(src_path, dst_path)
                        print(f"处理成功: {filename} -> {new_filename}")
                        success_count += 1

    print("-" * 30)
    print(f"任务完成！共处理文件: {success_count} 个")
    print(f"输出目录: {dst_dir}")


if __name__ == "__main__":
    batch_rename_process()