import inspect
import doctest
import os
from typing import List, Callable, Optional


def make_module(objects: List[Callable],
                module_name: str = 'module.py',
                module_dir: Optional[str] = None) -> None:
    """Save currently defined classes and functions to modules

        Examples:
            >>> import tempfile
            >>> outfile_path = tempfile.mkstemp('.py')[1]
            >>> def my_add(*args): return sum(args)
            >>> make_module([my_add], module_name=outfile_path)
            >>> with open(outfile_path, 'r') as f: f.read()
            'def my_add(*args): return sum(args)\\n\\n\\n'
    """

    def write_defs(path: str, definitions: List[str]) -> None:
        with open(path, 'w') as file:
            for definition in definitions:
                file.write(definition)

    defs = [inspect.getsource(obj) + '\n\n' for obj in objects]

    if module_dir is None:
        write_defs(module_name, defs)
    else:
        if not os.path.isdir(module_dir):
            os.makedirs(module_dir)
            print(f'Created {module_dir} folder.')
        write_defs(module_dir + '/' + module_name, defs)


if __name__ == '__main__':
    doctest.testmod(verbose=True)
