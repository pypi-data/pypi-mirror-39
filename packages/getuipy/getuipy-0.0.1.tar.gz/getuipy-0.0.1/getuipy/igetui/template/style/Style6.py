# -*- coding: utf-8 -*-
from .AbstractNotifyStyle import *
from getuipy.protobuf.gt_req_pb2 import InnerFiled


class Style6(AbstractNotifyStyle):
    def __init__(self):
        AbstractNotifyStyle.__init__(self)
        self.text = ""
        self.title = ""
        self.logo = ""
        self.logoUrl = ""
        self.bigStyle = ""
        self.bigImageUrl = ""
        self.bigText = ""
        self.bannerUrl = ""
    def getActionChain(self):
        # if self.bigStyle is "1":
        #     self.bigImageUrl =
        # if self.bigImageUrl is not None and self.bigImageUrl is not "":
        #     self.bigStyle = "1"
        # if self.bigText is not None and self.bigText is not "":
        #     self.bigStyle = "2"
        # if self.bigImageUrl is not None and self.bannerUrl is not None \
        #         and self.bigImageUrl is not "" and self.bannerUrl is not "":
        #     self.bigStyle = "3"
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
        notifyStyle_F.val = "6"
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

        bigStyle_F = self.actionChainBuilder.field.add()
        bigStyle_F.key = "bigStyle"
        bigStyle_F.val = str(self.bigStyle)
        bigStyle_F.type = InnerFiled.int32
        if self.bigStyle is "1":
            bigImageUrl_F = self.actionChainBuilder.field.add()
            bigImageUrl_F.key = "big_image_url"
            bigImageUrl_F.val = self.bigImageUrl
            bigImageUrl_F.type = InnerFiled.str

        if self.bigStyle is "2":
            bigText_F = self.actionChainBuilder.field.add()
            bigText_F.key = "big_text"
            bigText_F.val = self.bigText
            bigText_F.type = InnerFiled.str
        if self.bigStyle is "3":
            bannerUrl_F = self.actionChainBuilder.field.add()
            bannerUrl_F.key = "banner_url"
            bannerUrl_F.val = self.bannerUrl
            bannerUrl_F.type = InnerFiled.str

            bigImageUrl_F = self.actionChainBuilder.field.add()
            bigImageUrl_F.key = "big_image_url"
            bigImageUrl_F.val = self.bigImageUrl
            bigImageUrl_F.type = InnerFiled.str

        return self.actionChainBuilder
