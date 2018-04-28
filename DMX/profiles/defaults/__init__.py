class ImportUtil:

    @staticmethod
    def loader(name: str, file: str, append_parent: bool = True) -> dict:
        import os, glob, importlib

        classes = {}

        modules = glob.glob(os.path.join(os.path.dirname(file), "*.py"))
        modules = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f)[:-3].startswith("__")]
        for module in modules:
            global_name = name.split(".")[-1] + "_" + module if append_parent else module
            imported = importlib.import_module("." + module, name)
            classes[global_name] = imported.__getattribute__(module)
            del global_name, imported

        del os, glob, importlib, modules

        return classes

globals().update(ImportUtil.loader(__name__, __file__, False))

