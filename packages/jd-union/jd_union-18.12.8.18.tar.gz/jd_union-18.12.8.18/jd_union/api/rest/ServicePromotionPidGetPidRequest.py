from jd_union.api.base import RestApi

class ServicePromotionPidGetPidRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.unionId = None
			self.sonUnionId = None
			self.mediaName = None
			self.positionName = None
			self.promotionType = None

		def getapiname(self):
			return 'jingdong.service.promotion.pid.getPid'




