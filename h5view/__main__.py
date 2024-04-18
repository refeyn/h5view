# SPDX-FileCopyrightText: Copyright (c) 2024 Refeyn Ltd and other h5view contributors
# SPDX-License-Identifier: MIT

if __name__ == "__main__":
    try:
        from . import main
    except ImportError:
        from h5view import main

    main()
