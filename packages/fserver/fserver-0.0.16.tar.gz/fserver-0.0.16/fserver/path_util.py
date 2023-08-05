# -*- coding: utf-8 -*-
import os
import posixpath
import re
import sys

try:
    from urllib.parse import unquote
except:
    from urllib import unquote


def translate_path(path):
    """Translate a /-separated PATH to the local filename syntax.

    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)

    """
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    # Don't forget explicit trailing slash when normalizing. Issue17324
    trailing_slash = path.rstrip().endswith('/')
    try:
        path = unquote(path, errors='surrogatepass')
    except Exception as e:
        path = unquote(path)
    path = posixpath.normpath(path)
    words = path.split('/')
    words = filter(None, words)
    path = os.getcwd()
    for word in words:
        if os.path.dirname(word) or word in (os.curdir, os.pardir):
            # Ignore components that are not a simple file/directory name
            continue
        path = os.path.join(path, word)
    if trailing_slash:
        path += '/'
    if sys.version_info < (3, 4) and not isinstance(path, unicode):  # encode by unicode
        path = path.decode('utf-8')
    return path


def to_local_path(path):
    """
    :param path:
    :return: the path relative to current path
    """
    path = to_local_abspath(path)
    here = to_local_abspath('.')

    min_len = len(path) if len(path) < len(here) else len(here)

    if os.name == 'nt' and path[0] != here[0]:
        return path
    else:
        sep_ind = -1
        diff_ind = -1
        for i in range(min_len):
            if here[i] != path[i]:
                diff_ind = i
                break
            if here[i] == '/':
                sep_ind = i
        if diff_ind == -1:
            # split the same parent_path
            if len(path) < len(here):  # path is substring of here
                c = count(here[len(path):], '/')
                return '../' * (c + 1)
            elif len(path) > len(here):  # here is substring of path
                if path[len(here)] == '/':
                    return path[len(here) + 1:]
                else:
                    return '../' + path[len(parent_path(here)) + 1:]
            else:  # here is the same with path
                return '.'
        else:
            # sep_ind won't be -1 because the use of local_abspath
            path = path[sep_ind + 1:]
            here = here[sep_ind + 1:]
            return '../' * (count(here, '/') + 1) + path


def count(string, pattern):
    res = 0
    while True:
        if pattern in string:
            string = string[string.index(pattern) + len(pattern):]
            res += 1
        else:
            break
    return res


def to_local_abspath(path):
    path = '.' if path == '' else normalize_path(path)
    return normalize_path(os.path.abspath(path))


def normalize_path(path):
    p = path.replace('\\', '/').replace('/./', '/')
    p = p[:len(p) - 1] if p.endswith('/') and len(p) != 1 else p
    p = p[2:] if p.startswith('./') else p
    p = re.compile('/+').sub('/', p)
    p = re.compile('/[^./]*?/\.\.').sub('', p)
    return p


def parents_path(path):
    """
    :param path:
    :return: return parents_path which does not contain the end '/', that is remove the end '/'
    """
    res = set()
    path = normalize_path(path)
    while '/' in path:
        sep_ind = path.rindex('/')
        res.add(path[:sep_ind])
        path = path[:sep_ind]
    if path.startswith('./') or not path.startswith('.'):
        res.add('.')
    return res


def parent_path(path):
    """
    :param path:
    :return: return path which does not contain the end '/'
    """
    path = normalize_path(path)
    if '/' not in path:
        return '.'
    else:
        sep_ind = path.rindex('/')
        return path[:sep_ind]


def is_dir(local_path):
    return os.path.isdir(local_path)


def is_file(local_path):
    return os.path.isfile(local_path)


def get_filename(path):
    path = normalize_path(path)
    if '/' in path:
        sep_ind = path.rindex('/')
        return path[sep_ind + 1:]
    else:
        return path


def get_suffix(path):
    if '.' in path:
        return path[path.rindex('.') + 1:]
    else:
        return ''


def is_child(child_path, parent_path):
    nc = normalize_path(child_path)
    np = normalize_path(parent_path)
    if len(nc) >= len(np):
        if nc == np:
            return True
        if nc.startswith(np) and nc[len(np)] == '/':
            return True
    return False


def path_exists(path):
    res = set()
    np = normalize_path(path)
    if os.path.exists(np):
        res.add(np)
        return res
    file_name = np if '/' not in np else np[np.rindex('/') + 1:]
    pattern = re.compile(file_name.replace('\\', r'\\')
                         .replace(r'$', r'\$')
                         .replace(r'(', r'\(')
                         .replace(r')', r'\)')
                         .replace(r'+', r'\+')
                         .replace(r'.', r'\.')
                         .replace(r'[', r'\[')
                         .replace(r'?', r'\?')
                         .replace(r'^', r'\^')
                         .replace(r'{', r'\{')
                         .replace(r'|', r'\|')
                         .replace(r'*', r'.*') + '$')
    npp = parent_path(np)
    if os.path.exists(npp) and os.path.isdir(npp):
        for i in os.listdir(npp):
            if pattern.match(i):
                res.add(i if file_name == np else npp + '/' + i)
    return res


if __name__ == '__main__':
    print(os.getcwd())
    print(to_local_abspath('template/'))
    print(to_local_path(os.getcwd() + '/' + '../a/b'))  # ../a/b
    print(to_local_path(os.getcwd() + '/' + 'c/d'))  # c/d
    print(to_local_path(os.getcwd() + '/' + '.'))  # .
    print(to_local_path(os.getcwd() + '/'))  # .
    print(to_local_path(os.getcwd() + '_diff/a'))  # ../x_diff/a
    print(to_local_path(parent_path(os.getcwd()) + '/diff/template'))  # ../diff/template
