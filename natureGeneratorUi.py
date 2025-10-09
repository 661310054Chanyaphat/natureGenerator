try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


IMAGE_DIR = 'C:/Users/user/Documents/maya/2024/scripts/natureGenerator/icons'


class NatureGeneratorToolDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		# 🌱 ตั้งค่าหน้าต่าง
		self.setWindowTitle('Nature Generator Tool')
		self.resize(400, 480)

		# 🧱 Layout หลัก
		self.mainLayout = QtWidgets.QVBoxLayout(self)
		self.setLayout(self.mainLayout)

		
		self.setStyleSheet('''
			QDialog {
				background-color: #93C9C8;
				border-radius: 10px;
			}
			QLabel {
				font-family: Arial;
				color: #1B3B47;
			}
			QLineEdit {
				background-color: #55A1A0;
				border: 1.5px solid #2E6670;
				border-radius: 6px;
				padding: 3px 6px;
			}
			QPushButton {
				background-color: #2E6670;
				color: white;
				font-weight: bold;
				border-radius: 10px;
				padding: 8px;
			}
			QPushButton:hover {
				background-color: #66BB6A;
			}
			QPushButton:pressed {
				background-color: #388E3C;
			}
		''')

		
		titleLabel = QtWidgets.QLabel("Nature Generator Tool")
		titleLabel.setAlignment(QtCore.Qt.AlignCenter)
		titleLabel.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
		self.mainLayout.addWidget(titleLabel)

		
		imageLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(imageLayout)

		# รูปไอคอน
		icons = [
			("Tree", "tree.png"),
			("Flower", "flower.png"),
			("Grass", "grass.png"),
			("Rock", "rock.png")
		]

		for name, img in icons:
			vbox = QtWidgets.QVBoxLayout()
			label_img = QtWidgets.QLabel()
			pixmap = QtGui.QPixmap(f"{IMAGE_DIR}/{img}")
			if not pixmap.isNull():
				pixmap = pixmap.scaled(90, 90, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
				label_img.setPixmap(pixmap)
			label_img.setAlignment(QtCore.Qt.AlignCenter)

			text_label = QtWidgets.QLabel(name)
			text_label.setAlignment(QtCore.Qt.AlignCenter)
			text_label.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))

			vbox.addWidget(label_img)
			vbox.addWidget(text_label)
			imageLayout.addLayout(vbox)

		
		gridLayout = QtWidgets.QGridLayout()
		self.mainLayout.addLayout(gridLayout)

		def make_row(label_text, row, has_range=False):
			label = QtWidgets.QLabel(label_text)
			gridLayout.addWidget(label, row, 0)
			if has_range:
				minEdit = QtWidgets.QLineEdit()
				maxEdit = QtWidgets.QLineEdit()
				toLabel = QtWidgets.QLabel("to")
				toLabel.setAlignment(QtCore.Qt.AlignCenter)
				gridLayout.addWidget(minEdit, row, 1)
				gridLayout.addWidget(toLabel, row, 2)
				gridLayout.addWidget(maxEdit, row, 3)
				return minEdit, maxEdit
			else:
				edit = QtWidgets.QLineEdit()
				gridLayout.addWidget(edit, row, 1, 1, 3)
				return edit

		
		self.objCountEdit = make_row("Object Count:", 0)
		self.boundXMin, self.boundXMax = make_row("Boundary X:", 1, True)
		self.boundZMin, self.boundZMax = make_row("Boundary Z:", 2, True)
		self.minDistEdit = make_row("Minimum Distance Between Objects:", 3)
		self.scaleMin, self.scaleMax = make_row("Scale Min and Max:", 4, True)

		def make_row(label_text, row, has_range=False):
			label = QtWidgets.QLabel(label_text)
			label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
			label.setStyleSheet("color: #1B5E20;")
			gridLayout.addWidget(label, row, 0)
	


		
		self.generateBtn = QtWidgets.QPushButton("Generate Object")
		self.mainLayout.addWidget(self.generateBtn)
		self.mainLayout.addStretch()


def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = NatureGeneratorToolDialog(parent=ptr)
	ui.show()
