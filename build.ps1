.\ui2py.ps1
python -m nuitka h5view `
    --include-package=h5view `
    --mode=app --enable-plugin=pyside6 `
    --user-package-configuration-file=user.nuitka-package.config.yml `
    --include-qt-plugins=sensible --disable-ccache