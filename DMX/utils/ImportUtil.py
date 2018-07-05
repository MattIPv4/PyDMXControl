"""
Not used anymore. This does work as intended, but PyCharm doesn't like it when you import stuff this util has imported.
"""


class ImportUtil:

    @staticmethod
    def loader(name: str, file: str, append_parent: bool = True) -> dict:
        import os, glob, importlib

        classes = {}

        modules = glob.glob(os.path.join(os.path.dirname(file), "*.py"))
        modules = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f)[:-3].startswith("__")]
        for module in modules:
            global_name = name.split(".")[-1] + "_" + module
            imported = importlib.import_module("." + module, name)
            classes[module] = imported.__getattribute__(module)
            if append_parent:
                classes[global_name] = imported.__getattribute__(module)
            del global_name, imported

        del os, glob, importlib, modules

        return classes
