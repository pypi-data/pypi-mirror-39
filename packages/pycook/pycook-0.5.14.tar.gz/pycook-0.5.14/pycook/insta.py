#* Imports
import os
import pycook.elisp as el
sc = el.sc
lf = el.lf


#* Functions
def install_package(package):
    res = sc("dpkg --get-selections '{package}'")
    if not len(res):
        sc(
            # "TERM=linux"
            "sudo apt-get install -y {package}")


def git_clone(addr, target):
    target = el.expand_file_name(target)
    if el.file_exists_p(target):
        print(lf("{target}: OK"))
    else:
        gdir = el.expand_file_name(target)
        pdir = el.file_name_directory(gdir)
        if not el.file_exists_p(pdir):
            el.make_directory(pdir)
        sc("git clone {addr} {gdir}")


def ln(fr, to):
    fr = el.expand_file_name(fr)
    if not el.file_exists_p(fr):
        raise RuntimeError("File doesn't exist", fr)
    to = el.expand_file_name(to)
    if el.file_directory_p(to):
        to_full = el.expand_file_name(el.file_name_nondirectory(fr), to)
    else:
        to_full = to
    if el.file_exists_p(to_full):
        print(lf("{to_full}: OK"))
    else:
        fr_abbr = os.path.relpath(fr, to)
        el.sc("ln -s {fr_abbr} {to_full}")


def make(target, cmd, deps=[]):
    if not el.file_exists_p(target):
        sc(
            # "TERM=linux " +
            cmd)
