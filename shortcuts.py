import os
import sys
import shutil
import subprocess

import manage


def refresh_dist():
    dist_dir = os.path.join(os.getcwd(), 'dist')
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    else:
        os.mkdir(dist_dir)


def remake_dist():
    refresh_dist()
    # subprocess.call(['npm', 'run', 'build'])
    subprocess.call('npm run build', shell=True)


def remake_dist_and_collectstatic():
    remake_dist()
    sys.argv[0], sys.argv[1] = 'manage.py', 'collectstatic'
    manage.main()
    

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except Exception:
        print('引数を入力してください。')
        
    if arg == 'refresh-dist':
        refresh_dist()
    elif arg == 'remake-dist':
        remake_dist()
    elif arg == 'remake-dist-collectstatic':
        remake_dist_and_collectstatic()
