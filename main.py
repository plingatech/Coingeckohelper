from fastapi import FastAPI
from fastapi import Response
from datetime import date
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

import logging
from logging.handlers import SysLogHandler
import const
import coingeckoApi
import mapHelper

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = SysLogHandler(address='/dev/log')
handler.setLevel(logging.DEBUG)

# تنظیم فرمت پیام‌های لاگ
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# اضافه کردن handler به logger
logger.addHandler(handler)



app = FastAPI()
#print(coingeckoApi.getTokenDetail("tether"))
#print(mapHelper.mustCoinIdAdd("binance-usd"))
#print(mapHelper.correctCoinList(coingeckoApi.getCoins()))
#print(mapHelper.correctCoingeckoCoin("tether",coingeckoApi.getTokenDetail("tether")))
#print(mapHelper.getNetworkOfContract("0xbD07cf23A43f13078716A015F3Cc27F7a1661e65"))


@app.get("/api/v1/exchange_rates")
def getExchangerate():
    result = coingeckoApi.getExchangerate()
    return Response(content=result, media_type='application/json')

@app.get("/api/v1/coins/list")
def getCoinListWithPlatform(include_platform = None):
    if include_platform:
        result = mapHelper.correctCoinList(coingeckoApi.getCoins())
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
    else:
        result = coingeckoApi.getSimpleCoinList()
        return Response(content=result, media_type='application/json')

@app.get("/api/v1/coins/{id}")
def getCoinById(id : str):
    result = mapHelper.correctCoingeckoCoin(id,coingeckoApi.getTokenDetailNyTokenId(id))
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@app.get("/api/v1/coins/{platform}/contract/{contract}")
def getCoinByNetworkAndContract(platform : str,contract: str):
    coinId = mapHelper.getCoinIdOfContract(contract)
    result = mapHelper.correctCoingeckoCoin(coinId,coingeckoApi.getTokenDetailNyTokenId(coinId))
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@app.get("/api/v1/simple/token_price/{platform}")
def getCoin(platform, vs_currencies, contract_addresses):
    contract_addresses = mapHelper.chagePriceResultForCoinGecko(contract_addresses)
    queryStr = mapHelper.generateAddressForCoingeckoPrice(const.usedPlatform,contract_addresses,vs_currencies)
    logger.info(queryStr)
    rawRes = coingeckoApi.getCoinPrice(queryStr)
    result = mapHelper.chagePriceResultForblockscout(rawRes)
    return Response(content=result, media_type='application/json')



