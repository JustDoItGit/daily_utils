import os
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import fitz
import re

"""

# 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
"""

class PDF2Word():
    def __init__(self, pdfpapth):
        self.pdfpath = pdfpapth

    def get_content_from_pdf(self):  # 解析pdf文件函数
        with open(self.pdfpath,'rb') as f:
            parser = PDFParser(f)  # 创建一个pdf文档分析器
        pdf = PDFDocument()         # 创建一个PDF文档

        parser.set_document(pdf)  # 将分析器和文档进行绑定
        pdf.set_parser(parser)
        pdf.initialize()  # 对文档进行初始化，提供初始化密码

        if not pdf.is_extractable:  # 判断pdf文档是否能被转换，不能就结束程序
            raise PDFTextExtractionNotAllowed
        else:
            return list(pdf.get_pages())  # 返回pdf文档中的页面内容信息

    def save_content(self,page_index=None, save_path=None):
        pages = self.get_content_from_pdf()
        num_page = 0
        pdfresourcemanager = PDFResourceManager()  # 创建资源管理器来共享资源
        laparams = LAParams()
        pdfpageAggregator = PDFPageAggregator(pdfresourcemanager, laparams=laparams) # 创建一个PDF设备对象

        interpreter = PDFPageInterpreter(pdfresourcemanager, pdfpageAggregator)# 创建一个PDF解释器对象
        if page_index:  # 如果想提取某些页，就把具体页数指明出来
            pages = list(pages[i-1] for i in page_index)
        save_path = save_path if save_path else self.pdfpath.replace('pdf', 'doc')
        with open(save_path, 'w', encoding='utf-8') as f:  # 生成doc文件的文件名及路径
            for page in pages:  # doc.get_pages() 获取page列表
                num_page += 1  # 页面增一
                interpreter.process_page(page)
                layout = pdfpageAggregator.get_result()  # 提取页面的信息
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容,这里获取的是一行
                        # 保存文本内容
                        print("232")
                        results = x.get_text()
                        f.write(results)
                        f.write('\n')

    def save_pics(self,save_path):
        checkIM = r"/Subtype(?= */Image)"   # 使用正则表达式来匹配图片
        pdf = fitz.open(self.pdfpath)
        count = 0
        lenXREF = pdf._getXrefLength()  # 提取pdf内的对象
        for i in range(1, lenXREF):
            text = pdf._getXrefString(i)  # 定义字符串对象

            isImage = re.search(checkIM, text)  # 查看是否是图片对象
            if not isImage:  # 如果提取的不是图片，就跳过
                continue
            count += 1
            pixes = fitz.Pixmap(pdf, i)
            new_name = "{}.png".format(count)  # 设置保存图片的路径

            if pixes.n < 5:  # 如果pix.n<5,可以直接存为PNG
                pixes.writePNG(os.path.join(save_path, new_name))
            else:  # 否则就需要先转换为CMYK彩色模式,然后在进行保存
                pixes = fitz.Pixmap(fitz.csRGB, pixes)
                pixes.writePNG(os.path.join(save_path, new_name))


if __name__ == '__main__':
    pdf2word = PDF2Word(r"demo.pdf")
    pdf2word.save_pics(r"c:\")