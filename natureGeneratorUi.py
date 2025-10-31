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
import sys

script_dir = r"C:/Users/user/Documents/maya/2024/scripts/natureGenerator"
if script_dir not in sys.path:
    sys.path.append(script_dir)

import importlib
import natureGeneratorUtil as utils
importlib.reload(utils)

IMAGE_DIR = 'C:/Users/user/Documents/maya/2024/scripts/natureGenerator/icons'
MODEL_DIR = 'C:/Users/user/Documents/maya/2024/scripts/natureGenerator/models'

class NatureGeneratorToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Nature Generator Tool')
        self.resize(400, 450)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.mainLayout)

       
        top_image_path = os.path.join(IMAGE_DIR, "top.png")
        if os.path.exists(top_image_path):
            top_label = QtWidgets.QLabel()
            pix = QtGui.QPixmap(top_image_path)
            pix = pix.scaledToWidth(380, QtCore.Qt.SmoothTransformation)
            top_label.setPixmap(pix)
            top_label.setAlignment(QtCore.Qt.AlignCenter)
            self.mainLayout.addWidget(top_label)

        
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
        self.model_files = {"Tree": "tree.ma", "Flower": "flower.ma", "Grass": "grass.ma", "Rock": "rock.ma"}
        icons = [("Tree","tree.png"), ("Flower","flower.png"), ("Grass","grass.png"), ("Rock","rock.png")]
        for name,img in icons:
            vbox = QtWidgets.QVBoxLayout()
            img_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(os.path.join(IMAGE_DIR, img))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(80,80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
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
        themeCombo.addItems(["Spring","Autumn","Winter"])
        themeCombo.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        themeLayout.addWidget(themeLabel)
        themeLayout.addWidget(themeCombo)
        self.mainLayout.addLayout(themeLayout)
        self.selected_theme_combo = themeCombo

        
        gridLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(gridLayout)
        def make_row(label_text,row,has_range=False,placeholder=""):
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial",10,QtGui.QFont.Bold))
            gridLayout.addWidget(label,row,0)
            if has_range:
                minEdit = QtWidgets.QLineEdit()
                minEdit.setPlaceholderText("min")
                maxEdit = QtWidgets.QLineEdit()
                maxEdit.setPlaceholderText("max")
                toLabel = QtWidgets.QLabel("to")
                toLabel.setAlignment(QtCore.Qt.AlignCenter)
                gridLayout.addWidget(minEdit,row,1)
                gridLayout.addWidget(toLabel,row,2)
                gridLayout.addWidget(maxEdit,row,3)
                return minEdit,maxEdit
            else:
                edit = QtWidgets.QLineEdit()
                edit.setPlaceholderText(placeholder)
                gridLayout.addWidget(edit,row,1,1,3)
                return edit

        self.objCountEdit = make_row("Object Count:",0)
        self.boundXMin,self.boundXMax = make_row("Boundary X:",1,True)
        self.boundZMin,self.boundZMax = make_row("Boundary Z:",2,True)
        self.minDistEdit = make_row("Distance:",3)
        self.scaleMin,self.scaleMax = make_row("Scale Range:",4,True)

       
        self.snapToSurfaceCheck = QtWidgets.QCheckBox("Snap to Surface (Top of Mesh)")
        self.snapToSurfaceCheck.setChecked(False)
        self.snapToSurfaceCheck.setStyleSheet("QCheckBox { color: white; font-weight: bold; }")
        self.mainLayout.addWidget(self.snapToSurfaceCheck)

     
        self.add_use_selection_button()

        self.generateBtn = QtWidgets.QPushButton("Generate Objects")
        self.mainLayout.addWidget(self.generateBtn)
        self.mainLayout.addStretch()
        self.generateBtn.clicked.connect(self.generate_objects)

 
        bottom_image_path = os.path.join(IMAGE_DIR, "bottom.png")  
        if os.path.exists(bottom_image_path):
            bottom_label = QtWidgets.QLabel()
            pix = QtGui.QPixmap(bottom_image_path)
            pix = pix.scaledToWidth(380, QtCore.Qt.SmoothTransformation)
            bottom_label.setPixmap(pix)
            bottom_label.setAlignment(QtCore.Qt.AlignCenter)
            self.mainLayout.addWidget(bottom_label)

    def add_use_selection_button(self):
        useSelectionBtn = QtWidgets.QPushButton("Use Selection as Boundary")
        useSelectionBtn.setStyleSheet('''
            QPushButton { background-color: #468C91; color: white; font-weight: bold; border-radius: 8px; padding: 6px; }
            QPushButton:hover { background-color: #6AC7A1; }
            QPushButton:pressed { background-color: #388E3C; }
        ''')
        useSelectionBtn.clicked.connect(self.use_selection_as_boundary)
        self.mainLayout.addWidget(useSelectionBtn)  # ต่อท้าย Snap checkbox โดยอัตโนมัติ
        self.useSelectionBtn = useSelectionBtn

    def use_selection_as_boundary(self):
        sel = cmds.ls(selection=True)
        if not sel: cmds.warning("Select object for boundary"); return
        try:
            bbox = cmds.exactWorldBoundingBox(sel)
            self.boundXMin.setText(f"{bbox[0]:.2f}")
            self.boundXMax.setText(f"{bbox[3]:.2f}")
            self.boundZMin.setText(f"{bbox[2]:.2f}")
            self.boundZMax.setText(f"{bbox[5]:.2f}")
            cmds.inViewMessage(amg="<hl>Boundary set from selection!</hl>", pos='midCenter', fade=True)
        except Exception as e:
            cmds.warning(f"Cannot get boundary: {e}")

    def get_surface_top_y(self, mesh, x, z):
        try:
            shape = cmds.listRelatives(mesh, shapes=True, fullPath=True)[0]
            cp_node = cmds.createNode('closestPointOnMesh')
            cmds.connectAttr(shape + ".outMesh", cp_node + ".inMesh", f=True)
            cmds.connectAttr(shape + ".worldMatrix[0]", cp_node + ".inputMatrix", f=True)
            cmds.setAttr(cp_node + ".inPositionX", x)
            cmds.setAttr(cp_node + ".inPositionY", 10000)
            cmds.setAttr(cp_node + ".inPositionZ", z)
            y = cmds.getAttr(cp_node + ".positionY")
            cmds.delete(cp_node)
            bbox = cmds.exactWorldBoundingBox(mesh)
            top_y = bbox[4]
            return max(y, top_y)
        except:
            return 0.0

    def place_object_on_surface(self,obj,mesh,x,z):
        y = self.get_surface_top_y(mesh,x,z)
        bbox = cmds.exactWorldBoundingBox(obj)
        obj_bottom = bbox[1]
        cmds.move(x, y - obj_bottom, z, obj, absolute=True)

    def generate_objects(self):
        try:
            obj_count = int(self.objCountEdit.text())
        except:
            cmds.warning("Enter valid object count"); return
        try:
            x_min = float(self.boundXMin.text()); x_max=float(self.boundXMax.text())
            z_min = float(self.boundZMin.text()); z_max=float(self.boundZMax.text())
        except:
            cmds.warning("Enter valid boundary"); return
        try: scale_min=float(self.scaleMin.text()); scale_max=float(self.scaleMax.text())
        except: scale_min=1.0; scale_max=1.0
        try: min_distance=float(self.minDistEdit.text())
        except: min_distance=0.0

        theme = self.selected_theme_combo.currentText()
        selected_types = [name for name,chk in self.checkboxes.items() if chk.isChecked()]
        if not selected_types: cmds.warning("Select at least one type"); return

        sel_meshes = cmds.ls(selection=True, dag=True, type='transform') if self.snapToSurfaceCheck.isChecked() else []

        cmds.undoInfo(openChunk=True)
        created_objs = []
        positions = []

        def place_on_grid(obj,x,z):
            bbox = cmds.exactWorldBoundingBox(obj)
            obj_bottom = bbox[1]
            cmds.move(x,-obj_bottom,z,obj,absolute=True)

        try:
            for obj_type in selected_types:
                for i in range(obj_count):
                    maya_file = os.path.join(MODEL_DIR,self.model_files[obj_type])
                    if not os.path.exists(maya_file): cmds.warning(f"Not found {maya_file}"); continue
                    imported = cmds.file(maya_file,i=True,ignoreVersion=True,ra=True,mergeNamespacesOnClash=False,options="v=0;",pr=True,returnNewNodes=True)
                    new_objs = cmds.ls(imported, transforms=True)
                    if not new_objs: continue
                    obj = new_objs[0]

                    for attempt in range(100):
                        pos_x = random.uniform(x_min,x_max)
                        pos_z = random.uniform(z_min,z_max)
                        too_close = any(((pos_x-px)**2+(pos_z-pz)**2)**0.5<min_distance for px,pz in positions)
                        if not too_close: break
                    else:
                        pos_x = random.uniform(x_min,x_max)
                        pos_z = random.uniform(z_min,z_max)
                    positions.append((pos_x,pos_z))
                    scale = random.uniform(scale_min,scale_max)
                    cmds.scale(scale,scale,scale,obj)

                    if sel_meshes:
                        self.place_object_on_surface(obj, sel_meshes[0], pos_x, pos_z)
                    else:
                        place_on_grid(obj,pos_x,pos_z)

                    created_objs.append(obj)
                    utils.apply_theme_colors_by_material(obj,obj_type,theme)
        finally:
            cmds.undoInfo(closeChunk=True)

        if created_objs:
            cmds.select(created_objs)
            cmds.inViewMessage(amg="<hl>Created objects!</hl>", pos='midCenter', fade=True)


def run():
    global ui
    try: ui.close()
    except: pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = NatureGeneratorToolDialog(parent=ptr)
    ui.show()
