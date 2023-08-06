from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

import  setuptools 
import subprocess


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        subprocess.check_call("sudo apt install openvpn".split())
        install.run(self)



with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='VPNKit',  
     version='0.1.0',
     scripts=['vpnkit','vpnkit.py','exit.py'] ,
     author="54origins",
     author_email="opensource@54origins.com",
     description="An OpenVPN client",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     cmdclass={
        'install': PostInstallCommand,
     },
     install_requires=[
          'psutil','requests','pathlib',
      ],
     classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
     ],
 )

