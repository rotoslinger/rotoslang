import importlib
import pkgutil
import sys

def recursive_reload(package):
    """
    Recursively reloads all modules in a package.

    Args:
        package: The package or library to reload.
    """
    # Reload the main package/module
    importlib.reload(package)

    # Traverse through all the modules in the package
    package_name = package.__name__
    if package_name in sys.modules:
        for _, mod_name, is_pkg in pkgutil.walk_packages(package.__path__, package_name + "."):
            mod = sys.modules.get(mod_name)
            if mod:
                importlib.reload(mod)

# Example usage:
# Assuming `my_package` is your package to reload:
# import my_package
# recursive_reload(my_package)
