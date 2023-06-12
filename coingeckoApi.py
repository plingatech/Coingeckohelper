import const
import httpReq

def getTokenDetail(tokenId) :
    url = f"{const.coingeckoApiPath}/coins/{tokenId}"
    return httpReq.send_get_request(url)

def getCoins() :
    url = f"{const.coingeckoApiPath}/coins/list?include_platform=true"
    return httpReq.send_get_request(url)

def getCoinPrice(url: str):
    url = f"{const.coingeckoApiPath}/{url}"
    return httpReq.send_get_request(url)
