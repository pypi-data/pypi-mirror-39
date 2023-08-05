#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pickle
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pyqtgraph as pg
import cryio
import decor
from .tools import autoLevels
from .ui.wmask import Ui_WMask


MASK_EXT = '.bmsk'


class WMask(QtWidgets.QDialog, Ui_WMask):
    sigMask = QtCore.pyqtSignal(str)

    def __init__(self, itype, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.lessEdit.setValidator(QtGui.QIntValidator())
        self.moreEdit.setValidator(QtGui.QIntValidator())
        self.itype = itype
        self.beamline = ''
        self.roi = []
        self.data = None

    def saveSettings(self):
        s = QtCore.QSettings()
        s.setValue('WMask/Geometry', self.saveGeometry())
        s.setValue('WMask/less', self.lessEdit.text())
        s.setValue('WMask/more', self.moreEdit.text())
        s.setValue('WMask/folder', self.folder)

    def loadSettings(self):
        s = QtCore.QSettings()
        self.restoreGeometry(s.value('WMask/Geometry', b''))
        self.lessEdit.setText(s.value('WMask/less', '0', str))
        self.moreEdit.setText(s.value('WMask/more', '0', str))
        self.folder = s.value('WMask/folder', '', str)

    def closeEvent(self, event):
        self.saveSettings()

    def changeBeamline(self, beamline):
        self.beamline = beamline

    @QtCore.pyqtSlot()
    def on_openImageButton_clicked(self):
        extensions = ' *'.join(cryio.extensions())
        image = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image file', self.folder,
                                                      f'Frames (*{extensions} *{MASK_EXT})')[0]
        if not image:
            return
        self.folder = os.path.dirname(image)
        if image.endswith(MASK_EXT):
            return self.openBubbleMask(image)
        try:
            img = cryio.openImage(image).array
        except cryio.ImageError as err:
            return QtWidgets.QMessageBox.critical(self, 'Image error', f'Could open image: {err}')
        self.setData(decor.correctImage(self.beamline, self.itype, img), image)

    def setData(self, data, name):
        self.data = data
        self.imageView.setImage(data)
        self.imageView.setLevels(*autoLevels(data))
        self.setWindowTitle(f'Mask - {name}')

    def getImageCenter(self):
        ranges = self.imageView.getView().getState()['viewRange']
        return ranges[0][1] // 2, ranges[1][1] // 2

    @QtCore.pyqtSlot()
    def on_polyButton_clicked(self):
        xc, yc = self.getImageCenter()
        self.addRoi(PolyLineROI([[xc, yc], [xc - 100, yc - 100], [xc - 100, yc + 100]], closed=True, removable=True))

    @QtCore.pyqtSlot()
    def on_ellipseButton_clicked(self):
        xc, yc = self.getImageCenter()
        self.addRoi(EllipseROI([xc, yc], [100, 100], removable=True))

    @QtCore.pyqtSlot()
    def on_buttonCircle_clicked(self):
        xc, yc = self.getImageCenter()
        self.addRoi(CircleROI([xc, yc], [100, 100], removable=True))

    def addRoi(self, roi):
        self.roi.append(roi)
        self.imageView.getView().addItem(roi)
        roi.sigRemoveRequested.connect(self.removeRoi)

    def removeRoi(self, roi):
        self.imageView.getView().removeItem(roi)
        self.roi.remove(roi)

    def makeMaskArray(self):
        if self.data is None:
            return
        image = self.imageView.getImageItem()
        func = np.zeros
        for roi in self.roi:
            if roi.inverted():
                func = np.ones
                break
        mask = func(self.data.shape, dtype=np.int8)
        for roi in self.roi:
            array, coords = roi.getArrayRegion(self.data, image)
            if array is None:
                continue
            xc, yc = np.round(coords).astype(np.int32)
            xc1, yc1 = xc + 1, yc + 1
            xc2, yc2 = xc - 1, yc - 1
            s1, s2 = mask.shape[0] - 1, mask.shape[1] - 1
            xc[xc > s1] = s1
            yc[yc > s2] = s2
            xc1[xc1 > s1] = s1
            yc1[yc1 > s2] = s2
            xc2[xc2 > s1] = s1
            yc2[yc2 > s2] = s2
            xc[xc < 0] = 0
            xc1[xc1 < 0] = 0
            xc2[xc2 < 0] = 0
            xc[xc < 0] = 0
            xc1[xc1 < 0] = 0
            xc2[xc2 < 0] = 0
            array[array != 0] = 1
            if roi.inverted():
                array = 1 - array
            mask[xc, yc] = array
            mask[xc1, yc1] = array
            mask[xc2, yc2] = array
        less, more = self.getLessMore()
        if less is not None:
            mask[self.data <= less] = 1
        if more is not None:
            mask[self.data >= more] = 1
        return mask

    def getLessMore(self):
        less, more = None, None
        if self.lessCheckbox.isChecked():
            less = int(self.lessEdit.text())
        if self.moreCheckbox.isChecked():
            more = int(self.moreEdit.text())
        return less, more

    def openBubbleMask(self, name: str):
        try:
            f = open(name, 'rb')
            froi = pickle.load(f)
        except (OSError, pickle.UnpicklingError) as err:
            return QtWidgets.QMessageBox.critical(self, 'Mask error', f'Cannot open mask: {err}')
        f.close()
        self.setData(froi['frame'], name)
        if froi['less']:
            self.lessEdit.setText(str(froi['less']))
        if froi['more']:
            self.moreEdit.setText(str(froi['more']))
        for state in froi['roi']:
            roi = InvertibleROI.getROIByState(state)
            if not roi:
                continue
            self.addRoi(roi)
            roi.setState(state)

    def saveBubbleMask(self, name):
        mask = self.makeMaskArray()
        less, more = self.getLessMore()
        roi = []
        for r in self.roi:
            state = r.saveState()
            roi.append(state)
        try:
            f = open(name, 'wb')
        except OSError as err:
            return QtWidgets.QMessageBox.critical(self, 'Mask error', f'Could not save mask: {err}')
        msk = {'roi': roi, 'less': less, 'more': more, 'mask': mask, 'frame': self.data}
        pickle.dump(msk, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        self.sigMask.emit(name)

    @QtCore.pyqtSlot()
    def on_applyButton_clicked(self):
        if self.data is None:
            return
        self.saveBubbleMask(tempfile.mkstemp(suffix=MASK_EXT)[1])
        self.close()

    @QtCore.pyqtSlot()
    def on_clearButton_clicked(self):
        for roi in self.roi:
            self.imageView.getView().removeItem(roi)
        self.imageView.clear()
        self.setWindowTitle('Mask')
        self.data = None
        self.roi = []

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_saveMaskButton_clicked(self):
        if self.data is None:
            return
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save mask', self.folder, f'Bubble mask (*{MASK_EXT})')[0]
        if not name:
            return
        if not name.endswith(MASK_EXT):
            name = f'{name}{MASK_EXT}'
        self.saveBubbleMask(name)


class InvertibleROI:
    def __init__(self):
        self.invertedMask = False
        self.actionInvert = None

    def getMenu(self):
        if not self.actionInvert:
            self.actionInvert = QtWidgets.QAction('Invert mask ROI', self.menu)
            self.actionInvert.setCheckable(True)
            self.actionInvert.setChecked(self.invertedMask)
            # noinspection PyUnresolvedReferences
            self.actionInvert.triggered.connect(self.setInverted)
            self.menu.addAction(self.actionInvert)
        return self.menu

    def setInverted(self, checked):
        self.invertedMask = checked

    def setState(self, state):
        if 'invert' in state:
            self.invertedMask = state['invert']
            if self.actionInvert:
                self.actionInvert.setChecked(state['invert'])

    def saveStateI(self, state):
        state['invert'] = self.invertedMask

    def inverted(self):
        return self.invertedMask

    @staticmethod
    def getROIByState(state):
        if 'type' in state:
            if state['type'] == 'PolyLineROI':
                return PolyLineROI([[1, 1], [0, 0], [0, 2]], closed=True, removable=True)
            elif state['type'] == 'EllipseROI':
                return EllipseROI([0, 0], [1, 1], removable=True)
            elif state['type'] == 'CircleROI':
                return CircleROI([0, 0], [1, 1], removable=True)


class PolyLineROI(pg.PolyLineROI, InvertibleROI):
    def __init__(self, positions, closed=False, pos=None, **args):
        super().__init__(positions, closed, pos, **args)
        self.type = 'PolyLineROI'

    def getArrayRegion(self, data, img, axes=(0, 1), **kwds):
        s, m = pg.ROI.getArrayRegion(self, data, img, axes=axes, fromBoundingRect=True, returnMappedCoords=True, **kwds)
        if s is None:
            return None, None
        if img.axisOrder == 'col-major':
            mask = self.renderShapeMask(s.shape[axes[0]], s.shape[axes[1]])
        else:
            mask = self.renderShapeMask(s.shape[axes[1]], s.shape[axes[0]])
            mask = mask.T
        shape = [1] * data.ndim
        shape[axes[0]] = s.shape[axes[0]]
        shape[axes[1]] = s.shape[axes[1]]
        mask = mask.reshape(shape)
        return s * mask, m

    def saveState(self):
        state = super().saveState()
        state['type'] = self.type
        self.saveStateI(state)
        return state

    def getMenu(self):
        super().getMenu()
        return InvertibleROI.getMenu(self)

    def setState(self, state):
        super().setState(state)
        InvertibleROI.setState(self, state)


class EllipseROI(pg.EllipseROI, InvertibleROI):
    def __init__(self, pos, size, **args):
        super().__init__(pos, size, **args)
        self.type = 'EllipseROI'

    def getArrayRegion(self, arr, img=None, axes=(0, 1), **kwds):
        arr, m = pg.ROI.getArrayRegion(self, arr, img, axes, returnMappedCoords=True, **kwds)
        if arr is None or arr.shape[axes[0]] == 0 or arr.shape[axes[1]] == 0:
            return None, None
        w = arr.shape[axes[0]]
        h = arr.shape[axes[1]]
        mask = np.fromfunction(
            lambda x, y: (((x + 0.5) / (w / 2) - 1) ** 2 + ((y + 0.5) / (h / 2) - 1) ** 2) ** 0.5 < 1, (w, h))
        if axes[0] > axes[1]:
            mask = mask.T
        shape = [(n if i in axes else 1) for i, n in enumerate(arr.shape)]
        mask = mask.reshape(shape)
        mask = arr * mask
        return mask, m

    def saveState(self):
        state = super().saveState()
        state['type'] = self.type
        self.saveStateI(state)
        return state

    def getMenu(self):
        super().getMenu()
        return InvertibleROI.getMenu(self)

    def setState(self, state, update=True):
        super().setState(state, update)
        InvertibleROI.setState(self, state)


class CircleROI(EllipseROI):
    def __init__(self, pos, size, **args):
        super().__init__(pos, size, **args)
        self.aspectLocked = True
        self.addScaleHandle([0.5 * 2. ** -0.5 + 0.5, 0.5 * 2. ** -0.5 + 0.5], [0.5, 0.5])
        self.type = 'CircleROI'
