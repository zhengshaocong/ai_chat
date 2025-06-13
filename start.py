import os
import sys
import subprocess
import platform

def is_venv():
    """检查是否在虚拟环境中"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def create_and_activate_venv():
    """创建并激活虚拟环境"""
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
    
    # 检查虚拟环境是否存在
    if not os.path.exists(venv_path):
        print("正在创建虚拟环境...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    
    # 根据操作系统选择激活脚本
    if platform.system() == 'Windows':
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        python_path = os.path.join(venv_path, 'bin', 'python')
        pip_path = os.path.join(venv_path, 'bin', 'pip')

    # 安装依赖
    print("正在安装依赖...")
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)

    return python_path

def main():
    if not is_venv():
        print("未检测到虚拟环境，正在设置...")
        python_path = create_and_activate_venv()
    else:
        print("已在虚拟环境中")
        python_path = sys.executable

    # 运行主程序
    print("正在启动应用...")
    subprocess.run([python_path, 'run.py'])

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1) 