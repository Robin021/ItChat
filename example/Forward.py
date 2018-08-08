# coding:utf8

import itchat
from itchat.content import *

# 自动处理添加好友申请
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(u'你好哇', msg['RecommendInfo']['UserName'])


# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']

    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return

    if msg['Type'] == TEXT:
        content = msg['Content']
    elif msg['Type'] == SHARING:
        content = msg['Text']

    # 根据消息类型转发至其他需要同步消息的群聊或个人
    if msg['Type'] == TEXT:

        # 转个人
        if Flag_for_single_people:
            itchat.send_msg('[%s] [%s]中说: \n%s' % (
                username, chatroom_id,msg['Content']),
                            toUserName=itchat.search_friends(name=NickName_for_single_people)[0]['UserName'])

        #转发
        if single_chatrooms_flag:
            # 转指定群聊
                itchat.send('[%s]说: %s' % (username, msg['Content']), chatrooms['UserName'])
        else:
            # 转所有群聊
            for item in chatrooms:
                if not item['UserName'] == chatroom_id:
                    itchat.send('[%s]说: %s' % (username, msg['Content']), item['UserName'])

    elif msg['Type'] == SHARING:
        itchat.send_msg('%s\n%s' % (username, msg['Content']), toUserName=itchat.search_friends(name='晔枫')[0]['UserName'])
        # itchat.send_msg('%s\n%s' % (username, msg['Content']), toUserName=itchat.search_friends(name='westman')[0]['UserName'])


# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def group_reply_media(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']

    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return

    # 如果为gif图片则不转发
    if msg['FileName'][-4:] == '.gif':
        return

    # 下载图片等文件
    msg['Text'](msg['FileName'])
    # 转发至其他需要同步消息的个人或者群聊
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
        toUserName=itchat.search_friends(name='晔枫')[0]['UserName'])
    # itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
    #     toUserName=itchat.search_friends(name='westman')[0]['UserName'])

    #设置群聊名称
def set_single_groupname(group_name):
    chatroom = ichatroom = itchat.search_chatrooms(name=group_name)
    return chatrooms

# 扫二维码登录
itchat.auto_login(hotReload=True)

# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
chatroom_ids = [c['UserName'] for c in chatrooms]

#单独设置监听群聊名称
single_chatroom = set_single_groupname('老王家')
single_chatrooms_flag = False

#设置转发个人微信号
NickName_for_single_people = '宗鹏'
Flag_for_single_people = True

print(
'正在监测的群聊：', len(chatrooms), '个')
print(
' '.join([item['NickName'] for item in chatrooms]))
# 开始监测
itchat.run()
