# -*- coding: utf-8 -*-

from getuipy.igt_push import *
from getuipy.igetui.template import *
from getuipy.igetui.template.igt_base_template import *
from getuipy.igetui.template.igt_transmission_template import *
from getuipy.igetui.template.igt_link_template import *
from getuipy.igetui.template.igt_notification_template import *
from getuipy.igetui.template.igt_notypopload_template import *
from getuipy.igetui.template.igt_apn_template import *
from getuipy.igetui.igt_message import *
from getuipy.igetui.igt_target import *
from getuipy.igetui.template import *
import os

#toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'true'
APPKEY = "j4l9rfhgwT79B9EH1Wvai8"
APPID = "LLNstWgyGm8UM2SsherlU3"
MASTERSECRET = "ItQSEF1Hgw7V0q95csarI1"
CID = "a7f536a051965dec65ae7e1b59956f0d"
CID2 = "4bdb40e77cb0775051cc38bb613cc3af"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'
ALIAS = '中文123'
DEVICETOKEN = "0aaa60df893cf1c36122818a5b67301a26d1f442a4611db3daa3e2423e66e4cd"

def pushMessageToSingle():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    #消息模版：
    #1.TransmissionTemplate:透传功能模板
    #2.LinkTemplate:通知打开链接功能模板
    #3.NotificationTemplate：通知透传功能模板
    #4.NotyPopLoadTemplate：通知弹框下载功能模板

    template = NotificationTemplateDemo()
    #template = LinkTemplateDemo()
    # template = TransmissionTemplateDemo()
    #template = NotyPopLoadTemplateDemo()

    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    message.pushNetWorkType = 2    

    target = Target()
    target.appId = APPID
    target.alias = ALIAS

    ret = push.pushMessageToSingle(message, target)
    print (ret)


def pushMessageToList():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    #消息模版： 
    #1.TransmissionTemplate:透传功能模板  
    #2.LinkTemplate:通知打开链接功能模板  
    #3.NotificationTemplate：通知透传功能模板  
    #4.NotyPopLoadTemplate：通知弹框下载功能模板

    #template = NotificationTemplateDemo()
    template = LinkTemplateDemo()
    #template = TransmissionTemplateDemo()
    #template = NotyPopLoadTemplateDemo()

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.pushNetWorkType = 0

    target1 = Target()
    target1.appId = APPID
    target1.alias = (ALIAS)

    target2 = Target()
    target2.appId = APPID
    target2.alias= ('中文')

    targets = [target1]
    # targets.append(target2)
    contentId = push.getContentId(message,'ToList_任务别名_可为空')
    ret = push.pushMessageToList(contentId, targets)
    print (ret)

#通知透传模板动作内容
def NotificationTemplateDemo():
    template = NotificationTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1
    template.transmissionContent = u"请填入透传内容"
    template.title = u"请填入通知标题"
    template.text = u"请填入通知内容"
    template.logo = "icon.png"
    template.logoURL = ""
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    return template

#通知链接模板动作内容
def LinkTemplateDemo():
    template = LinkTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.title = u"请填入通知标题"
    template.text = u"请填入通知内容"
    template.logo = ""
    template.url = "http://www.baidu.com"
    template.transmissionType = 1
    template.transmissionContent = ''
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    #iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    #template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
    #template.setPushInfo("open",4,"message","test1.wav","","","","");
    return template

#透传模板动作内容
def TransmissionTemplateDemo():
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '请填入透传内容'
    #iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    #template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
    #template.setPushInfo("",2,"","","","","","");
    return template

#单个ClientID绑定别名功能
def bindAlias():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    ret = push.bindAlias(APPID, ALIAS, CID)
    print (ret)

def queryClientId():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    ret = push.queryClientId(APPID,ALIAS)
    print (ret)

def queryAlias():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    dictz = push.queryAlias(APPID, CID)
    for key in dictz:
        print (key+":"+dictz[key])

def aliasUnBind():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    ret = push.unBindAlias(APPID,ALIAS,CID)
    print (ret)

def bindAliasBatch():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    target = Target()
    target.clientId = CID
    target.alias = ALIAS

    target1 = Target()
    target1.clientId = CID2
    target1.alias = ALIAS
    
    targets=[target]
    targets.append(target1)

    ret = push.bindAliasBatch(APPID, targets)
    print (ret)

def unBindAliasAll():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    ret = push.unBindAliasAll(APPID,ALIAS)
    print (ret)

#单个ClientId绑定别名
# bindAlias()
#多个ClientIdn绑定一个别名
# bindAliasBatch()
#根据别名获取ClientId
# queryClientId()
#根据ClientID获取别名
# queryAlias()
#解除Clientid与别名的绑定关系
# aliasUnBind()

#取消别名下的所有ClientId绑定
# unBindAliasAll()

# pushMessageToSingle()
pushMessageToList()
