from fastapi import FastAPI
import logging
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
print(mapHelper.generateAddressForCoingeckoPrice("0xbD07cf23A43f13078716A015F3Cc27F7a1661e65"))


@app.get("/api/v1/coins/list")
async def getCoinListWithPlatform(include_platform : str):
    logger.info("platform is {include_platform}")
    result = await mapHelper.correctCoinList(coingeckoApi.getCoins())
    return result

@app.get("/api/v1/coins/{id}")
async def getCoin(id : str):
    result = await mapHelper.correctCoingeckoCoin("tether",coingeckoApi.getTokenDetail("tether"))
    return result


@app.get("/api/v1/simple/token_price/{platform}?vs_currencies={currency}&include_market_cap=true&contract_addresses={joined_addresses}")
async def getCoin(platform, vs_currencies, contract_addresses):
    result = await mapHelper.correctCoingeckoCoin("tether",coingeckoApi.getTokenDetail("tether"))
    return result



