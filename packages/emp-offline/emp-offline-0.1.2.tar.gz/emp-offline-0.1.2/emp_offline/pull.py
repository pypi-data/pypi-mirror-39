import os

django_path = os.path.dirname(os.path.realpath(__file__))
django_html_path = os.path.join(django_path, 'ide/templates/ide/index.html')
django_static_path = os.path.join(django_path, 'ide/static')

vue_path = '../MicroIDE'
vue_html = os.path.join(vue_path, 'dist/index.html')
vue_static = os.path.join(vue_path, 'dist/static/')


def npm_build(des_path=vue_path):
    os.chdir(des_path)
    os.system('npm run build')
    os.chdir(django_path)


def del_django_static(des_path=django_static_path):
    try:
        os.system('rm -rf ' + des_path)
        print(des_path, 'removed.')
    except:
        pass


def copy_static_to_django(src_path=vue_static, des_path=django_static_path):
    os.system('cp -rp ' + src_path + ' ' + des_path)
    print('static files copy done')


def copy_html_to_django(src_path=vue_html, des_path=django_html_path):
    os.system('cp -rp ' + src_path + ' ' + des_path)
    print('index.html copy done')
    

if __name__ == '__main__':
    print(django_path)
    npm_build()
    del_django_static()
    copy_html_to_django()
    copy_static_to_django()
    print('deploy done.')
