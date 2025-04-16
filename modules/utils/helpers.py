#!/usr/bin/env python3
"""
辅助工具模块

提供在整个项目中使用的通用辅助功能，如文件处理、日志记录等。

函数:
    ensure_dir: 确保目录存在
    get_file_info: 获取文件信息
    setup_logger: 设置日志记录器
"""
import os
import glob
import logging
from datetime import datetime

def ensure_dir(directory):
    """
    确保目录存在，如果不存在则创建

    参数:
        directory (str): 要检查/创建的目录路径

    返回:
        str: 目录路径
    """
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"已创建目录: {directory}")
    return directory

def get_file_info(file_path):
    """
    获取文件的详细信息

    参数:
        file_path (str): 文件路径

    返回:
        dict: 包含文件信息的字典，如果文件不存在则返回None
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return None
        
    try:
        stat_info = os.stat(file_path)
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'extension': os.path.splitext(file_path)[1].lower(),
            'size': stat_info.st_size,
            'size_human': format_file_size(stat_info.st_size),
            'created': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"获取文件信息时出错: {e}")
        return None

def format_file_size(size_bytes):
    """
    格式化文件大小为人类可读格式

    参数:
        size_bytes (int): 文件大小（字节）

    返回:
        str: 格式化后的文件大小
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def find_files(directory, pattern="*"):
    """
    在目录中查找匹配模式的文件

    参数:
        directory (str): 要搜索的目录路径
        pattern (str, optional): 文件匹配模式，如 "*.wav"

    返回:
        list: 匹配文件的路径列表
    """
    search_path = os.path.join(directory, pattern)
    files = glob.glob(search_path)
    return sorted(files)

def setup_logger(name="musicaitools", level=logging.INFO):
    """
    设置并返回日志记录器

    参数:
        name (str, optional): 日志记录器名称
        level (int, optional): 日志级别

    返回:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 防止重复的处理程序
    if logger.handlers:
        return logger
        
    # 创建控制台处理程序
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 设置格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # 添加处理程序
    logger.addHandler(console_handler)
    
    return logger 