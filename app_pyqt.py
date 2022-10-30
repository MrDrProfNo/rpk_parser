import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import traceback


GRID_LINE_LENGTH = 32


class AppWindow(QWidget):

	GRID_BUTTON_HOVER_STYLESHEET = ""

	def __init__(self, parent=None):
		super(AppWindow, self).__init__(parent)

		self.__create_filepath_loader()
		self.__create_selected_value_tracker()


		self.scrollArea = QScrollArea(self)
		self.scrollArea.setGeometry(QRect(40, 110, 761, 521))
		self.scrollArea.setWidgetResizable(True)

		# self.scrollAreaWidget = QWidget(self.scrollArea)
		# self.scrollAreaWidget.setGeometry(QRect(40, 110, 761, 521))
		# self.scrollAreaWidget.setObjectName("scrollAreaWidgetContents")

		self.gridLayoutWidget = QWidget()
		self.gridLayoutWidget.setGeometry(QRect(40, 110, 900, 521))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayoutWidget.setStyleSheet("QPushButton { border: 0px}")

		self.grid = QGridLayout()
		self.grid.setContentsMargins(0, 0, 0, 0)
		self.grid.setSpacing(0)

		self.gridLayoutWidget.setLayout(self.grid)

		self.scrollArea.setWidget(self.gridLayoutWidget)

		self.setGeometry(QRect(40, 110, 761, 521))
		self.setWindowTitle("PyQt")

	def __create_filepath_loader(self):
		self.filepath_entry = QLineEdit(self)
		self.filepath_entry.setGeometry(0, 0, 800, 20)
		self.filepath_entry.setPlaceholderText("Enter a filepath...")
		self.filepath_entry.setText(r"C:\Users\aheil\Documents\My Stuff\Personal\Programming\Planetfall\rpks\test_rpk.rpk")

		self.filepath_entry_button = QPushButton(self)
		self.filepath_entry_button.setGeometry(0, 20, 80, 20)
		self.filepath_entry_button.setText("Load RPK")
		self.filepath_entry_button.clicked.connect(self.__filepath_button_clicked)

		self.filepath_error_text = QLabel(self)
		self.filepath_error_text.setGeometry(100, 20, 500, 20)
		self.filepath_error_text.setText("Error goes here//////////////////////////////////////////////////////////")

	def __create_selected_value_tracker(self):
		self.selected_value = QLabel(self)
		self.selected_value.setGeometry(0, 40, 200, 20)
		self.selected_value.setText("Click a grid button to select a value")
		self.selected_value.hide()

	def __filepath_button_clicked(self):
		try:
			contents = AppWindow.__load_from_filepath(self.filepath_entry.text())
			self.filepath_error_text.hide()
			self.__display_grid_contents(contents)
			self.selected_value.show()
		except FileNotFoundError as e:
			self.filepath_error_text.setText(f"File could not be found")
		except PermissionError as e:
			self.filepath_error_text.setText(f"Permission to open file denied. You may have supplied a directory")
		except Exception as e:
			traceback.print_exc()

	@staticmethod
	def __load_from_filepath(filepath):
		with open(filepath, "rb") as file:
			contents = file.read()
			return contents

	def __display_grid_contents(self, contents):

		contents_idx = 0

		while contents_idx < len(contents):
			row_idx = contents_idx // GRID_LINE_LENGTH
			for col_idx in range(min(GRID_LINE_LENGTH, len(contents) - contents_idx)):
				button = self.__create_grid_button(contents[contents_idx + col_idx])
				self.grid.addWidget(button, row_idx, col_idx)

			contents_idx += GRID_LINE_LENGTH

	def __create_grid_button(self, value: int):
		button = QPushButton(self.gridLayoutWidget)
		button.setText(f"{value:02x}")
		# button.setFixedWidth(20)
		# button.setFixedHeight(20)
		button.setContentsMargins(0, 0, 0, 0)

		def __on_click():
			self.selected_value.setText(button.text())

		def __on_hover():
			button.setStyle()

		button.clicked.connect(__on_click)

		return button


def main():
	# app = QApplication(sys.argv)
	# ex = window()
	# # ex = test.Ui_Form()
	# ex.show()
	# sys.exit(app.exec_())

	app = QApplication(sys.argv)
	win = AppWindow()

	win.show()

	# win2 = AppWindow()
	# win2.setGeometry(QRect(801, 110, 761, 521))
	# win2.show()

	# draw_ui()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
