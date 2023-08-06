from .AbstractNotifyStyle import *
from getuipy.protobuf.gt_req_pb2 import InnerFiled

class Style0(AbstractNotifyStyle):
    def __init__(self):
        AbstractNotifyStyle.__init__(self)
        self.text = ""
        self.title = ""
        self.logo = ""
        self.logoUrl = ""
        self.isRing = True
        self.isVibrate = True
        self.isClearable = True
    def getActionChain(self):
        title_F = self.actionChainBuilder.field.add()
        title_F.key = "title"
        title_F.val = self.title
        title_F.type = InnerFiled.str

        text_F = self.actionChainBuilder.field.add()
        text_F.key = "text"
        text_F.val = self.text
        text_F.type = InnerFiled.str

        logo_F = self.actionChainBuilder.field.add()
        logo_F.key = "logo"
        logo_F.val = self.logo
        logo_F.type = InnerFiled.str

        logo_url_F = self.actionChainBuilder.field.add()
        logo_url_F.key = "logo_url"
        logo_url_F.val = self.logoUrl
        logo_url_F.type = InnerFiled.str

        notifyStyle_F = self.actionChainBuilder.field.add()
        notifyStyle_F.key = "notifyStyle"
        notifyStyle_F.val = "0"
        notifyStyle_F.type = InnerFiled.int32

        isRing_F = self.actionChainBuilder.field.add()
        isRing_F.key = "is_noring"
        isRing_F.val = str(False if self.isRing else True)
        isRing_F.type = InnerFiled.bool

        isClearable_F = self.actionChainBuilder.field.add()
        isClearable_F.key = "is_noclear"
        isClearable_F.val = str(False if self.isClearable else True)
        isClearable_F.type = InnerFiled.bool

        isVibrate_F = self.actionChainBuilder.field.add()
        isVibrate_F.key = "is_novibrate"
        isVibrate_F.val = str(False if self.isVibrate else True)
        isVibrate_F.type = InnerFiled.bool
        return self.actionChainBuilder