#!/usr/bin/python3
import os
import sys
from contextlib import suppress
from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia, uic

try:
    import qoob.backend.tools as tools
    import qoob.backend.player as player
    import qoob.backend.parser as parser
    import qoob.frontend.preferences as preferences
    import qoob.frontend.trinkets as trinkets
    import qoob.frontend.playlist as playlist
    import qoob.ui.player
except ImportError:
    import backend.tools as tools
    import backend.player as player
    import backend.parser as parser
    import frontend.preferences as preferences
    import frontend.trinkets as trinkets
    import frontend.playlist as playlist

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
DB_DIR = os.path.expanduser("~/.config/qoob/")


class LibraryTree(QtWidgets.QTreeWidget):
    selectedItem = QtCore.pyqtSignal(str)
    clearFilter = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.preferences = parent.preferences
        self.libraryView = parent.tabWidget.tabs["Library viewer"]["playlist"]
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setIndentation(10)
        self.header().setVisible(False)
        self.itemSelectionChanged.connect(self._selectItem)

    def _hasFilteredFiles(self, path):
        for root, subfolders, files in os.walk(path):
            for f in files:
                if parser.allowedType(f):
                    if self._sift(f):
                        return True
        return False

    def _recursiveScan(self, folder, node=None):
        try:
            for f in os.listdir(folder):
                path = os.path.join(folder, f)
                if os.path.isdir(path):
                    if self._hasFilteredFiles(path):
                        item = self.addItem(node, path)
                        self._recursiveScan(path, node=item)

                elif parser.allowedType(path):
                    if self._sift(f):
                        self.addItem(node, path)
        except PermissionError:
            pass

    def _scanSelection(self, path):
        for root, subfolder, files in os.walk(path):
            for f in files:
                if self._sift(f):
                    self.libraryView.add(os.path.join(root, f))
        if os.path.isfile(path):
            if self._sift(path):
                self.libraryView.add(path)

    def _selectItem(self):
        if self.selectedItems():
            self.libraryView.clear()
        for item in self.selectedItems():
            if item.text(1):
                self._scanSelection(item.text(1))
            elif item.text(0) == "All Music":
                for folder in self.preferences.get("general", "music database"):
                    self._scanSelection(folder)
            self.selectedItem.emit(item.text(1))

    def _sift(self, string):
        sift = self.parent.ui.libraryFilterLine.text()
        return string.lower().count(sift.lower()) > 0

    def addArtist(self, node):
        self.addTopLevelItem(node)
        self.sortItems(0, QtCore.Qt.AscendingOrder)

    def addItem(self, node, path):
        name = os.path.splitext(os.path.basename(path))[0]
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, path)
        try:
            if node:
                node.addChild(item)
            else:
                self.addTopLevelItem(item)
        except RuntimeError:
            pass
        return item

    def addWildCard(self):
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, "All Music")
        self.insertTopLevelItem(0, item)

    def clearAll(self):
        self.clearFilter.emit()
        self.clear()

    """
    def deleteItem(self, item, path):
        for subItem in range(item.childCount()):
            subItem = item.child(subItem)
            if subItem.childCount() > 0:
                self.deleteItem(subItem, path)
            elif subItem.text(1) == path:
                index = item.indexOfChild(subItem)
                item.takeChild(index)
                return True
        return False
    """

    def filterEvent(self):
        self.refresh()
        if self.preferences.get("viewer", "expand library"):
            count = self.topLevelItemCount()
            for item in range(self.topLevelItemCount()):
                count += self.topLevelItem(item).childCount()
            if (count * 12) <= self.height():  # Where 12px is the height of one item
                self.expandAll()
        self.sortItems(0, QtCore.Qt.AscendingOrder)
        self.addWildCard()

    def refresh(self):
        self.clear()
        for folder in self.preferences.get("general", "music database"):
            self._recursiveScan(folder)


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        if "qoob.ui.player" in sys.modules:
            self.ui = qoob.ui.player.Ui_MainWindow()
            self.ui.setupUi(self)
        else:
            self.ui = uic.loadUi(LOCAL_DIR + "ui/player.ui", self)

        self.copied = []
        self.parent = parent
        self.logger = tools.Logger(name="qoob", path=DB_DIR)
        self.log = self.logger.new("qoob")
        self.preferences = preferences.PreferencesDatabase(self)
        self._styleInit()
        self.preferencesForm = preferences.PreferencesForm(self)
        self.popup = trinkets.PopupWidget(self)
        self.process = QtCore.QProcess()
        self.random = QtCore.QRandomGenerator()
        if not self.preferences.db["general"]["music database"]:
            self._findDefaultMusicFolder()

        self.player = player.MediaPlayer(self)
        self.parser = parser.Parser(self)
        self.tabWidget = playlist.Tabs(self)
        self.library = LibraryTree(self)
        self.trayIcon = trinkets.TrayIcon(self)

        self.player.currentMediaChanged.connect(self.currentMediaChanged)
        self.player.setItemColor.connect(self.setItemColor)
        self.player.setSliderRange.connect(self.ui.playbackSlider.setRange)
        self.player.setSliderValue.connect(self.ui.playbackSlider.setValue)
        self.player.setPlayPauseIcon.connect(self.ui.playButton.setIcon)
        self.player.setShuffleIcon.connect(self.ui.shuffleButton.setIcon)
        self.player.setRepeatIcon.connect(self.ui.repeatButton.setIcon)
        self.player.setStatusMessage.connect(self.setStatusMessage)
        self.player.shuffle = self.preferences.get("state", "shuffle")
        self.player.repeat = self.preferences.get("state", "repeat")
        self.ui.volumeSlider.setValue(self.player.volume())

        self.tabWidget.keyEvent.connect(self.parseKey)
        self.tabWidget.changed.connect(self.player.clearPlaylist)
        self.library.selectedItem.connect(self.librarySelect)
        self.library.clearFilter.connect(self.ui.libraryFilterLine.clear)
        self.preferencesForm.accepted.connect(self.preferencesSave)
        self.preferencesForm.resetMetadata.connect(self.parser.reset)
        self.preferencesForm.activateWindow()

        self.parserThread = QtCore.QThread()
        self.parserThread.started.connect(self.parser.scanAll)
        self.parser.moveToThread(self.parserThread)
        self.parser.done.connect(self.libraryDone)
        self.parser.addArtist.connect(self.library.addArtist)
        self.parser.addAlbum.connect(self.library.addItem)
        self.parser.clear.connect(self.library.clearAll)
        self.parser.startDb.connect(self.preferencesForm.dbStartSlot)
        self.parser.doneDb.connect(self.preferencesForm.dbDoneSlot)
        self.parser.pending.connect(self.preferencesForm.setPending)
        self.parser.setFilterEnable.connect(self.ui.libraryFilterLine.setEnabled)
        self.parserThread.start()

        self.trayIcon.hideWindow.connect(self.hide)
        self.trayIcon.showWindow.connect(self.show)
        self.trayIcon.close.connect(self.close)
        self.trayIcon.play.connect(self.player.playPauseEvent)
        self.trayIcon.stop.connect(self.player.stopEvent)
        self.trayIcon.next.connect(self.player.nextEvent)
        self.trayIcon.previous.connect(self.player.previousEvent)
        self.trayIcon.shuffle.connect(self.player.shuffleEvent)
        self.trayIcon.showPreferencesForm.connect(self.preferencesForm.show)
        self.trayIcon.popup.connect(self.popup.display)

        self.menu = QtWidgets.QMenu()
        self.menu.aboutToShow.connect(self._menuRefresh)

        self.ui.statusBar = QtWidgets.QStatusBar()
        self.ui.statusRightLabel = QtWidgets.QLabel()

        self.ui.statusBar.addPermanentWidget(self.ui.statusRightLabel)
        self.ui.libraryLayout.insertWidget(1, self.library)
        self.ui.tabLayout.addWidget(self.tabWidget, 1, 1, 1, 8)

        self.ui.playButton.clicked.connect(self.player.playPauseEvent)
        self.ui.stopButton.clicked.connect(self.player.stopEvent)
        self.ui.nextButton.clicked.connect(self.player.nextEvent)
        self.ui.previousButton.clicked.connect(self.player.previousEvent)
        self.ui.shuffleButton.clicked.connect(self.player.shuffleEvent)
        self.ui.repeatButton.clicked.connect(self.player.repeatEvent)
        self.ui.preferencesButton.clicked.connect(self.preferencesShow)
        self.ui.refreshButton.clicked.connect(self.parser.scanAll)
        self.ui.collapseButton.clicked.connect(self.library.collapseAll)
        self.ui.expandButton.clicked.connect(self.library.expandAll)
        self.ui.libraryFilterLine.textChanged.connect(self.library.filterEvent)
        self.ui.libraryFilterClearButton.clicked.connect(self.ui.libraryFilterLine.clear)
        self.ui.volumeSlider.valueChanged.connect(self.player.setVolume)
        self.ui.playbackSlider.installEventFilter(self)
        self.ui.volumeSlider.installEventFilter(self)
        self.ui.artButton.clicked.connect(self._artViewerToggle)

        self._artInit()
        self._styleLoad()
        self.setStatusBar(self.ui.statusBar)
        self.setWindowTitle("qoob")
        self.setWindowIcon(self.icon["qoob"])
        width = self.preferences.get("state", "width")
        height = self.preferences.get("state", "height")
        self.resize(width, height)
        self.tabWidget.setFocus(True)
        self._resumePlayback()
        self.show()

    def closeEvent(self, event):
        self.preferences.db["state"]["shuffle"] = self.player.shuffle
        self.preferences.db["state"]["repeat"] = self.player.repeat
        self.preferences.db["state"]["volume"] = self.player.volume()
        self.preferences.db["state"]["tab"] = self.tabWidget.tabBar().currentIndex()
        self.preferences.db["state"]["playback position"] = self.player.position()
        self.preferences.db["state"]["media state"] = self.player.state()
        self.preferences.db["state"]["file"] = self.player.path
        self.preferences.db["state"]["width"] = self.width()
        self.preferences.db["state"]["height"] = self.height()
        self.preferences.save()
        self.tabWidget.playlistSave()
        self.parent.exit()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            mouseEvent = QtGui.QMouseEvent(event)
            position = QtWidgets.QStyle.sliderValueFromPosition(obj.minimum(), obj.maximum(), mouseEvent.x(), obj.width())
            obj.setValue(position)
            if obj == self.ui.playbackSlider:
                self.player.setPosition(obj.value())
        return QtCore.QObject.event(obj, event)

    def changeEvent(self, event):
        # Override minimize event
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                if self.preferences.get("general", "tray minimize") and self.preferences.get("general", "tray icon"):
                    self.setWindowState(QtCore.Qt.WindowNoState)
                    self.hide() if self.isVisible() else self.show()

    def _artDisplay(self):
        if self.preferences.get("art", "enable"):
            size = self.preferences.get("art", "size")
            if self.art.isNull():
                art = self.icon["qoob"].pixmap(64, 64)
                self.ui.artFrame.setVisible(self.preferences.get("art", "show empty"))
            else:
                aspectRatio = QtCore.Qt.IgnoreAspectRatio
                smooth = QtCore.Qt.SmoothTransformation
                art = self.art.scaled(size, size, aspectRatio, transformMode=smooth)
                self.ui.artFrame.setVisible(True)
            self.ui.artLabel.setFixedSize(size, size)
            self.ui.artLabel.setPixmap(art)

    def _artInit(self):
        size = self.preferences.get("art", "size")
        art = self.icon["qoob"].pixmap(size, size)
        self.art = QtGui.QPixmap(None)
        self.ui.artLabel.setPixmap(art)
        self.ui.artFrame.setVisible(self.preferences.get("art", "show empty") and self.preferences.get("art", "enable"))
        if self.preferences.get("art", "enable"):
            self.ui.artButton.setIcon(self.icon["art_on"])
        else:
            self.ui.artButton.setIcon(self.icon["art_off"])

    def _artLoad(self, path):
        self.art = self.parser.art(path)

    def _artViewerToggle(self):
        if self.preferences.get("art", "enable"):
            self.preferences.db["art"]["enable"] = False
            self.ui.artButton.setIcon(self.icon["art_off"])
            self.ui.artFrame.setVisible(False)
        else:
            self.preferences.db["art"]["enable"] = True
            self.ui.artButton.setIcon(self.icon["art_on"])
            self._artDisplay()
        self.preferences.save()

    def _delete(self, files):
        self.action("delete")
        for f in files:
            if os.path.isfile(f):
                os.remove(f)

            # Remove empty folder
            if self.preferences.get("general", "clean folder"):
                parent = os.path.abspath(os.path.join(f, os.pardir))
                if len(os.listdir(parent)) == 0:
                    os.rmdir(parent)
                    self.library.refresh()
                    self.library.addWildCard()
                    return

            """
            # Remove item from library tree
            for item in range(self.library.topLevelItemCount()):
                item = self.library.topLevelItem(item)
                if self.library.deleteItem(item, f):
                    break
            """

    def _deletePrompt(self, files):
        if self.preferences.get("general", "delete confirm"):
            names = ""
            for f in files:
                names += "\n" + os.path.basename(f)
            msg = QtWidgets.QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Delete confirmation")
            msg.setText(f"Please confirm deletion of :\n{names}")
            msg.setStandardButtons(QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
            if msg.exec_() == QtWidgets.QMessageBox.Apply:
                self._delete(files)
        else:
            self._delete(files)

    def _findDefaultMusicFolder(self):
        xdgDirectories = os.path.expanduser("~/.config/user-dirs.dirs")
        if os.path.isfile(xdgDirectories):
            with open(xdgDirectories) as f:
                for line in f.read().splitlines():
                    line = line.split("=")
                    if line[0] == "XDG_MUSIC_DIR":
                        musicFolder = line[1].replace("$HOME", "~")
                        musicFolder = os.path.expanduser(musicFolder[1:-1])
                        self.preferences.db["general"]["music database"].append(musicFolder)
                        self.preferences.save()
                        break

    def _styleInit(self):
        # Init icons
        iconTheme = self.preferences.get("general", "icon theme")
        iconPath = f"{LOCAL_DIR}icons/{iconTheme}/"
        self.icon = {}
        for icon in os.listdir(iconPath):
            iconName = os.path.splitext(icon)
            if iconName[1] == ".svg":
                self.icon[iconName[0]] = QtGui.QIcon(f"{iconPath}{icon}")

        # Init stylesheet
        stylesheet = f"QPushButton#libraryFilterClearButton {{ border-image: url({iconPath}filter_clear.svg); }}\n"
        stylesheet += f"QPushButton#libraryFilterClearButton:hover {{ border-image: url({iconPath}filter_hover.svg); }}"
        self.ui.libraryFilterClearButton.setStyleSheet(stylesheet)

    def _styleLoad(self):
        self.ui.playButton.setIcon(self.icon["play"])
        self.ui.stopButton.setIcon(self.icon["stop"])
        self.ui.nextButton.setIcon(self.icon["next"])
        self.ui.previousButton.setIcon(self.icon["previous"])
        self.ui.preferencesButton.setIcon(self.icon["preferences"])
        self.ui.refreshButton.setIcon(self.icon["refresh"])
        self.ui.collapseButton.setIcon(self.icon["collapse"])
        self.ui.expandButton.setIcon(self.icon["expand"])

        icon = {0: "repeat_off", 1: "repeat_all", 2: "repeat_single"}
        stateIcon = icon[self.player.repeat]
        self.ui.repeatButton.setIcon(self.icon[stateIcon])

        if self.player.shuffle:
            self.ui.shuffleButton.setIcon(self.icon["shuffle_on"])
        else:
            self.ui.shuffleButton.setIcon(self.icon["shuffle_off"])

        if self.preferences.get("art", "enable"):
            self.ui.artButton.setIcon(self.icon["art_on"])
        else:
            self.ui.artButton.setIcon(self.icon["art_off"])

    def _menuRefresh(self):
        self.menu.clear()
        if self.copied:
            self.menu.addAction(self.icon["paste"], "Paste selection", lambda: self.action("paste"))
        if self.tabWidget.current.selectedItems():
            self.menu.addAction(self.icon["cut"], "Cut selection", lambda: self.action("cut"))
            self.menu.addAction(self.icon["copy"], "Copy selection", lambda: self.action("copy"))
            if self.preferences.get("general", "file manager"):
                self.menu.addAction(self.icon["folder"], "Browse song folder", lambda: self.action("browse"))
            self.menu.addSeparator()
            self.menu.addAction(self.icon["remove"], "Delete from playlist", lambda: self.action("delete"))
            self.menu.addAction(self.icon["delete"], "Delete from disk", lambda: self.action("delete prompt"))

    def _resumePlayback(self):
        self.player.resumePlayback = self.preferences.get("general", "resume playback")
        playing = self.preferences.get("state", "media state") == QtMultimedia.QMediaPlayer.PlayingState
        if self.player.resumePlayback and playing:
            self.player.setCurrentMedia(self.preferences.get("state", "file"))

    def _titleFormat(self, title):
        replace = ("artist", "album", "track", "title")
        for tag in replace:
            title = title.replace("%" + tag + "%", self.player.tags[tag])
        return title

    def action(self, action):
        currentTab = self.tabWidget.current
        selection = currentTab.selectedItems()
        if action == "paste" and self.copied:
            for path in self.copied:
                item = currentTab.add(path)

            # Select pasted item
            currentTab.clearSelection()
            currentTab.setCurrentItem(item)

        elif selection:
            files = []
            for item in selection:
                files.append(item.text(5))

            if action == "copy":
                self.copied = files

            if action == "cut":
                self.copied = files
                for item in selection:
                    index = currentTab.indexOfTopLevelItem(item)
                    currentTab.takeTopLevelItem(index)

            elif action == "delete":
                for item in selection:
                    index = currentTab.indexOfTopLevelItem(item)
                    currentTab.takeTopLevelItem(index)
                self.player.nextEvent()

            elif action == "delete prompt":
                self._deletePrompt(files)

            elif action == "browse":
                folder = os.path.abspath(os.path.join(currentTab.currentItem().text(5), os.pardir))
                cmd = f'{self.preferences.get("general", "file manager")} "{folder}"'
                self.process.startDetached(cmd)

    def currentMediaChanged(self, path):
        titlePopup = self._titleFormat(self.preferences.get("viewer", "notification format"))
        titleWindow = self._titleFormat(self.preferences.get("viewer", "title format"))
        titleTooltip = self._titleFormat(self.preferences.get("viewer", "tooltip format"))
        self.popup.display(titlePopup)
        self.setWindowTitle(titleWindow)
        self.trayIcon.setToolTip(titleTooltip)
        self._artLoad(path)
        if self.preferences.get("art", "media trigger"):
            self._artDisplay()

    def libraryDone(self):
        self.library.addWildCard()

    def librarySelect(self, path):
        self.player.lastPlayed = []
        self.tabWidget.current.sort()
        self.tabWidget.tabBar().setCurrentIndex(0)
        self._artLoad(path)
        if self.preferences.get("art", "library trigger"):
            self._artDisplay()

    def menuShow(self):
        if self.tabWidget.current.selectedItems() or self.copied:
            self.menu.popup(QtGui.QCursor.pos())

    def parseCommands(self, cmd):
        if "delete" in cmd:
            self.action("delete prompt")

        elif "delete-no-confirm" in cmd:
            self.action("delete")

        if "shuffle" in cmd:
            if len(cmd["shuffle"]) > 0:
                if cmd["shuffle"][0] == "on":
                    self.player.shuffleEvent(enable=True)
                elif cmd["shuffle"][0] == "off":
                    self.player.shuffleEvent(enable=False)
            else:
                self.player.shuffleEvent()
            self.popup.display("Shuffle enabled" if self.player.shuffle else "Shuffle disabled")

        if "repeat" in cmd:
            if len(cmd["repeat"]) > 0:
                states = {"off": 0, "all": 1, "single": 2}
                arg = cmd["repeat"][0]
                self.player.repeatEvent(state=states[arg])
            else:
                self.player.repeatEvent()
            states = {0: "off", 1: "all", 2: "single"}
            self.popup.display(f"Repeat {states[self.player.repeat]}")

        if "clear" in cmd:
            self.tabWidget.tabs["Library viewer"]["playlist"].clear()

        if "file" in cmd:
            if len(cmd["file"]) == 0:
                return False
            for f in cmd["file"]:
                if os.path.isfile(f):
                    item = self.tabWidget.tabs["Library viewer"]["playlist"].add(f)
            self.tabWidget.tabBar().setCurrentIndex(0)
            self.tabWidget.tabs["Library viewer"]["playlist"].sort()
            self.tabWidget.tabs["Library viewer"]["playlist"].setCurrentItem(item)

        if "folder" in cmd:
            if len(cmd["folder"]) == 0:
                return False
            for folder in cmd["folder"]:
                if os.path.isdir(folder):
                    for root, subfolder, files in os.walk(folder):
                        for f in files:
                            self.tabWidget.tabs["Library viewer"]["playlist"].add(f"{root}/{f}")
            self.tabWidget.tabBar().setCurrentIndex(0)
            self.tabWidget.tabs["Library viewer"]["playlist"].sort()

        if "stop" in cmd:
            self.player.stopEvent()

        if "previous" in cmd:
            self.player.previousEvent()

        if "next" in cmd:
            self.player.nextEvent()

        if "play" in cmd:
            self.player.playEvent()

        if "play-pause" in cmd:
            self.player.playPauseEvent()

        if "pause" in cmd:
            self.player.pauseEvent()

        if "quit" in cmd:
            self.close()

    def parseKey(self, modifier, key):
        ctrl = (modifier == QtCore.Qt.ControlModifier)
        if ctrl and key == QtCore.Qt.Key_C:
            self.action("copy")
        elif ctrl and key == QtCore.Qt.Key_X:
            self.action("cut")
        elif ctrl and key == QtCore.Qt.Key_V:
            self.action("paste")
        elif key == QtCore.Qt.Key_Left:
            self.player.skip(-5)
        elif key == QtCore.Qt.Key_Right:
            self.player.skip(5)
        elif key == QtCore.Qt.Key_Backspace:
            self.action("delete")
        elif key == QtCore.Qt.Key_Delete:
            self.action("delete prompt")
        elif key == QtCore.Qt.Key_Space:
            self.player.playPauseEvent()

    def preferencesSave(self):
        self.preferencesForm.settingsSave()
        oldDb = self.preferences.get("general", "music database")
        newDb = self.preferencesForm.db["general"]["music database"]
        changedDb = not oldDb == newDb

        self.preferences.db = tools.copyDict(self.preferencesForm.db)
        self.preferences.save()

        for path in oldDb:
            if path not in newDb:
                self.parser.removeDatabase(path)
        if changedDb:
            QtCore.QMetaObject.invokeMethod(self.parser, "scanAll", QtCore.Qt.QueuedConnection)

        self._styleInit()
        self._styleLoad()
        self._artDisplay()
        self.player.icon = self.icon
        self.tabWidget.initStyle()
        self.popup.updateView()
        if self.preferences.get("general", "tray icon"):
            self.trayIcon.show()
        else:
            self.trayIcon.hide()

    def preferencesShow(self):
        self.preferencesForm.show()
        self.preferencesForm.raise_()

    def setItemColor(self, color):
        current = self.tabWidget.current.currentItem()
        if current:
            self.tabWidget.current.currentItem().setColor(color)

    def setStatusMessage(self, left, right):
        if left:
            self.ui.statusBar.showMessage(left)
        if right:
            self.ui.statusRightLabel.setText(right)


def main(cmd=""):
    app = QtWidgets.QApplication([''])
    app.setQuitOnLastWindowClosed(False)
    gui = Main(app)
    gui.parseCommands(cmd)
    bus = tools.QDBusObject(parent=gui)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
