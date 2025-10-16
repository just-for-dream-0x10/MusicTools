#!/usr/bin/env python3
"""
模型重新训练脚本 - MusicAITools
使用 conda activate myenv 环境

支持训练的模型：
1. InstrumentTimbre - 乐器音色分析模型
2. Theory_net Emotion - 音乐情感分析模型  
3. Theory_net Theory - 音乐理论分析模型
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse

def check_environment():
    """检查训练环境"""
    print("🔍 检查训练环境...")
    
    # 检查conda环境
    try:
        result = subprocess.run(['conda', 'info', '--envs'], 
                              capture_output=True, text=True)
        if 'myenv' in result.stdout:
            print("✅ conda myenv 环境存在")
        else:
            print("❌ conda myenv 环境未找到")
            return False
    except:
        print("❌ conda 未安装或不可用")
        return False
    
    # 检查音频文件
    wav_files = list(Path("../wav").glob("*.wav")) if Path("../wav").exists() else []
    print(f"📁 在 ../wav 目录找到 {len(wav_files)} 个WAV音频文件")
    
    if len(wav_files) < 5:
        print("⚠️  音频文件较少，建议添加更多训练数据")
    
    return True

def retrain_instrument_timbre():
    """重新训练乐器音色分析模型"""
    print("\n🎵 开始重新训练 InstrumentTimbre 模型")
    print("=" * 50)
    
    # 准备训练数据
    data_dir = "../wav"  # 使用上级目录的wav数据
    if not Path(data_dir).exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return False
    
    # 训练命令
    cmd = [
        "/opt/anaconda3/bin/conda", "run", "-n", "myenv",
        "python", "train.py",
        "--data-dir", data_dir,
        "--chinese-instruments",  # 优化中国传统乐器
        "--use-wav-files",        # 直接使用WAV文件
        "--augment",             # 数据增强
        "--epochs", "50",        # 训练轮数
        "--batch-size", "16",    # 批次大小
        "--lr", "0.001",         # 学习率
        "--patience", "10",      # 早停耐心值
        "--cache-features",      # 启用特征缓存
        "--device", "auto"       # 自动选择设备
    ]
    
    print(f"🚀 训练命令: {' '.join(cmd[5:])}")  # 显示python部分的命令
    
    try:
        # 切换到InstrumentTimbre目录
        os.chdir("InstrumentTimbre")
        
        # 执行训练
        result = subprocess.run(cmd, cwd=".", capture_output=False)
        
        if result.returncode == 0:
            print("✅ InstrumentTimbre 模型训练完成!")
            return True
        else:
            print("❌ InstrumentTimbre 模型训练失败")
            return False
            
    except Exception as e:
        print(f"❌ 训练过程出错: {e}")
        return False
    finally:
        os.chdir("..")  # 返回主目录

def retrain_emotion_model():
    """重新训练情感分析模型"""
    print("\n🎭 开始重新训练 Emotion 模型")
    print("=" * 50)
    
    # 检查数据
    audio_dir = "../wav"
    if not Path(audio_dir).exists():
        print(f"❌ 音频目录不存在: {audio_dir}")
        return False
    
    # 训练命令
    cmd = [
        "/opt/anaconda3/bin/conda", "run", "-n", "myenv",
        "python", "train/train_emotion_model.py",
        "--audio-dir", audio_dir,
        "--epochs", "100",
        "--batch-size", "32",
        "--learning-rate", "0.001",
        "--validation-split", "0.2",
        "--early-stopping-patience", "15",
        "--device", "auto"
    ]
    
    print(f"🚀 训练命令: {' '.join(cmd[5:])}")
    
    try:
        # 切换到theory_net目录
        os.chdir("theory_net")
        
        # 执行训练
        result = subprocess.run(cmd, cwd=".", capture_output=False)
        
        if result.returncode == 0:
            print("✅ Emotion 模型训练完成!")
            return True
        else:
            print("❌ Emotion 模型训练失败")
            return False
            
    except Exception as e:
        print(f"❌ 训练过程出错: {e}")
        return False
    finally:
        os.chdir("..")

def retrain_theory_model():
    """重新训练音乐理论分析模型"""
    print("\n🎼 开始重新训练 Theory 模型")
    print("=" * 50)
    
    # 检查数据
    data_dir = "../wav"
    if not Path(data_dir).exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return False
    
    # 训练命令
    cmd = [
        "/opt/anaconda3/bin/conda", "run", "-n", "myenv", 
        "python", "train/train_theory_model.py",
        "--data-dir", data_dir,
        "--epochs", "150",
        "--batch-size", "24",
        "--learning-rate", "0.001",
        "--validation-split", "0.15"
    ]
    
    print(f"🚀 训练命令: {' '.join(cmd[5:])}")
    
    try:
        # 切换到theory_net目录
        os.chdir("theory_net")
        
        # 执行训练
        result = subprocess.run(cmd, cwd=".", capture_output=False)
        
        if result.returncode == 0:
            print("✅ Theory 模型训练完成!")
            return True
        else:
            print("❌ Theory 模型训练失败") 
            return False
            
    except Exception as e:
        print(f"❌ 训练过程出错: {e}")
        return False
    finally:
        os.chdir("..")

def quick_test_training():
    """快速测试训练 - 少量epoch验证环境"""
    print("\n🧪 快速测试训练环境")
    print("=" * 50)
    
    cmd = [
        "/opt/anaconda3/bin/conda", "run", "-n", "myenv",
        "python", "train.py",
        "--data-dir", "../wav",
        "--epochs", "2",        # 只训练2个epoch
        "--batch-size", "8",    # 小批次
        "--debug",              # 调试模式
        "--device", "auto"
    ]
    
    try:
        os.chdir("InstrumentTimbre")
        print("🚀 开始快速测试...")
        
        result = subprocess.run(cmd, cwd=".", capture_output=False)
        
        if result.returncode == 0:
            print("✅ 训练环境测试通过!")
            return True
        else:
            print("❌ 训练环境测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        return False
    finally:
        os.chdir("..")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MusicAITools 模型重新训练工具")
    parser.add_argument("--model", 
                       choices=["instrument", "emotion", "theory", "all", "test"],
                       default="test",
                       help="选择要训练的模型")
    parser.add_argument("--check-env", action="store_true", help="只检查环境")
    
    args = parser.parse_args()
    
    print("🎵 MusicAITools 模型重新训练工具")
    print("=" * 60)
    print("环境: conda activate myenv")
    print("")
    
    # 检查环境
    if not check_environment():
        print("❌ 环境检查失败，请确保:")
        print("1. conda myenv 环境已创建并激活")
        print("2. 安装了所需依赖: pip install -r requirements.txt")
        print("3. 有足够的音频训练数据")
        return
    
    if args.check_env:
        print("✅ 环境检查完成")
        return
    
    # 执行训练
    success_count = 0
    total_count = 0
    
    if args.model == "test":
        print("\n🧪 执行快速测试...")
        if quick_test_training():
            print("✅ 快速测试成功! 可以开始正式训练")
        else:
            print("❌ 快速测试失败，请检查环境配置")
        return
    
    if args.model in ["instrument", "all"]:
        total_count += 1
        if retrain_instrument_timbre():
            success_count += 1
    
    if args.model in ["emotion", "all"]:
        total_count += 1
        if retrain_emotion_model():
            success_count += 1
    
    if args.model in ["theory", "all"]:
        total_count += 1
        if retrain_theory_model():
            success_count += 1
    
    # 总结
    print("\n" + "=" * 60)
    print(f"📊 训练总结: {success_count}/{total_count} 个模型训练成功")
    
    if success_count == total_count:
        print("🎉 所有模型训练完成!")
    else:
        print("⚠️  部分模型训练失败，请检查上面的错误信息")

if __name__ == "__main__":
    main()