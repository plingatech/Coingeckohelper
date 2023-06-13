coingeckoApiPath = "https://api.coingecko.com/api/v3"
coingeckoProApiPath = "https://pro-api.coingecko.com/api/v3"
logFile = "/var/log/coingeckoHelper/coingeckoHelper.log"

cache = {} 

coinId = {"USDT": "tether"}
contractMapWithBsc = {"0xbD07cf23A43f13078716A015F3Cc27F7a1661e65":"0x55d398326f99059ff775485246999027b3197955"}


coinMap = [{"network": "plinga" , "tokens" : {"tether" : "0xbD07cf23A43f13078716A015F3Cc27F7a1661e65"}}]

usedPlatform = "binance-smart-chain"