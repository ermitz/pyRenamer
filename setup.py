#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from distutils.core import setup
from distutils.command.build_py import build_py as _build_py
from distutils.command.install_data import install_data as _install_data
from distutils.command.install_lib import install_lib as _install_lib
from babel.messages import frontend as babel

from babel.messages.frontend import compile_catalog as _compile_catalog
from babel.messages.frontend import update_catalog as _update_catalog
from babel.messages.frontend import extract_messages as _extract_messages

from distutils import dir_util

import os 

# Note that we import the package
# you should ensure that this import has no side effect  
import pyrenamer

class extract_messages(_extract_messages):

    def initialize_options(self):
        _extract_messages.initialize_options(self)
        self.output_file = 'messages.pot'
        self.input_dirs = 'pyrenamer,data'
        self.mapping_file = 'extract.cfg'

    # TODO: generate .glade.h file

class update_catalog(_update_catalog):

    def initialize_options(self):
        _update_catalog.initialize_options(self)
        self.input_file = 'messages.pot'
        self.domain = 'pyrenamer'
        self.locale = 'fr'
        self.output_file = os.path.join ('po', '%s.po' % self.locale)

    def run(self):
        for lang in ['en','fr','es','de']:
           self.locale = lang
           self.output_file = os.path.join ('po', '%s.po' % self.locale)
           _update_catalog.run(self)


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

    def run(self):
        _build_py.run(self)

        cmd_obj = self.distribution.get_command_obj('compile_catalog', 1)
       
        for lang in ['en','fr','de','es']:
            bdir = os.path.join('build','locale', lang)
            dir_util.mkpath(bdir,dry_run=self.dry_run,verbose=self.verbose)
            cmd_obj.initialize_options()
            cmd_obj.locale = lang
            cmd_obj.use_fuzzy = True
            cmd_obj.input_file = os.path.join('po', '%s.po' % (lang))
            cmd_obj.output_file = os.path.join(bdir,'%s.mo' % self.distribution.get_name())
            cmd_obj.run()




class install_data(_install_data):
    # TODO: use **kwargs, check that outdir is a dir or file
    def copy_file(self, infile, outdir):
        if infile.endswith('.in'):
            iobj = self.distribution.command_obj['install']
            myname = self.distribution.get_name()

            resource_dir = os.path.join(iobj.install_data, 'usr', 'share', myname)
            image_dir = os.path.join(iobj.install_data, 'usr', 'share', myname)
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

    def run(self):
        _install_data.run(self)


class install_lib(_install_lib):

    def run(self):
        _install_lib.run(self)

        iobj = self.distribution.command_obj['install']
        locale_dir = os.path.join(iobj.install_data, 'usr', 'share', 'locale')

        for lang in ['en','fr','de','es']:
            bdir = os.path.join('build','locale', lang)
            infile = os.path.join(bdir, '%s.mo' % self.distribution.get_name())
            outdir = os.path.join(locale_dir,lang,'LC_MESSAGES')
            dir_util.mkpath(outdir,dry_run=self.dry_run,verbose=self.verbose)
            _install_lib.copy_file(self,infile, outdir)



# This a function call, with many options. 
setup(

     cmdclass={ 'build_py': build_py, 
                'install_data': install_data,
                'install_lib': install_lib,
                'compile_catalog': babel.compile_catalog,
                'extract_messages': extract_messages,
                'init_catalog': babel.init_catalog,
                'update_catalog': update_catalog},
 
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
                 ],

    scripts=['pyrenamer/pyrenamer'],

    # Name of author
    author="Adolfo González Blázquez ; Eric Sagnard",
 
    # Email
    author_email="ermitz888@gmail.com",
 
    # A short description 
    description="pyRenamer is an application for mass renaming files",
 
    # A long description, will be printed to present the lib  
    # We usually dump the READ here.    
    long_description=open('README').read(),
 
    # You can add a list of dependencies for your lib and even precise
    # a version. During installation, Python will try to download and   
    # install them.                       
    #
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    #
    # In our case we dont need that, so I let it commented, but I let it
    # so that you know it exists, as it is very useful. 
    # install_requires= ,
 
    # An url which points to official page of your lib.
    #TODO:url='http://github.com/sametmax/sm_lib',
 
    # It is good habits to put some metadata about the lib
    # So that bots may class it.
    # The list of possible tags is long:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "License :: GPLv2",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
 
    # To be provided only if your license is not listed in "classifiers"
    # which is not our case.
    #license="WTFPL",
)

