import os
import sys

from functools import partial

from qgis.core import QgsApplication, QgsProviderRegistry, QGis

from PyQt4.QtGui import QApplication, QFont, QIcon

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(srcpath)

import roam
import roam.environ
import roam.project
import roam.resources_rc

from configmanager.ui.configmanagerdialog import ConfigManagerDialog

import configmanager.logger as logger

logger.info("Loading Roam Config Manager")
roamapp = roam.environ.setup(sys.argv)

app = QgsApplication(sys.argv, True)
QgsApplication.setPrefixPath(roamapp.prefixpath, True)
QgsApplication.initQgis()

logger.info(QgsApplication.showSettings())
logger.info(QgsProviderRegistry.instance().pluginList())
logger.info(QgsApplication.libraryPaths())

logger.info("Roam Version: {}".format(roam.__version__))
logger.info("QGIS Version: {}".format(str(QGis.QGIS_VERSION)))

QApplication.setStyle("Plastique")
QApplication.setFont(QFont('Segoe UI'))
QApplication.setWindowIcon(QIcon(':/branding/logo'))
QApplication.setApplicationName("IntraMaps Roam Config Manager")

import roam.config
roam.config.load(roamapp.settingspath)

projectpaths = roam.environ.projectpaths(sys.argv, roamapp)
projects = list(roam.project.getProjects(projectpaths))

def excepthook(errorhandler, exctype, value, traceback):
    logger.error("Uncaught exception", exc_info=(exctype, value, traceback))
    errorhandler(exctype, value, traceback)

dialog = ConfigManagerDialog(projectpaths[0])
sys.excepthook = partial(excepthook, dialog.raiseerror)
dialog.loadprojects(projects)
dialog.show()
#dialog.showMaximized()

roamapp.exec_()
roam.config.save()
roamapp.exit()
