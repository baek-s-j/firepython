from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QLabel, QPushButton, QVBoxLayout, QInputDialog, QDialog, \
    QLineEdit, QDialogButtonBox, QFormLayout

from mapviewer import MapViewer

#작성자: 백승진
#기능: 진입로 데이터 수정
# 좌측에 데이터 수정 뷰, 우측에 지도 뷰.
# 지도 뷰에서 좌표 데이터를 받아옴.


class ApproachEditor(QWidget):
    def __init__(self, approach):
        super().__init__()

        self.approach = approach

        self.list_widget = QListWidget(self)
        self.list_widget.setFixedWidth(300)
        self.map_viewer = MapViewer()
        self.map_viewer.setPhoto(QtGui.QPixmap('yukgeori_market_map.png'))
        self.map_viewer.photoClicked.connect(self.photoClicked)
        self.cur_x = 0.0
        self.cur_y = 0.0
        self.dialog = InputDialog()

        self.syncListWidget()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.list_widget)
        hbox1.addWidget(self.map_viewer)

        font = QFont()
        font.setPointSize(10)

        btn = QPushButton('현재 위치에 추가', self)
        btn.setFont(font)
        btn.setFixedSize(150, 45)
        btn.clicked.connect(lambda: self.addApproach(state='cur'))

        btn2 = QPushButton('끝에 추가', self)
        btn2.setFont(font)
        btn2.setFixedSize(150, 45)
        btn2.clicked.connect(lambda: self.addApproach(state='end'))

        btn_vbox = QVBoxLayout()
        btn_vbox.addWidget(btn)
        btn_vbox.addWidget(btn2)

        btn3 = QPushButton('현재 위치 삭제', self)
        btn3.setFont(font)
        btn3.setFixedSize(150, 100)
        btn3.clicked.connect(self.delete)

        label = QLabel('마우스 오른쪽 클릭: 드래그 모드/ 좌표 찍기 모드 변경\n'
                       '좌표 찍기 모드에서 마우스 왼쪽 클릭을 하면 해당 건물의 좌표값이 업데이트 되며 다음 건물로 자동으로 넘어감\n'
                       '드래그 모드에서 마우스 휠/ 드래그 사용 가능')
        label.setFont(font)

        self.cur_ratio = QLabel('현재 좌표\nx: ' + str(self.cur_x) + '\ny: ' + str(self.cur_y))

        hbox2 = QHBoxLayout()
        hbox2.stretch(1)
        hbox2.addLayout(btn_vbox)
        hbox2.stretch(1)
        hbox2.addWidget(btn3)
        hbox2.stretch(1)
        hbox2.addWidget(label)
        hbox2.stretch(1)
        hbox2.addWidget(self.cur_ratio)
        hbox2.stretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox1)

        self.setLayout(vbox)

    def photoClicked(self, x_ratio, y_ratio):
        if self.map_viewer.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            self.cur_x = x_ratio
            self.cur_y = y_ratio
            self.cur_ratio.setText('현재 좌표\nx: ' + str(self.cur_x) + '\ny: ' + str(self.cur_y))

    def addApproach(self, state):
        self.dialog.show()
        if self.dialog.exec():
            tmp = self.dialog.getInputs()
            tmp['x'] = self.cur_x
            tmp['y'] = self.cur_y
            if state == 'cur':
                self.approach.insert(self.list_widget.currentRow(), tmp)
            else:
                self.approach.append(tmp)
        self.syncListWidget()

    def syncListWidget(self):
        self.list_widget.clear()
        for i in range(len(self.approach)):
            self.list_widget.addItem('진입로' + chr(ord('A') + i) + ', 주소: ' + self.approach[i]['address'])
        self.list_widget.setCurrentItem(self.list_widget.item(0))

    def delete(self):
        del self.approach[self.list_widget.currentRow()]
        self.syncListWidget()


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name = QLineEdit(self)
        self.address = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("진입로 이름", self.name)
        layout.addRow("주소", self.address)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        approach = {'name': self.name.text(), 'address': self.address.text()}
        return approach
