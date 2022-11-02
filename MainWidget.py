from PyQt5.Qt import *
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, \
    QComboBox, QLabel, QSpinBox, QFileDialog
from PaintBoard import PaintBoard

from recognize import recognize

class MainWidget(QWidget):

    def __init__(self, Parent=None):

        super().__init__(Parent)

        self.__InitData()  # 先初始化数据，再初始化界面
        self.__InitView()

    def __InitData(self):
        '''
                  初始化成员变量
        '''
        self.__paintBoard = PaintBoard(self)
        # 获取颜色列表(字符串类型)
        self.__colorList = QColor.colorNames()

    def __InitView(self):
        '''
                  初始化界面
        '''
        self.setFixedSize(640, 480)
        self.setWindowTitle("Digit Recognizer")

        # 新建一个水平布局作为本窗体的主布局
        main_layout = QHBoxLayout(self)
        # 设置主布局内边距以及控件间距为10px
        main_layout.setSpacing(10)

        # 在主界面左侧放置画板
        main_layout.addWidget(self.__paintBoard)

        # 新建垂直子布局用于放置按键
        sub_layout = QVBoxLayout()

        # 设置此子布局和内部控件的间距为10px
        sub_layout.setContentsMargins(10, 10, 10, 10)

        self.__label_School = QLabel(self)
        self.__label_School.setText("😘😝")
        self.__label_School.setAlignment(Qt.AlignCenter)
        self.__label_School.setFont(QFont("楷体", 12, QFont.Bold))
        sub_layout.addWidget(self.__label_School)

        self.__label_faculty = QLabel(self)
        self.__label_faculty.setText("張継")
        self.__label_faculty.setAlignment(Qt.AlignCenter)
        self.__label_faculty.setFont(QFont("楷体", 12, QFont.Bold))
        sub_layout.addWidget(self.__label_faculty)

        self.__label_Name = QLabel(self)
        self.__label_Name.setText("(〃'▽'〃)")
        self.__label_Name.setAlignment(Qt.AlignCenter)
        self.__label_Name.setFont(QFont("楷体", 12, QFont.Bold))
        sub_layout.addWidget(self.__label_Name)

        splitter = QSplitter(self)  # 占位符
        sub_layout.addWidget(splitter)

        self.__btn_Clear = QPushButton("清空画板")
        self.__btn_Clear.setParent(self)  # 设置父对象为本界面

        # 将按键按下信号与画板清空函数相关联
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)

        self.__btn_Quit = QPushButton("退出")
        self.__btn_Quit.setParent(self)  # 设置父对象为本界面
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout.addWidget(self.__btn_Quit)

        self.__btn_Save = QPushButton("保存作品")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        sub_layout.addWidget(self.__btn_Save)

        self.__cbtn_Eraser = QCheckBox("  使用橡皮擦")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)

        self.__btn_Recognize = QPushButton("识别")
        self.__btn_Recognize.setParent(self)  # 设置父对象为本界面
        self.__btn_Recognize.clicked.connect(self.on_recognize_clicked)
        sub_layout.addWidget(self.__btn_Recognize)

        self.__label_result = QLabel(self)
        self.__label_result.setText("识别结果：")
        # self.__label_result.setFixedHeight(20)
        sub_layout.addWidget(self.__label_result)

        self.__label_rec_result = QLabel('',self)
        # self.__label_rec_result.setFixedHeight(20)
        self.__label_rec_result.setAlignment(Qt.AlignCenter)
        self.__label_rec_result.setFont(QFont("Roman times", 18, QFont.Bold))
        self.__label_rec_result.setStyleSheet("color:red")
        sub_layout.addWidget(self.__label_rec_result)

        splitter = QSplitter(self)  # 占位符
        sub_layout.addWidget(splitter)

        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("画笔粗细")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)

        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(20)
        self.__spinBox_penThickness.setMinimum(2)
        self.__spinBox_penThickness.setValue(10)  # 默认粗细为10
        self.__spinBox_penThickness.setSingleStep(2)  # 最小变化值为2
        self.__spinBox_penThickness.valueChanged.connect(
            self.on_PenThicknessChange)  # 关联spinBox值变化信号和函数on_PenThicknessChange
        sub_layout.addWidget(self.__spinBox_penThickness)

        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("画笔颜色")
        self.__label_penColor.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penColor)

        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor)  # 用各种颜色填充下拉列表
        self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange)  # 关联下拉列表的当前索引变更信号与函数on_PenColorChange
        sub_layout.addWidget(self.__comboBox_penColor)

        main_layout.addLayout(sub_layout)  # 将子布局加入主布局


    def __fillColorList(self, comboBox):
        index_black = 0
        index = 0
        for color in self.__colorList:
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70, 20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix), None)
            comboBox.setIconSize(QSize(70, 20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)


    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)


    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)


    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])


    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True  # 进入橡皮擦模式
        else:
            self.__paintBoard.EraserMode = False  # 退出橡皮擦模式

    def on_recognize_clicked(self):
        savePath = './tmp/image.png'
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath)
        print(savePath)

        predict = recognize(savePath)
        print(predict)
        self.__label_rec_result.setText(predict)

    def Quit(self):
        self.close()
