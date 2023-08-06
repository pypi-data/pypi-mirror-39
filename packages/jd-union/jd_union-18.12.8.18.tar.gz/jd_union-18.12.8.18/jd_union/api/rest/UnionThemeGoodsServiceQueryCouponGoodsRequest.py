from jd_union.api.base import RestApi

class UnionThemeGoodsServiceQueryCouponGoodsRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			RestApi.__init__(self,domain, port)
			self.from = None
			self.pageSize = None
			self.cid3 = None

		def getapiname(self):
			return 'jingdong.UnionThemeGoodsService.queryCouponGoods'




