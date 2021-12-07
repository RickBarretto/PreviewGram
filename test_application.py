"""
Run this module, if you want to run application without build
"""

import src

if __name__ == '__main__':
    src.start_app()


"""
Changelog:

- Model class deleted
- src.model.db moved to src.model
- Parse class from `src.model.__parser__` deleted
- Imports on `src` starts with `src.`
"""