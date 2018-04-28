import os, glob, importlib

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
modules = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f)[:-3].startswith("__")]
for module in modules:
    global_name = __name__.split(".")[-1] + "_" + module
    imported = importlib.import_module("." + module, __name__)
    globals()[global_name] = imported.__getattribute__(module)
    del global_name, imported

del os, glob, importlib, modules

## TODO: Use default.ImportUtil.loader to do the above
##   from DMX.profiles.defaults import ImportUtil
##   ImportUtil.loader(__name__, __file__)
## ISSUE: Using the static method updates the globals of ImportUtil and not here