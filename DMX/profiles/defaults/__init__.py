from .Fixture import Fixture
from .Vdim import Vdim


class ImportUtil:

    @staticmethod
    def loader(self, name, file):
        import os, glob, importlib

        modules = glob.glob(os.path.join(os.path.dirname(file), "*.py"))
        modules = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f)[:-3].startswith("__")]
        for module in modules:
            global_name = name.split(".")[-1] + "_" + module
            imported = importlib.import_module("." + module, name)
            globals()[global_name] = imported.__getattribute__(module)
                ## This updates the globals of this file and not the globals of the calling file
            del global_name, imported

        del os, glob, importlib, modules
