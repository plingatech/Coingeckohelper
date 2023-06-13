from fastapi import FastAPI
from fastapi import Response
from datetime import date
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
import json

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
    if "Exchangerate" in const.cache:
        logger.info ("return exchangerate from cache")
        return JSONResponse(content=jsonable_encoder(const.cache["Exchangerate"]), status_code=status.HTTP_200_OK)
    else:
        result = coingeckoApi.getExchangerate()
        const.cache["Exchangerate"] = result
        return Response(content=result, media_type='application/json')

@app.get("/api/v1/coins/list")
def getCoinListWithPlatform(include_platform = None):
    if include_platform:
        if "CoinListWithPlatform" in const.cache:
            logger.info ("return CoinList with platform from cache")
            res = const.cache.get("CoinListWithPlatform")
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        else:
            result = mapHelper.correctCoinList(coingeckoApi.getCoins())
            const.cache["CoinListWithPlatform"] = jsonable_encoder(result)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
    else:
        if "CoinList" in const.cache:
            logger.info ("return CoinList from cache")
            return JSONResponse(content=jsonable_encoder(const.cache["CoinList"]), status_code=status.HTTP_200_OK)
        else:
            result = coingeckoApi.getSimpleCoinList()
            const.cache["CoinList"] = result
            return Response(content=result, media_type='application/json')

@app.get("/api/v1/coins/{id}")
def getCoinById(id : str):
    key = f"coin_coinid_{id}"
    if key in const.cache:
        logger.info (f"return coinid {id} from cache")
        return JSONResponse(content=jsonable_encoder(const.cache[key]), status_code=status.HTTP_200_OK)
    else:
        result = mapHelper.correctCoingeckoCoin(id,coingeckoApi.getTokenDetailNyTokenId(id))
        const.cache[key] = jsonable_encoder(result)
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@app.get("/api/v1/coins/{platform}/contract/{contract}")
def getCoinByNetworkAndContract(platform : str,contract: str):
    key = f"coin_platform_contract_{platform}_{contract}"
    if key in const.cache:
        logger.info (f"return coin_platform_contract {platform} {contract} from cache")
        return JSONResponse(content=jsonable_encoder(const.cache[key]), status_code=status.HTTP_200_OK)
    else:
        coinId = mapHelper.getCoinIdOfContract(contract)
        result = mapHelper.correctCoingeckoCoin(coinId,coingeckoApi.getTokenDetailNyTokenId(coinId))
        const.cache[key] = jsonable_encoder(result)
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@app.get("/api/v1/simple/token_price/{platform}")
def getCoin(platform, vs_currencies, contract_addresses):
    key = f"coin_platform_Currency_contract_{platform}_{vs_currencies}_{contract_addresses}"
    if key in const.cache:
        logger.info (f"return coin_platform_Currency_contract {platform} {vs_currencies} {contract_addresses} from cache")
        return Response(content=const.cache[key], media_type='application/json')
    else:
        contract_addresses = mapHelper.chagePriceResultForCoinGecko(contract_addresses)
        queryStr = mapHelper.generateAddressForCoingeckoPrice(const.usedPlatform,contract_addresses,vs_currencies)
        rawRes = coingeckoApi.getCoinPrice(queryStr)
        result = mapHelper.chagePriceResultForblockscout(rawRes)
        const.cache[key] = jsonable_encoder(result)
        return Response(content=result, media_type='application/json')



