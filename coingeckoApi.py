import const
import httpReq

def getTokenDetailNyTokenId(tokenId: str) :
    url = f"{const.coingeckoApiPath}/coins/{tokenId}"
    return httpReq.send_get_request(url)

def getTokenDetailNyNetworkAndContract(platform: str,contract: str) :
    url = f"{const.coingeckoApiPath}/coins/{platform}/contract/{contract}"
    return httpReq.send_get_request(url)

def getCoins() :
    url = f"{const.coingeckoApiPath}/coins/list?include_platform=true"
    return httpReq.send_get_request(url)

def getCoinPrice(url: str):
    url = f"{const.coingeckoApiPath}/{url}"
    return httpReq.send_get_request(url)


def getSimpleCoinList():
    url = f"{const.coingeckoApiPath}/coins/list"
    return httpReq.send_get_request(url)
