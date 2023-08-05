"""
List all installed packages in a python installation
by using pip.

It can be used to install a virtual environment, so that it matches
another installation (for example blender)
"""
import pip


installed_packages = pip.get_installed_distributions()
installed_packages = sorted(["%s==%s" % (i.key, i.version)
                             for i in installed_packages])
with open('requirement.txt', 'w') as cfile:
    for line in installed_packages:
        print(line)
        cfile.write(line+'\n')
