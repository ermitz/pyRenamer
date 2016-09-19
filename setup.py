#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from distutils.core import setup
from distutils.command.build_py import build_py as _build_py
from distutils.command.install_data import install_data as _install_data
import os 

# Note that we import the package
# you should ensure that this import has no side effect  
import pyrenamer

class build_py(_build_py):
    """build_py command
    
    This specific build_py command will modify module 'pyrenamer.build_info' so that it
    contains information on installation prefixes afterwards.
    """
    # TODO: use **kwargs, check that outfile is file or dir
    def copy_file(self, module_file, outfile, preserve_mode=0):
        if module_file.endswith('build_info.py'):
            iobj = self.distribution.command_obj['install']

            with open(outfile, 'w') as module_fp:
                module_fp.write('# -*- coding: UTF-8 -*-\n\n')
                module_fp.write("RESOURCE_DIR = '%s'\n"%(
                    os.path.join(iobj.install_data, 'usr', 'share', 'pyrenamer')))
                module_fp.write("LOCALE_DIR = '%s'\n"%(
                    os.path.join(iobj.install_data, 'usr', 'share', 'locale')))
                #module_fp.write("LIB_DIR = '%s'\n"%(iobj.install_lib))
                module_fp.write("BIN_DIR = '%s'\n"%(iobj.install_scripts))
            return (outfile, True)
        else:
           return _build_py.copy_file(self,module_file, outfile, preserve_mode=0)

class install_data(_install_data):
    # TODO: use **kwargs, check that outdir is a dir or file
    def copy_file(self, infile, outdir):
        if infile.endswith('.in'):
            iobj = self.distribution.command_obj['install']

            resource_dir = os.path.join(iobj.install_data, 'usr', 'share', 'pyrenamer')
            locale_dir = os.path.join(iobj.install_data, 'usr', 'share', 'locale')
            bin_dir = iobj.install_scripts

            outfile = os.path.join(outdir,os.path.basename(infile[:-3]))

            with open(outfile, 'w') as module_fp:
                for line in open(infile, 'r').readlines():
                    line = line.replace('@RESOURCEDIR@',resource_dir)
                    line = line.replace('@LOCALEDIR@',locale_dir)
                    line = line.replace('@BINDIR@',bin_dir)
                    module_fp.write(line)

            return (outfile, True)

        else:
          return _install_data.copy_file(self,infile, outdir)


# This a function call, with many options. 
setup(

     cmdclass={'build_py': build_py, 'install_data': install_data},
 
    # The name of your package, as it will appear on pypi.       
    name='pyrenamer',
 
    # the version of code
    version=pyrenamer.__version__,
 
    # The list of packages to be inserted in distribution
    packages=['pyrenamer'],

    # The list of data to be inserted in distribution
    data_files = [ ('usr/share/pyrenamer', ['data/pyrenamer.glade','images/pyrenamer.png', 
                                            'images/pyrenamer.svg', 'images/stop.png']),
                   ('usr/share/gconf/schemas', ['data/pyrenamer.schemas.in']),
                   ('usr/share/application',  ['data/pyrenamer.desktop.in']),
                   ('usr/share/pixmaps', ['images/pyrenamer.png']),
                   ('usr/share/man/man1', ['doc/pyrenamer.1']),
                   ('usr/share/doc/pyrenamer', ['doc/treefilebrowser_example.py',
                                               'AUTHORS', 'ChangeLog', 'COPYING', 'NEWS', 'README', 'TODO']),
                   ('usr/share/locale/pyrenamer', ['po/ChangeLog', 'po/de.po', 'po/en.po', 'po/es.po',
                                         'po/fr.po', 'po/LINGUAS', 'po/POTFILES.in', 'po/POTFILES.skip']),
                 ],

    scripts=['pyrenamer/pyrenamer'],

    # Name of author
    author="Adolfo González Blázquez ; Eric Sagnard",
 
    # Votre email, sachant qu'il sera publique visible, avec tous les risques
    # que ça implique.
    author_email="lesametlemax@gmail.com",
 
    # Une description courte
    description="pyRenamer is an application for mass renaming files",
 
    # Une description longue, sera affichée pour présenter la lib
    # Généralement on dump le README ici
    long_description=open('README').read(),
 
    # Vous pouvez rajouter une liste de dépendances pour votre lib
    # et même préciser une version. A l'installation, Python essayera de
    # les télécharger et les installer.
    #
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    #
    # Dans notre cas on en a pas besoin, donc je le commente, mais je le
    # laisse pour que vous sachiez que ça existe car c'est très utile.
    # install_requires= ,
 
    ## Active la prise en compte du fichier MANIFEST.in
    #include_package_data=True,
 
    # Une url qui pointe vers la page officielle de votre lib
    #TODO:url='http://github.com/sametmax/sm_lib',
 
    # Il est d'usage de mettre quelques metadata à propos de sa lib
    # Pour que les robots puissent facilement la classer.
    # La liste des marqueurs autorisées est longue:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    #
    # Il n'y a pas vraiment de règle pour le contenu. Chacun fait un peu
    # comme il le sent. Il y en a qui ne mettent rien.
    classifiers=[
        "Programming Language :: Python",
        "License :: GPLv2",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
 
 
    # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
    # ce qui est notre cas
    #license="WTFPL",
 
    # Il y a encore une chiée de paramètres possibles, mais avec ça vous
    # couvrez 90% des besoins
 
)

