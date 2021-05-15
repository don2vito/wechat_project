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
with Imbox('邮箱的 imap 网址','邮箱地址',pwd,ssl=True) as imbox:
    all_inbox_messages = imbox.messages()
    for uid, message in all_inbox_messages:
        print(message.subject)
        print(message.body['plain'])

'''
message.sent_from 发件人
message.sent_to 收件人
message.subject 主题
message.date 时间
message.body[‘plain’] 文本格式内容
message.body[‘html’] html格式内容
message.attchments 附件
'''

# 未读邮件：imbox.message(unread=True)
# 红旗邮件: imbox.messages(flagged=True)
# 某发件人的邮件: imbox.messages(sent_from='发件人邮箱')
# 某收件人的邮件: imbox.messages(sent_to='收件人邮箱')
# date__lt 某天前：imbox.messages(date__lt = datetime.date(年,月,日))
# date__gt 某天后：imbox.messages(date__gt = datetime.date(年,月,日))
# date__on 指定某一天：imbox.messages(date__on = datetime.date(年,月,日))
# 标记已读： imbox.mark_seen(uid)
# 删除邮件： imbox.delete(uid)
