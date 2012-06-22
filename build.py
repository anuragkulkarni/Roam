#! /usr/bin/python
''' Build file that compiles all the needed resources'''
import os.path

from fabricate import *
import os
import sys
from shutil import copytree, ignore_patterns, rmtree
import datetime
from subprocess import Popen, PIPE

ui_sources = ['ui_datatimerpicker', 'ui_listmodules',
              'syncing/ui_sync', 'ui_listfeatures']

doc_sources = ['docs/README']

path = os.path.dirname(__file__)

ignore = ['*.pyc', 'build', '.git', '.deps', 'nbproject', 'obj',
          'Properties', '*.csproj', '*.sln', '*.suo', 'app.config',
          '*.vshost.*', '*.cs', 'make_win.bat', 'resources', '.gitignore',
          'rst*.py', 'builddocs.bat', '*.qrc', '*.log', '*.orig',
          'ui_datatimerpicker.ui', 'ui_drawingpad.ui', 'ui_listfeatures.ui',
          'ui_listmodules.ui']

# Add the path to MSBuild to PATH so that subprocess can find it.
env = os.environ.copy()
env['PATH'] += ";c:\\WINDOWS\\Microsoft.NET\Framework\\v3.5"

curpath = os.path.dirname(os.path.abspath(__file__))
buildpath = os.path.join(curpath, "build", "app", "python", "plugins", \
                            "SDRCDataCollection" )
                            
def build():
    compile()
    
def compile():
    print " - building UI files..."
    for source in ui_sources:
        run('pyuic4.bat', '-o', source+'.py', source+'.ui' )

    print " - building resource files..."
    run('pyrcc4', '-o', 'resources_rc.py', 'resources.qrc')
    run('pyrcc4', '-o', 'syncing/resources_rc.py', 'syncing/resources.qrc')
    
    print " - building sync app..."
    run('MSBuild','/property:Configuration=Release', '/verbosity:m', \
        'syncing/SyncProofConcept.csproj', shell=True, env=env)

    print " - building docs..."
    docs()
    
def docs():
    for doc in doc_sources:
        run('python', 'docs/rst2html.py', doc+'.txt', doc+'.html')

def clean():
    autoclean()

def getVersion():
    """
        Returns the version number for the plugin
    """
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    commit = shell('git', 'log', '-1', '--pretty=%h').strip()
    return "{0}.{1}.{2}.{3}".format(year, month, day, commit )

def test():
    pass

def deploy():
    print "Deploy started"
    print "Building..."
    compile()
    
    if os.path.exists(buildpath):
        print "Removing old depoly directory..."
        rmtree(buildpath)
    
    # Copy all the files to the ouput directory
    print "Copying new files..."
    copytree(curpath, buildpath, ignore=ignore_patterns(*ignore))

    # Replace version numbers
    version = getVersion()
    run("sed", '-i','s/version=0.1/version={0}/'.format(version), \
        os.path.join(buildpath, 'metadata.txt'))
        
    print "Local depoly compelete into {0}".format(buildpath)

def deploy_to(client, rebuild=True):
    if rebuild:
        deploy()

    print "Remote depolying to %s" % client
    
    buildpath = os.path.join(curpath, "build", "app")
    msg = shell('xcopy',buildpath, client, '/D', '/S', '/E', '/K', '/C', '/H', \
                                   '/R', '/Y',silent=False)
   
    print "Remote depoly compelete"

if __name__ == "__main__":
    deploy_to("\\\\sd0469\\C$\\Users\\woodrown\\Desktop\\build\\app")
    
