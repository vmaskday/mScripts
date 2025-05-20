import os
import re
import shutil

INCLUDE_PATTERN = re.compile(r'#include\s+(?:"([^"]+)"|<([^>]+)>)')

def find_includes(file_path, base_dirs):
    """查找一个文件中的所有 #include 并返回绝对路径"""
    includes = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return includes

    dir_name = os.path.dirname(file_path)

    for match in INCLUDE_PATTERN.findall(content):
        quote_include, angle_include = match
        if quote_include:
            # 处理 "#include "..."
            rel_path = os.path.normpath(os.path.join(dir_name, quote_include))
            if os.path.exists(rel_path):
                includes.add(rel_path)
            else:
                # 在 base_dirs 中查找
                found = False
                for base_dir in base_dirs:
                    abs_path = os.path.normpath(os.path.join(base_dir, quote_include))
                    if os.path.exists(abs_path):
                        includes.add(abs_path)
                        found = True
                        break
                if not found:
                    print(f"Warning: Could not find included file: {quote_include} (from {file_path})")
        elif angle_include:
            # 处理 "#include <...>"
            found = False
            for base_dir in base_dirs:
                abs_path = os.path.normpath(os.path.join(base_dir, angle_include))
                if os.path.exists(abs_path):
                    includes.add(abs_path)
                    found = True
                    break
            if not found:
                print(f"Warning: Could not find system include: {angle_include} (from {file_path})")

    return includes


def collect_all_includes(start_file, base_dirs):
    """递归收集所有 include 文件"""
    visited = set()
    to_visit = [start_file]

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)
        includes = find_includes(current, base_dirs)
        for inc in includes:
            if inc not in visited:
                to_visit.append(inc)

    return visited


def copy_files_with_structure(files, source_root, dest_root):
    """将文件按照相对于 source_root 的路径复制到 dest_root 下"""
    for file in files:
        rel_path = os.path.relpath(file, start=source_root)
        dest_file = os.path.join(dest_root, rel_path)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(file, dest_file)
        print(f"Copied: {file} -> {dest_file}")


def main(dts_file, new_dir, search_paths=None):
    """
    主函数
    :param dts_file: 初始 dts 文件路径
    :param new_dir: 输出目录
    :param search_paths: 包含搜索路径列表（用于查找 include）
    """
    if not os.path.isfile(dts_file):
        print(f"Error: File not found - {dts_file}")
        return

    if search_paths is None:
        search_paths = [os.path.dirname(dts_file)]

    all_files = collect_all_includes(dts_file, search_paths)
    if not all_files:
        print("No include files found.")
        return

    source_root = os.path.commonprefix(list(all_files))
    source_root = os.path.dirname(source_root) if os.path.isfile(source_root) else source_root

    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.makedirs(new_dir)

    copy_files_with_structure(all_files, source_root, new_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DTS Include 文件提取工具（支持 \"\" 和 <> 两种方式）")
    parser.add_argument("input_dts", help="输入的 .dts 文件路径")
    parser.add_argument("output_dir", help="输出目录")
    parser.add_argument("--search-path", nargs='+', default=None,
                        help="额外的搜索路径（用于查找 include 文件）")

    args = parser.parse_args()

    main(args.input_dts, args.output_dir, args.search_path)
