# import keyring
# keyring.set_password('yagmail','邮箱地址','SMTP码')

'''
发送邮件
'''

import yagmail

with yagmail.SMTP(user='发件人邮箱地址',host='邮箱的 smtp 网址') as yag:
    body = '正文内容'
    img = '图片文件路径'
    yag.send(to=['收件人邮箱地址'],cc=['抄送人邮箱地址'],bcc=['密送人邮箱地址']subject='主题',contents=[body,img,yagmail.inline('邮件内容中内嵌图片文件路径')],attachments=['附件文件路径'])
    print('发送成功！！')


'''
接收邮箱所有附件
'''

from imbox import Imbox

pwd = keyring.get_password('yagmail','邮箱地址')
with Imbox('邮箱的 imap 网址','邮箱地址',pwd) as imbox:
    pass