#!/usr/bin/env python3
"""
项目环境检查脚本
"""
import sys
import importlib

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"✓ Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 12:
        print("  ✓ Python 版本满足要求 (>=3.12)")
        return True
    else:
        print("  ✗ Python 版本不满足要求，需要 >=3.12")
        return False

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        "langchain",
        "langchain_core",
        "langchain_community",
        "langchain_openai",
        "openai",
        "moviepy",
        "google.genai",
        "cv2",
        "scenedetect",
        "faiss",
        "chardet",
        "yaml",
        "PIL",
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        try:
            if package == "cv2":
                importlib.import_module("cv2")
            elif package == "yaml":
                importlib.import_module("yaml")
            elif package == "PIL":
                importlib.import_module("PIL")
            elif package == "google.genai":
                importlib.import_module("google.genai")
            elif package == "faiss":
                importlib.import_module("faiss")
            else:
                importlib.import_module(package)
            installed.append(package)
            print(f"  ✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ✗ {package} - 未安装")
    
    return missing, installed

def check_config_files():
    """检查配置文件"""
    import os
    configs = [
        "configs/idea2video.yaml",
        "configs/script2video.yaml",
    ]
    
    issues = []
    for config_file in configs:
        if os.path.exists(config_file):
            print(f"  ✓ {config_file} 存在")
            # 简单检查 API key 是否为空
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'api_key:' in content and 'api_key: ' in content.replace('api_key:', ''):
                        # 检查是否有空值
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'api_key:' in line and i+1 < len(lines):
                                next_line = lines[i+1].strip()
                                if not next_line or next_line.startswith('#') or not next_line:
                                    issues.append(f"{config_file} 中的 API key 可能未配置")
            except Exception as e:
                print(f"  ⚠ {config_file} 读取失败: {e}")
        else:
            print(f"  ✗ {config_file} 不存在")
            issues.append(f"{config_file} 不存在")
    
    return issues

def main():
    print("=" * 60)
    print("ViMax 项目环境检查")
    print("=" * 60)
    print()
    
    # 检查 Python 版本
    print("1. Python 版本检查:")
    python_ok = check_python_version()
    print()
    
    # 检查依赖
    print("2. 依赖包检查:")
    missing, installed = check_dependencies()
    print(f"\n   已安装: {len(installed)}/{len(required_packages)}")
    print(f"   缺失: {len(missing)}")
    print()
    
    # 检查配置文件
    print("3. 配置文件检查:")
    config_issues = check_config_files()
    print()
    
    # 总结
    print("=" * 60)
    print("检查总结:")
    print("=" * 60)
    
    if python_ok and len(missing) == 0 and len(config_issues) == 0:
        print("✓ 所有检查通过！项目可以启动。")
        return 0
    else:
        print("⚠ 发现问题:")
        if not python_ok:
            print("  - Python 版本不满足要求")
        if len(missing) > 0:
            print(f"  - 缺少 {len(missing)} 个依赖包")
            print("    需要运行: uv sync 或 pip install -r requirements.txt")
        if len(config_issues) > 0:
            print(f"  - 配置文件问题:")
            for issue in config_issues:
                print(f"    • {issue}")
        return 1

if __name__ == "__main__":
    required_packages = [
        "langchain",
        "langchain_core",
        "langchain_community",
        "langchain_openai",
        "openai",
        "moviepy",
        "google.genai",
        "cv2",
        "scenedetect",
        "faiss",
        "chardet",
        "yaml",
        "PIL",
    ]
    sys.exit(main())

