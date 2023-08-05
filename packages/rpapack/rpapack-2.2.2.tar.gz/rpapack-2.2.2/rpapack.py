import sys
import os
import subprocess
import tempfile
import json
import shutil
import errno
import zipfile


pip = os.path.join(os.path.dirname(sys.executable), 'Scripts\\pip.exe')
if not os.path.exists(pip):
    pip = os.path.join(os.path.dirname(sys.executable), 'pip.exe')
template = '{0} show --files {1}'


def _copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def _splitline(line: str):
    index = line.index(':')
    return line[:index], line[index+2:]


def _analyze_output(output: str):
    info = dict()
    files = []
    isfile = False
    lines = output.splitlines()
    for line in lines:
        if isfile:
            files.append(line.strip())
        else:
            key, value = _splitline(line)
            if key == 'Requires':
                if value:
                    modnames = [x.strip() for x in value.split(',')]
                    for modname in modnames:
                        _, child_files = _modinfo(modname)
                        files.extend(child_files)
                    # value = [x.strip() for x in value.split(',')]
                else:
                    value = None
                continue
            elif key == 'Files':
                isfile = True
                continue
            else:
                pass
            info[key] = value
    return info, files


def _modinfo(modname):
    cmd = template.format(pip, modname)
    output = subprocess.check_output(cmd).decode('utf-8')
    info, files = _analyze_output(output)
    return info, files


def _save_metadata(modinfo: dict, dirname: str):
    metadata = {
        'version': 2,
        'type': 'sdk-external',
        'sdk-external': {
            'name': modinfo.get('Name'),
            'version': modinfo.get('Version'),
            'instruction': '',
            'introduction': modinfo.get('Summary'),
            'home-page': modinfo.get('Home-page'),
        }
    }
    filename = os.path.join(dirname, 'package.json')
    with open(filename, 'w', encoding='utf-8') as fw:
        fw.write(json.dumps(metadata))


def _copy_files(modinfo: dict, files: list, dirname: str):
    cache = set()
    for file in files:
        if file.startswith('..') or '.dist-info' in file or '__pycache__' in file:
            continue
        source = os.path.join(modinfo['Location'], file.strip())
        target = os.path.join(dirname, file.strip())
        curdir = os.path.dirname(target)
        if curdir not in cache:
            cache.add(curdir)
            if not os.path.exists(curdir):
                os.makedirs(curdir)
        _copyanything(source, target)

    # _copyanything()


def _zipdir(folder, target):
    with zipfile.ZipFile(target, 'w') as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                filename = os.path.join(root, file)
                zipf.write(filename, os.path.relpath(filename, folder))


def main():
    dirname = os.path.join(os.getcwd(), sys.argv[1])
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    info, files = _modinfo(sys.argv[1])
    
    _save_metadata(info, dirname)
    _copy_files(info, files, dirname)
    zipfile = dirname+'.rpax'
    _zipdir(dirname, zipfile)
    shutil.rmtree(dirname, True)
    print('打包完成,', zipfile)


if __name__ == '__main__':
    main()
