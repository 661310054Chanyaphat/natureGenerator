try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import os
import random

IMAGE_DIR = 'C:/Users/user/Documents/maya/2024/scripts/natureGenerator/icons'
MODEL_DIR = 'C:/Users/user/Documents/maya/2024/scripts/natureGenerator/models'


class NatureGeneratorToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Nature Generator Tool')
        self.resize(400, 420)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.setStyleSheet('''
            QDialog { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #257278, stop:1 #8ADAE3) }
            QLabel { font-family: Arial; color: #FFFFFF; }
            QLineEdit { background-color: #247982; border: 1.5px solid #194F54; border-radius: 6px; padding: 3px 6px; color: white; }
            QPushButton { background-color: #2E6670; color: white; font-weight: bold; border-radius: 10px; padding: 8px; }
            QPushButton:hover { background-color: #66BB6A; }
            QPushButton:pressed { background-color: #388E3C; }
            QCheckBox { color: white; font-weight: bold; }
            QComboBox { background-color: #3E9C9E; color: white; border: 1.5px solid #2E6670; border-radius: 6px; padding: 2px 5px; }
        ''')

        titleLabel = QtWidgets.QLabel("🌿 Nature Generator Tool")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.mainLayout.addWidget(titleLabel)

        imageLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(imageLayout)

        self.checkboxes = {}
        self.model_files = {
            "Tree": "tree.ma",
            "Flower": "flower.ma",
            "Grass": "grass.ma",
            "Rock": "rock.ma"
        }

        icons = [
            ("Tree", "tree.png"),
            ("Flower", "flower.png"),
            ("Grass", "grass.png"),
            ("Rock", "rock.png")
        ]

        for name, img in icons:
            vbox = QtWidgets.QVBoxLayout()

            img_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(os.path.join(IMAGE_DIR, img))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                img_label.setPixmap(pixmap)
            img_label.setAlignment(QtCore.Qt.AlignCenter)

            check = QtWidgets.QCheckBox(name)
            check.setChecked(False)

            vbox.addWidget(img_label)
            vbox.addWidget(check, alignment=QtCore.Qt.AlignCenter)

            imageLayout.addLayout(vbox)
            self.checkboxes[name] = check

        themeLayout = QtWidgets.QHBoxLayout()
        themeLabel = QtWidgets.QLabel("Select Theme:")
        themeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))

        themeCombo = QtWidgets.QComboBox()
        themeCombo.addItems(["Spring", "Autumn", "Winter"])
        themeCombo.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        themeLayout.addWidget(themeLabel)
        themeLayout.addWidget(themeCombo)
        self.mainLayout.addLayout(themeLayout)

        self.selected_theme_combo = themeCombo

        gridLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(gridLayout)

        def make_row(label_text, row, has_range=False, placeholder=""):
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            gridLayout.addWidget(label, row, 0)

            if has_range:
                minEdit = QtWidgets.QLineEdit()
                minEdit.setPlaceholderText("min")
                maxEdit = QtWidgets.QLineEdit()
                maxEdit.setPlaceholderText("max")
                toLabel = QtWidgets.QLabel("to")
                toLabel.setAlignment(QtCore.Qt.AlignCenter)
                gridLayout.addWidget(minEdit, row, 1)
                gridLayout.addWidget(toLabel, row, 2)
                gridLayout.addWidget(maxEdit, row, 3)
                return minEdit, maxEdit
            else:
                edit = QtWidgets.QLineEdit()
                edit.setPlaceholderText(placeholder)
                gridLayout.addWidget(edit, row, 1, 1, 3)
                return edit

        self.objCountEdit = make_row("Object Count:", 0)
        self.boundXMin, self.boundXMax = make_row("Boundary X:", 1, True)
        self.boundZMin, self.boundZMax = make_row("Boundary Z:", 2, True)
        self.minDistEdit = make_row("Distance:", 3)
        self.scaleMin, self.scaleMax = make_row("Scale Range:", 4, True)

        self.generateBtn = QtWidgets.QPushButton("Generate Objects")
        self.mainLayout.addWidget(self.generateBtn)
        self.mainLayout.addStretch()

        self.generateBtn.clicked.connect(self.generate_objects)

    
    def generate_objects(self):
        try:
            obj_count = int(self.objCountEdit.text())
        except:
            cmds.warning("Please enter a valid object count.")
            return

        try:
            x_min = float(self.boundXMin.text())
            x_max = float(self.boundXMax.text())
            z_min = float(self.boundZMin.text())
            z_max = float(self.boundZMax.text())
        except:
            cmds.warning("Please enter valid boundary values.")
            return

        try:
            scale_min = float(self.scaleMin.text())
            scale_max = float(self.scaleMax.text())
        except:
            scale_min = 1.0
            scale_max = 1.0

        try:
            min_distance = float(self.minDistEdit.text())
        except:
            min_distance = 0.0

        theme = self.selected_theme_combo.currentText()
        selected_types = [name for name, check in self.checkboxes.items() if check.isChecked()]

        if not selected_types:
            cmds.warning("Please select at least one object type.")
            return

        cmds.undoInfo(openChunk=True)
        created_objs = []

        try:
            for i in range(obj_count):
                obj_type = random.choice(selected_types)
                maya_file = os.path.join(MODEL_DIR, self.model_files[obj_type])

                if not os.path.exists(maya_file):
                    cmds.warning(f"Model not found: {maya_file}")
                    continue

                if maya_file.endswith((".ma", ".mb")):
                    imported = cmds.file(maya_file, i=True, ignoreVersion=True, ra=True,
                                         mergeNamespacesOnClash=False, options="v=0;", pr=True, returnNewNodes=True)
                else:
                    imported = cmds.file(maya_file, i=True, type="FBX", ignoreVersion=True, ra=True,
                                         mergeNamespacesOnClash=False, options="fbx", pr=True, returnNewNodes=True)

                new_objs = cmds.ls(imported, transforms=True)
                if not new_objs:
                    continue

                obj = new_objs[0]

                pos_x = random.uniform(x_min, x_max)
                pos_z = random.uniform(z_min, z_max)
                pos_y = 0
                scale = random.uniform(scale_min, scale_max)

                cmds.move(pos_x, pos_y, pos_z, obj)
                cmds.scale(scale, scale, scale, obj)
                created_objs.append(obj)

        except Exception as e:
            cmds.warning(f"Error during generation: {e}")
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_objs:
            cmds.select(created_objs)
            cmds.inViewMessage(amg=f"<hl>{len(created_objs)} objects created!</hl>",
                               pos='midCenter', fade=True)


def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = NatureGeneratorToolDialog(parent=ptr)
    ui.show()
