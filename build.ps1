.\ui2py.ps1
python -m nuitka h5view `
    --include-package=h5view `
    --onefile --enable-plugin=pyside6 `
    --enable-plugin=numpy `
    --include-data-files=h5view/*.ui=./ `
    --include-qt-plugins=sensible --disable-ccache