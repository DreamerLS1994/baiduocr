# coding:utf-8
from PyQt5 import QtWidgets,QtGui
import sys
import requests
import base64
import pyperclip
from ocrui import Ui_MainWindow  
from api_ocr import api as API
from threading import Thread
from PIL import ImageGrab, Image
from webbrowser import open as WebOpen

token = None
AppKey = 'HGXnQTTvk3mTeP1Fk3mOgdbI'
SecretKey = '4e7U2tOmEAhKfqirIKMgEzbOy1ChlOsK'
TIMEOUT_SECOND = 2


class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):
    img64 = ''
    filename = ''

    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

    def get_token(self):
        self.statusbar.showMessage('初始化中...')
        token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + AppKey+ '&client_secret=' + SecretKey
        try:
            token_res = requests.get(token_url, timeout=TIMEOUT_SECOND)
        except:
            return None
        else:
            try:
                res = token_res.json()["access_token"]
            except:
                self.statusbar.showMessage('初始化失败！请检查网络并设置正确的Key！')
            else:
                global token
                token = res
                self.statusbar.showMessage('初始化完成！欢迎使用！')
                self.btn_ocr_start.setEnabled(True)

    def get_pic64(self, file):
        try:
            with open (file,'rb') as pic:
                img64_x = base64.b64encode(pic.read())
        except:
            return None
        else:
            return img64_x

    def get_type(self):
        pic_type = self.comboBox.currentText()

        if self.radioButton.isChecked():
            pic_side = 'front'
        elif self.radioButton_2.isChecked():
            pic_side = 'back'

        return pic_type, pic_side

    def set_key(self):
        value1, ok = QtWidgets.QInputDialog.getText(self,
                                                    "设置", "请输入正确的AppKey:\n",
                                                    QtWidgets.QLineEdit.Normal, "HGXnQTTvk3mTeP1Fk3mOgdbI")
        if ok:
            value2, ok = QtWidgets.QInputDialog.getText(self,
                                                        "设置", "请输入正确的SecretKey:\n",
                                                        QtWidgets.QLineEdit.Normal, "4e7U2tOmEAhKfqirIKMgEzbOy1ChlOsK")
            global AppKey, SecretKey
            AppKey = value1
            SecretKey = value2
            self.btn_ocr_start.setEnabled(False)
            t = Thread(target=window.get_token, args=())
            t.start()

    def help(self):
        url='https://www.jerrycoding.com/tool/ocr-ui'
        WebOpen(url, new=0, autoraise=True)

    #定义槽函数
    def upload(self):
        filename_x, filetype = QtWidgets.QFileDialog.getOpenFileName(self, '选择图片', './', 'jpg (*.jpg;*jpeg;*jpe);;png(*.png);;bmp(*.bmp)')

        self.filename = filename_x
        pix = QtGui.QPixmap(self.filename)
        self.label.setPixmap(pix)
        self.label.setScaledContents(True)

    def paste(self):
        self.filename = './截图.png'
        if isinstance(ImageGrab.grabclipboard(), Image.Image):
            ImageGrab.grabclipboard().save(self.filename)
            pix = QtGui.QPixmap(self.filename)
            self.label.setPixmap(pix)
            self.label.setScaledContents(True)


    def ocr(self):
        if self.filename == '':
            QtWidgets.QMessageBox.information(self, "提示", "请先选择图片！")
            return
        self.statusbar.showMessage('正在识别....')
        self.img64 = self.get_pic64(self.filename)

        pic_type, pic_side = self.get_type()
        t_ocr = None

        if pic_type == '通用文字识别':
            t_ocr = Thread(target=API.get_ocr_common, args=(self, token, self.img64, 1))
        elif pic_type == '通用文字高精度识别':
            t_ocr = Thread(target=API.get_ocr_common, args=(self, token, self.img64, 2))
        elif pic_type == '手写文字识别':
            t_ocr = Thread(target=API.get_ocr_handwritng, args=(self, token, self.img64))
        elif pic_type == '身份证识别':
            t_ocr = Thread(target=API.get_ocr_idcard, args=(self, token, self.img64, pic_side))
        elif pic_type == '银行卡识别':
            t_ocr = Thread(target=API.get_ocr_bankcard, args=(self, token, self.img64))
        elif pic_type == '护照识别':
            t_ocr = Thread(target=API.get_ocr_passport, args=(self, token, self.img64))
        elif pic_type == '营业执照识别':
            t_ocr = Thread(target=API.get_ocr_business_license, args=(self, token, self.img64))
        elif pic_type == '车牌识别':
            t_ocr = Thread(target=API.get_ocr_license_plate, args=(self, token, self.img64,False))
        else:
            return
        if t_ocr:
            t_ocr.start()
            t_ocr.join()
            self.statusbar.showMessage('识别完成！')

        self.result_text.setPlainText("")
        self.result_text.setPlainText(API.get_text(self))

    def copy(self):
        out = self.result_text.toPlainText()
        pyperclip.copy(out)
        QtWidgets.QMessageBox.information(self, "提示", "已拷贝到剪切板！")

    def export(self):
        file_name, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", '/',  "Text 文本 (*.txt)")
        if file_name == "":
            return

        text = self.result_text.toPlainText()
        try:
            with open(file_name, 'w+') as f:
                f.write(text)
        except:
            QtWidgets.QMessageBox.information(self, "提示", "导出文件失败！")
        else:
            QtWidgets.QMessageBox.information(self, "提示", "导出文件成功！")


app = QtWidgets.QApplication(sys.argv)
#MainWindow = QMainWindow()
window = mywindow()
window.show()
window.help()
window.btn_ocr_start.setEnabled(False)
t = Thread(target=window.get_token, args=())
t.start()


sys.exit(app.exec_())
