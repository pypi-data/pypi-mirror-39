# -*- coding: utf-8 -*-
from array import array

from getuipy import RequestException
from getuipy.igetui.template.igt_startactivity_template import StartActivityTemplate
from getuipy.igetui.template.notify.igt_notify import Notify
from getuipy.protobuf.gt_req_pb2 import NotifyInfo
from getuipy.payload.VoIPPayload import *
from getuipy.igetui.template.style.Style1 import *
from getuipy.igetui.template.style.Style4 import *
from getuipy.igetui.template.style.Style6 import *


__author__ = 'wei'

from getuipy.igt_push import *
from getuipy.igetui.template.igt_transmission_template import *
from getuipy.igetui.template.igt_link_template import *
from getuipy.igetui.template.igt_notification_template import *
from getuipy.igetui.template.igt_notypopload_template import *
from getuipy.igetui.template.igt_apn_template import *
from getuipy.igetui.igt_message import *
from getuipy.igetui.igt_target import *
from getuipy.igetui.template import *
from getuipy.GtConfig import GtConfig
from getuipy.BatchImpl import *
from getuipy.payload.APNPayload import *
from getuipy.igetui.utils.AppConditions import *
from getuipy.igetui.template.notify.igt_smsmessage import SmsMessage
from getuipy.igetui.template.style.Style0 import *
# from igetui.template.style.Style1 import *
# from igetui.template.style.Style4 import *
# from igetui.template.style.Style6 import *

# toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'true'
# os.environ['gexin_pushSingleBatch_needAsync'] = 'False'
APPKEY = ""
APPID = ""
MASTERSECRET = ""
CID = ""

HOST = 'http://sdk.open.api.igexin.com/apiex.htm'
Alias = 'Alias'
Badge = '+1'
TASKID = ''
PN = ''
DEVICETOKEN = ""
GroupName = 'GroupName'

def pushMessageToSingle():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    template = NotificationTemplateDemo()
    # template = LinkTemplateDemo()
    # template = TransmissionTemplateDemo()
    # template = StartActivityTemplateDemo()
    message = IGtSingleMessage()
    # 是否离线推送
    message.isOffline = True
    # 离线有效时间
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    # 推送的网络类型：(0:不限;1:wifi;2:4G/3G/2G)
    # message.pushNetWorkType = 2

    target = Target()
    target.appId = APPID
    target.clientId = CID

    try:
        ret = push.pushMessageToSingle(message, target)
        time.sleep(1)
        print (ret)
    except RequestException as e:
        requstId = e.getRequestId()
        ret = push.pushMessageToSingle(message, target, requstId)
        print (ret)



def pushMessageToSingleBatch():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    batch = BatchImpl(APPKEY, push)

    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

    templateNoti = NotificationTemplateDemo()
    templateLink = LinkTemplateDemo()
    # template = TransmissionTemplateDemo()

    messageNoti = IGtSingleMessage()
    messageNoti.isOffline = True
    messageNoti.offlineExpireTime = 1000 * 3600 * 12
    messageNoti.data = templateNoti
    #     message.pushNetWorkType = 1

    targetNoti = Target()
    targetNoti.appId = APPID
    targetNoti.clientId = CID
    batch.add(messageNoti, targetNoti)

    messageLink = IGtSingleMessage()
    messageLink.isOffline = True
    messageLink.offlineExpireTime = 1000 * 3600 * 12
    messageLink.data = templateLink
    #     message.pushNetWorkType = 1

    targetLink = Target()
    targetLink.appId = APPID
    targetLink.clientId = "532434e53324be9c2a68c4f5923f07a9"
    batch.add(messageLink, targetLink)
    try:
        ret = batch.submit()
        print (ret)
    except Exception as e:
        ret = batch.retry()
        print (ret)


def pushMessageToList():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

    # template = NotificationTemplateDemo()
    template = LinkTemplateDemo()
    # template = TransmissionTemplateDemo()
    # template = NotyPopLoadTemplateDemo()

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.pushNetWorkType = 0

    target1 = Target()
    target1.appId = APPID
    target1.clientId = CID
    # target1.alias = "123"
    target2 = Target()
    target2.appId = APPID
    # target2.clientId = "a99f38fb45c8c6c822664b5de316af88"
    target2.alias = "456"
    arr = []

    arr.append(target1)
    arr.append(target2)
    contentId = push.getContentId(message, 'ToList_任务别名_可为空')
    ret = push.pushMessageToList(contentId, arr)
    print (ret)

def getContentIdDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    contentId = "OSS-1030_3d86cfa3efcff1a5453325adfebf0d06"
    res = push.cancelContentId(contentId)
    print(res)

def cancelContentIdDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    message = IGtListMessage()
    template = NotificationTemplateDemo()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.pushNetWorkType = 0
    contentId = push.cancelContentId(message, 'ToList_任务别名_可为空')
    print(contentId)

def pushMessageToApp():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

    template = NotificationTemplateDemo()
    # template = LinkTemplateDemo()
    # template = TransmissionTemplateDemo()
    # template = NotyPopLoadTemplateDemo()

    message = IGtAppMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.appIdList.extend([APPID])
    # 定时任务
    # message.pushTime = "201811132000"

    conditions = AppConditions()
    phoneType = ['ANDROID']
    tags = ['标签2', '......']
    region = ['上海市']
    conditions.addCondition('phoneType', phoneType, OptType.OR)
    conditions.addCondition(AppConditions.TAG, tags, OptType.OR)
    conditions.addCondition(AppConditions.REGION, region, OptType.NOT)
    # message.setConditions(conditions)
    # message.pushNetWorkType = 1
    # 控速推送(条/秒)
    message.speed =10
    ret = push.pushMessageToApp(message, 'toApp_任务别名_可为空')
    print (ret)

def StartActivityTemplateDemo():
    template = StartActivityTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.intent = "intent:#Intent;component=com.pp.infonew/com.getui.demo.MainActivity;S.key1=value1;end"
    # template.title = "在1999年12月11日,世界末日大魔王从天而降"
    # template.text = "English"
    # template.isVibrate = True
    # template.isClearable = True
    # template.isRing = True
    return template



# 通知透传模板动作内容
def NotificationTemplateDemo():
    template = NotificationTemplate()
    template.appId = APPID
    template.appKey = APPKEY

    style0 = Style0()
    style0.title = "style0通知标题"
    style0.text = "sytle0通知内容"
    # style0.isRing = True
    # style0.isClearable = True
    # style0.isVibrate = True
    template.style = style0

    # style1 = Style1()
    # style1.title = "style1通知标题"
    # style1.text = "sytle1通知内容"
    # style1.isRing = False
    # style1.isClearable = False
    # style1.isVibrate = False
    # template.style = style1

    # style4 = Style4()
    # style4.banner_url = "https://www.baidu.com/img/bd_logo1.png"
    # # style4.isRing = False
    # # style4.isClearable = False
    # # style4.isVibrate = False
    # template.style = style4

    # style6 = Style6()
    # style6.title = "通知标题"
    # style6.text = "通知内容"
    # style6.bannerUrl = "https://www.baidu.com/img/bd_logo1.png"
    # template.style = style6

    template.transmissionType = 1
    template.transmissionContent = '{"key":"value"}'
    # begin = "2015-03-04 17:40:22"
    # end = "2015-03-04 17:47:24"
    # template.setDuration(begin, end)

    #短信相关
    # smsMessage = SMSDemo()
    # template.setSmsInfo(smsMessage)
    return template


# 通知链接模板动作内容
def LinkTemplateDemo():
    template = LinkTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    # template.title = "请填入通知标题"
    # template.text = "请填入通知内容"
    # # template.logo = ""
    # template.isRing = True
    # template.isVibrate = True
    # template.isClearable = True
    template.url = "http://www.baidu.com"

    style0 = Style0()
    style0.title = "style0"
    style0.text = "style0"
    # style0.isClearable = False
    # style0.isRing = False
    # style0.isVibrate = False
    template.style = style0

    # style1 = Style1()
    # style1.title = "style1"
    # style1.text = "style1"
    # template.style = style1


    # style4 = Style4()
    # style4.banner_url = "http://s1.hao123img.com/res/images/search_logo/image.png"
    # template.style = style4

    return template


# 透传模板动作内容
def TransmissionTemplateDemo():
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '中午你跟'
    notify = Notify()
    # notify.title = "titleee"
    # notify.content = "contentee"
    # notify.payload = 'payloadtest'
    # notify.type = NotifyInfo._payload

    # notify.title = "titleee"
    # notify.content = "contentee"
    # notify.intent = "intent:#Intent;component=com.pp.infonew/com.getui.demo.MainActivity;S.key1=value1;end"
    # notify.type = NotifyInfo._intent

    notify.title = "ThirdPartyUrl"
    notify.content = "contentee"
    notify.url = "http://www.getui.com"
    notify.type = NotifyInfo._url
    template.set3rdNotifyInfo(notify)

    # # APN简单推送
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = ""
    # apn = APNPayload()
    # apn.alertMsg = alertMsg
    # apn.badge = 2
    # apn.sound = ""
    # apn.addCustomMsg("payload", "payload")
    # apn.contentAvailable=1
    # apn.category="ACTIONABLE"
    # template.setApnInfo(apn)

    # APN高级推送
    apnpayload = APNPayload()
    apnpayload.autoBadge = "+1"
    apnpayload.sound = ""
    apnpayload.addCustomMsg("payload", "payload")
    apnpayload.contentAvailable = 1
    apnpayload.category = "ACTIONABLE"
    apnpayload.voicePlayType = 2
    apnpayload.voicePlayMessage = ""
    alertMsg = DictionaryAlertMsg()
    alertMsg.body = 'body'
    alertMsg.actionLocKey = 'actionLockey'
    alertMsg.locArgs = ['locArgs']
    alertMsg.launchImage = 'launchImage'
    # IOS8.2以上版本支持
    alertMsg.title = 'Title'
    alertMsg.titleLocArgs = ['TitleLocArg']
    alertMsg.titleLocKey = 'TitleLocKey'
    apnpayload.alertMsg = alertMsg
    # voIPPayload = VoIPPayload()
    # voIPPayload.setVoIPPayload("Payload")
    template.setApnInfo(apnpayload)
    return template


def SMSDemo():
    smsMessage = SmsMessage()
    smsContent = {}
    smsContent["url"] = "http://www.getui.com"
    smsMessage.smsContent = smsContent
    smsMessage.smsTemplateId = "9137608ccae841b29b40d6f97efc0521"
    smsMessage.offlineSendtime = 1000
    return smsMessage

# 获取用户状态
def getUserStatus():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    print (push.getClientIdStatus(APPID, CID))

# 任务停止功能
def stopTask():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    print (push.stop("OSA-1113_ckyvRe2JDS7uFgDHqiQZm5"))


# 根据ClientID设置标签功能
def setTag():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    tagList = ['标签1', '标签2', '......']
    print (push.setClientTag(APPID, CID, tagList))


# 根据taskId返回推送结果
def getPushResultTest():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    # 返回根据任务tasdkId返回数据
    print (push.getPushResult(TASKID))
    # 返回用户推送结果信息
    #     print push.queryAppPushDataByDate(APPID, "20150525")
    # 返回用户注册结果信息
    # print push.queryAppUserDataByDate(APPID, "20150525")

# 根据ClientID查询标签
def getUserTagsTest():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    dictz = push.getUserTags(APPID, CID)
    for key in dictz:
        print (key + ":" + str(dictz[key]))

def queryAppPushDataByDate():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.queryAppPushDataByDate(APPID, "20181023")
    print(res)

def queryAppUserDataByDate():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.queryAppUserDataByDate(APPID, "20180923")
    print(res)

def getPersonaTagsDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.getPersonaTags(APPID)
    print(res)
    for result in res["tags"]:
        print(result["desc"])

def getPushActionResultByTaskidsDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    taskIdList = [TASKID]
    actionIdList = ["90009"]
    res = push.getPushActionResultByTaskids(taskIdList,actionIdList)
    print(res)

def getPushResultByTaskidListDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    taskIdList = [TASKID, "GT_1101_aecab33f7f4c43f8af8995cf7001e638"]
    res = push.getPushResultByTaskidList(taskIdList)
    print(res)

def getPushResultByGroupNameDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.getPushResultByGroupName(APPID, GroupName)
    print(res)

def getLast24HoursOnlineUserStatisticsDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.getLast24HoursOnlineUserStatistics(APPID)
    print(res)

def queryUserCountDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cdt = AppConditions()
    # phoneTypeList = ['ANDROID']
    # provinceList = ['浙江省']
    # tagList = ['发生大幅度三']
    #新增机型
    # cdt.addCondition(AppConditions.PHONE_TYPE, phoneTypeList)
    #新增地区
    # cdt.addCondition(AppConditions.REGION,provinceList)
    #新增tag
    # cdt.addCondition(AppConditions.TAG,tagList)
    # response = push.getPersonaTags(APPID)
    # print(response)

    #新增用户对象
    # jobs = ["0102","0110"]
    # cdt.addCondition("job",jobs)
    # age = ["0000"]
    # cdt.addCondition("age",age)
    result = push.queryUserCount(APPID, cdt)
    print(result)

def getUserCountByTagsDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    tagList = ["标签2", "......"]
    res = push.getUserCountByTags(APPID, tagList)
    print(res)

def restoreCidListFromBlkDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cidList = [CID]
    res = push.restoreCidListFromBlk(APPID,cidList)
    print(res)

def addCidListToBlkDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cidList = [CID, ""]
    res = push.addCidListToBlk(APPID,cidList)
    print(res)

def setBadgeForCIDDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cidList = [CID]
    res = push.setBadgeForCID(Badge, APPID, cidList)
    print(res)

def setBadgeForDeviceTokenDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    deviceTokenList = ["67fdddedadd63f1fec55b5d74034d021ce76804f88c9e040e40372dc6e0c6dcd"]
    res = push.setBadgeForDeviceToken(Badge, APPID, deviceTokenList)
    print(res)

def pushTagMessageRetryDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = NotificationTemplate()
    template.appId = "s3olXQVg1d5mwSaZ2Oz642"
    template.appKey = "YZkTKbz91l84HyM0TGlb38"
    template.transmissionType = 2
    template.transmissionContent = "测试离线"
    message = IGtAppMessage()
    message.setOffline(False)
    message.setOfflineExpireTime(10 * 60 * 1000)
    message.setData(template)
    appidList = []
    appidList.append(APPID)
    message.setAppIdList(appidList)
    message.setSpeed(1)
    message.setTag("标签1")
    res = push.pushTagMessageRetry(message)
    print(res)

def pushTagMessageDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = LinkTemplateDemo()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1
    template.transmissionContent = "测试离线"
    message = IGtAppMessage()
    message.setOffline(True)
    message.setOfflineExpireTime(10 * 60 * 1000)
    message.setData(template)
    appidList = []
    appidList.append(APPID)
    message.setAppIdList(appidList)
    # message.setSpeed(1)
    message.setTag("标签3")
    res = push.pushTagMessage(message, "groupname")
    print(res)

def getScheduleTaskDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.getScheduleTask(TASKID,APPID)
    print(res)

def delScheduleTaskDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.delScheduleTask(TASKID, APPID)
    print(res)

def bindCidPnDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cid = hashlib.md5(PN.encode('utf8')).hexdigest()
    params = {}
    params[CID] = cid
    # params["d0d4c3315e49e2868c7fd235379d32ed"] = PN
    res = push.bindCidPn(APPID,params)
    print(res)

def unbindCidPnDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cids = [CID]
    res = push.unbindCidPn(APPID,cids)
    print(res)

def queryCidPnDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    cidList = [CID]
    res = push.queryCidPn(APPID,cidList)
    print(res)

def stopSendSmsDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.stopSendSms(APPID, TASKID)
    print(res)


def pushMessageToSingleToSMS():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = TransmissionTemplateDemo()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = 2
    template.transmissionType = "透传内容"

    smsMessage = SmsMessage()
    smsContent = {}
    smsContent["url"] = "http://www.getui.com"
    # smsContent = {}
    # smsContent["name"] = "${name}"
    # smsContent["money"] = "${money}"

    smsMessage.payload = "1234"
    smsMessage.smsContent = smsContent
    smsMessage.smsTemplateId = "d0d4c3315e49e2868c7fd235379d32ed"
    smsMessage.url = "www.getui.com"
    smsMessage.offlineSendtime = 1000
    template.setSmsInfo(smsMessage)
    print (template.getTransparent())
    message = IGtSingleMessage()
    # 是否离线推送
    message.isOffline = True
    # 离线有效时间
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    # 推送的网络类型：(0:不限;1:wifi;2:4G/3G/2G)
    # message.pushNetWorkType = 2

    target = Target()
    target.appId = APPID
    target.clientId = CID

    try:
        ret = push.pushMessageToSingle(message, target)
        print (ret)
    except RequestException as e:
        requstId = e.getRequestId()
        ret = push.pushMessageToSingle(message, target, requstId)
        print (ret)



#消息推送接口
# pushMessageToSingle()
# pushMessageToList()
# pushMessageToApp()
pushMessageToSingleBatch()
# pushTagMessageDemo()
# pushTagMessageRetryDemo()

# -----------短信相关
# bindCidPnDemo()
# queryCidPnDemo()
# unbindCidPnDemo()

# ----------报表统计
#获取24小时在线用户数
# getLast24HoursOnlineUserStatisticsDemo()
#根据条件查询用户总数
# queryUserCountDemo()
# 根据TaskID返回任务推送结果功能
# getPushResultTest()
#根据Taskid列表返回推送结果
# getPushResultByTaskidListDemo()
#根据taskid获取自定义推送数据报表
# getPushActionResultByTaskidsDemo()
#根据日期获取APP推送报表
# queryAppPushDataByDate()
#根据用户标签获取用户总数
# getUserCountByTagsDemo()
#根据推送组名，返回推送结果
# getPushResultByGroupNameDemo()
#获取当日用户数据
# queryAppUserDataByDate()
# 获取用户状态接口
# getUserStatus()
#----------其他接口------------
# 通过服务端设置用户标签
# setTag()
# 根据ClientID查询标签功能
# getUserTagsTest()
#获取用户状态
# getUserStatus()
#获取其他标签接口
# getPersonaTagsDemo()
#获取定时任务
# getScheduleTaskDemo()
# delScheduleTaskDemo()
#根据CID初始化角标
# setBadgeForCIDDemo()
#根据DT初始化角标
# setBadgeForDeviceTokenDemo()
#停止短信发送
# stopSendSmsDemo()
# 任务停止功能接口
# stopTask()
#取消cid黑名单
# restoreCidListFromBlkDemo()
#设置cid黑名单
# addCidListToBlkDemo()
