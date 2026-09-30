import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quality', choices=['l', 'm', 'h'], default='m',
                        help='l=480p15, m=720p30, h=1080p60')
    parser.add_argument('--check-only', action='store_true', help='Compilar y verificar solo C++')
    args = parser.parse_args()
    compiler = os.environ.get('CXX', 'g++')
    if shutil.which(compiler) is None:
        raise SystemExit('No se encuentra g++. Instala un compilador C++17 y agregalo al PATH.')
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    exe = build / ('bloom.exe' if os.name == 'nt' else 'bloom')
    subprocess.run([compiler, '-std=c++17', '-O2', '-Wall', '-Wextra',
                    str(ROOT / 'bloom.cpp'), '-o', str(exe)], check=True)
    subprocess.run([str(exe), str(ROOT / 'trace.json')], check=True)
    if args.check_only:
        return
    subprocess.run([sys.executable, '-m', 'manim', '-q' + args.quality,
                    '--disable_caching', '--progress_bar', 'none',
                    str(ROOT / 'bloom_animation.py'), 'BloomCompleto'],
                    cwd=ROOT, check=True)
    quality_dir = {'l': '480p15', 'm': '720p30', 'h': '1080p60'}[args.quality]
    source = ROOT / 'media' / 'videos' / 'bloom_animation' / quality_dir / 'BloomCompleto.mp4'
    target = ROOT / 'bloom_completo.mp4'
    shutil.copy2(source, target)
    print('Video listo:', target)


if __name__ == '__main__':
    main()
