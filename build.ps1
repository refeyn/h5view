.\ui2py.ps1
python -m nuitka h5view `
    --include-package=h5view `
    --onefile --enable-plugin=pyside6 `
    --include-qt-plugins=sensible --disable-ccache