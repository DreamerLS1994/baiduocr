# coding:utf-8
import requests
from enum import IntEnum


class OCR_TYPE(IntEnum):
    general_basic      =1,       #通用文字识别
    accurate_basic     =2,       #通用文字识别（高精度版）
    general_enhanced   =3,       #通用文字识别（含生僻字版）
    handwriting        =4,       #手写文字识别
    idcard             =5,       #身份证识别
    bankcard           =6,       #银行卡识别
    business_license   =7,       #营业执照识别
    passport           =8,       #护照识别
    business_card      =9,       #名片识别
    household_register =10,      #户口本识别
    birth_certificate  =11,      #出生医学证明识别
    HK_Macau_exitentrypermit=12, #港澳通行证识别
    taiwan_exitentrypermit =13,  #台湾通行证识别
    receipt           =14,       #通用票据识别
    vat_invoice       =15,       #增值税发票识别
    train_ticket      =16,       #火车票识别
    taxi_receipt      =17,       #出租车票识别
    quota_invoice     =18,       #定额发票识别
    driving_license   =19,       #驾驶证识别
    vehicle_license   =20,       #行驶证识别
    license_plate     =21,       #车牌识别
    qrcode            =22,       #二维码识别
    webimage          =23,       #网络图片文字识别
    lottery           =24,       #彩票识别
    insurance_documents =25,     #保单识别



HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

class api():
    output_text = ''

    def get_text(self):
        return self.output_text

    '''
    type=1:通用识别
    type=2:高精度识别
    '''
    def get_ocr_common(self, token, img64, type):
        self.output_text = ''
        params = {"image": img64, "detect_direction": "true"}
        if (type == OCR_TYPE['general_basic'].value):
            url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + token
        elif (type == OCR_TYPE['accurate_basic'].value):
            url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + token
        else:
            self.output_text = '由于某种原因识别失败！请重试~！'
            
        res = requests.post(url, data=params, headers=HEADERS)
        try:
            text = ''
            text_1 = res.json()["words_result"]
            for each in text_1:
                for key, value in each.items():
                    text += value + '\n'
        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            self.output_text = text

    '''
    手写字识别
    '''
    def get_ocr_handwritng(self, token, img64):
        self.output_text = ''
        params = {"image": img64}
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token=' + token

        res = requests.post(url, data=params, headers=HEADERS)
        try:
            text = ''
            text_1 = res.json()["words_result"]
            print(text_1)
            for i in text_1:
                text += i["words"] + '\n'

        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            self.output_text = text

    '''
    身份证识别
    '''
    def get_ocr_idcard(self, token, img64, side):
        self.output_text = ''
        params = {"image": img64, "id_card_side": side, "detect_direction": "true"}
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/idcard?access_token=' + token

        res = requests.post(url, data=params, headers=HEADERS)
        try:
            text = res.json()["words_result"]
        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            s = ""
            for key, value in text.items():
                s += key + ": " + value['words'] + "\n"
            self.output_text = s
    '''
    +bank_card_number	string	是	银行卡卡号
    +bank_name	string	是	银行名，不能识别时为空
    +bank_card_type	uint32	是	银行卡类型，0:不能识别; 1: 借记卡; 2: 信用卡
    银行卡识别
    '''
    def get_ocr_bankcard(self, token, img64):
        self.output_text = ''
        params = {"image": img64}
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard?access_token=' + token

        res = requests.post(url, data=params, headers=HEADERS, timeout=2)
        text = ''
        try:
            text = res.json()["result"]
        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            if (text['bank_card_type'] == 2):
                type = '信用卡'
            elif (text['bank_card_type'] == 1):
                type = '借记卡'
            else:
                type = '无法识别'
            self.output_text += '银行卡号: ' + text['bank_card_number'] + '\n'
            self.output_text += '有效期: ' + text['valid_date'] + '\n'
            self.output_text += '卡类型: ' + type + '\n'
            self.output_text += '银行名称: ' + text['bank_name'] + '\n'

    '''
    护照识别
    '''
    def get_ocr_passport(self, token, img64):
        self.output_text = ''
        params = {"image": img64}
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/passport?access_token=' + token

        res = requests.post(url, data=params, headers=HEADERS)
        out = ''
        try:
            text = res.json()["words_result"]
            for key, value in text.items():
                out += key + ": " + value['words'] + '\n'
        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            self.output_text = out

    '''
    营业执照识别
    '''
    def get_ocr_business_license(self, token, img64):
        self.output_text = ''
        params = {"image": img64, "detect_direction": "true"}
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/business_license?access_token=' + token

        res = requests.post(url, data=params, headers=HEADERS)
        out = ''
        try:
            text = res.json()["words_result"]
            for key, value in text.items():
                out += key + ": " + value['words'] + '\n'
        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            self.output_text = out

    '''
    车牌识别
    multi_detect 是否检测多张车牌，默认为false
    '''
    def get_ocr_license_plate(self, token, img64, multi_detect):
        self.output_text = ''
        params = {"image": img64, "multi_detect": multi_detect}
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate?access_token=' + token

        res = requests.post(url, data=params, headers=HEADERS)
        try:
            print(res.text)
            text = res.json()["words_result"]

        except:
            self.output_text = '由于某种原因识别失败！请重试~！'
        else:
            self.output_text += '颜色: ' + text['color'] + '\n'
            self.output_text += '号码: ' + text['number'] + '\n'
