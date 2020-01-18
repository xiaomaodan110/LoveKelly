import os
import poplib
from email.parser import Parser
from email.header import  decode_header
from email.utils import parseaddr
import chardet

def decode_bytes(x):
    charset = chardet.detect(x)["encoding"]
    if charset:
        if charset == 'GB2312' or charset == 'GBK':
            charset = 'GB18030'
        x = x.decode(charset,"ignore")
    else:
        charset = 'utf-8'
        x = x.decode(charset,"ignore")
    return x

def decode_str(s):
    value,charset = decode_header(s)[0]
    if charset:
        if charset == 'GB2312' or charset == 'GBK':
            charset = 'GB18030'
        value = value.decode(charset,"ignore")
    return value

def get_email_headers(msg):
    headers = {}
    for header in ['From','To','Cc','Subject','Date']:
        value = msg.get(header,'')
        if value:
            if header == 'From':
                hdr,addr = parseaddr(value)
                # name = decode_str(hdr)
                # from_addr = u'%s<%s>' % (name,addr)
                headers['From'] = addr
            if header == 'To':
                all_to = value.split(',')
                to = []
                for x in all_to:
                    hdr,addr = parseaddr(x)
                    name = decode_str(hdr)
                    to_addr = u'%s<%s>' % (name,addr)
                    to.append(to_addr)
                headers['To'] = ','.join(to)
            if header == 'Cc':
                all_cc = value.split(',')
                cc = []
                for x in all_cc:
                    hdr,addr = parseaddr(x)
                    name = decode_str(hdr)
                    cc_addr = u'%s<%s>' % (name,addr)
                    to.append(cc_addr)
                headers['Cc'] = ','.join(cc)
            if header == 'Subject':
                subject = decode_str(value)
                headers['Subject'] = subject
            if header == 'Date':
                headers['Date'] = value
    return headers


def get_email_content(msg,savepath):
    # Message里可能包含多个MIMEBase，也就是多个part，每个part里都可能有一个附件，message.walk()遍历这些part，依次解析。
    # 该函数把附件都保存到了savepath路径下了，不考虑附件重名的情况了。
    attahments = []
    for part in msg.walk():
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            attahments.append(filename)
            data = part.get_payload(decode=True)
            abs_filename = os.path.join(savepath,filename)
            if not os.path.exists(savepath):
                os.mkdir(savepath)
            attach = open(abs_filename,'wb')
            attach.write(data)
            attach.close()

    return attahments

if __name__ == '__main__':
    user_path = 'D:\\account.txt'
    # 邮箱账号密码
    # account = 'yizhao.liu@hand-china.com'
    # passwd = 'Hswzwzjzd1002'
    # 邮箱服务器
    with open(user_path, "rb") as f:
        userinfo = f.read()
    account = userinfo.decode('utf-8').split('\r\n')[0]
    passwd = userinfo.decode('utf-8').split('\r\n')[1]
    pop3_server = 'pop.hand-china.com'
    server = poplib.POP3(pop3_server)
    server.set_debuglevel(0)
    print(server.getwelcome())
    server.user(account)
    server.pass_(passwd)
    msg_count, msg_size = server.stat()
    print('message count:',msg_count)
    print('message size:',msg_size,'bytes')
    # resp,mails,octets = server.list()
    for i in range(1, msg_count):
        resp, byte_lines, octets = server.retr(i)
        str_lines = []
        for x in byte_lines:
            str_lines.append(decode_bytes(x))
        msg_content = '\n'.join(str_lines)
        msg = Parser().parsestr(msg_content)
        headers = get_email_headers(msg)
        attahments = get_email_content(msg,r'D:\email-attach')
        print('subject:',headers['Subject'])
        print('from:',headers['From'])
        print('to:',headers['To'])
        if 'cc' in headers:
            print('cc:',headers['Cc'])
        print('date:',headers['Date'])
        print('attachments: ',attahments)
        print('-'*20)

    server.quit()

