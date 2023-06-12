import const
import json
from typing import List
from dataclasses import dataclass
from dataclasses import asdict



@dataclass
class Coin:
    id: str
    symbol: str
    name: str
    platforms: dict

@dataclass
class CoinGeckoCoin:
    id: str
    symbol: str
    name: str
    asset_platform_id: str
    platforms: dict
    detail_platforms: dict
    block_time_in_minutes: int
    hashing_algorithm: str
    categories: list
    public_notice: str
    additional_notices: list
    localization: dict
    description: dict
    links: dict
    image: dict
    country_origin: str
    genesis_date: str
    contract_address: str
    sentiment_votes_up_percentage: float
    sentiment_votes_down_percentage: float
    watchlist_portfolio_users: int
    market_cap_rank: int
    coingecko_rank: int
    coingecko_score: float
    developer_score: float
    community_score: float
    liquidity_score: float
    public_interest_score: float
    market_data: dict
    community_data: dict
    developer_data: dict
    public_interest_stats: dict
    status_updates: list
    last_updated: str
    tickers: list

def coin_to_dict(coin):
    return coin.__dict__

def dict_to_coin(d):
    coin = CoinGeckoCoin(
        id='',
        symbol='',
        name='',
        asset_platform_id='',
        platforms={},
        detail_platforms={},
        block_time_in_minutes=0,
        hashing_algorithm='',
        categories=[],
        public_notice='',
        additional_notices=[],
        localization={},
        description={},
        links={},
        image={},
        country_origin='',
        genesis_date='',
        contract_address='',
        sentiment_votes_up_percentage=0.0,
        sentiment_votes_down_percentage=0.0,
        watchlist_portfolio_users=0,
        market_cap_rank=0,
        coingecko_rank=0,
        coingecko_score=0.0,
        developer_score=0.0,
        community_score=0.0,
        liquidity_score=0.0,
        public_interest_score=0.0,
        market_data={},
        community_data={},
        developer_data={},
        public_interest_stats={},
        status_updates=[],
        last_updated='',
        tickers=[]
    )

    coin.__dict__.update(d)
    return coin

def getCoinsJson(coins):
    return remove_backticks(json.dumps(coins, default=lambda o: asdict(o), indent=4, ensure_ascii=False))
    

def remove_backticks(json_str):
    if json_str.startswith('"') and json_str.endswith('"'):
        json_str = json_str[1:-1]
    return json_str

def getCoinObjectFronJson(jsonStr : str):
    if (jsonStr):
        data = json.loads(jsonStr)
        return CoinGeckoCoin(**data)
    else:
        return None

def convertCoinObjectToJson(coin : CoinGeckoCoin):
    return json.dumps(coin.__dict__, indent=4)

def correctCoingeckoCoin(coinId : str,jsonStr : str):
    if mustCoinIdAdd(coinId):
        coin = getCoinObjectFronJson(jsonStr)
        cs = getCoinListForAdd(coinId)
        cl = getCoinListInDetailForAdd(coinId)
        coin.platforms.update(cs)
        coin.detail_platforms.update(cl)
        return convertCoinObjectToJson(coin)
    else:
        return jsonStr
    
    

def getCoinId(coinId : str):
    coinId = coinId.upper()
    for cId in const.coinId:
        if (coinId == cId):
            return const.coinId[cId]
    return coinId

def getCoinList(jsonStr : str):
    data = json.loads(jsonStr)
    coins = []
    for item in data:
        coin = Coin(**item)
        coins.append(coin)
    return coins

def addMyNetwork(json : str):
   coins =  getCoinList(json)
   for coin in coins:
       for network in const.coinMap:
           for tokens in network.tokens :
               print (tokens)



def mustAddToken(network,coinId):
    return getContractOfToken(network,coinId) != None

def getContractOfToken(networkId,coinId):
    for network in const.coinMap:
        if network["network"] == networkId:
            if "tokens" in network:
                tokens = network["tokens"]
                if coinId in tokens:
                    return tokens[coinId]
                

def mustCoinIdAdd(coinId):
    coin = getCoinListForAdd(coinId)
    if coin:
        return True
    else:
        return False 
                
def getCoinListForAdd(coinId):
    coin = dict()
    for network in const.coinMap:
        if mustAddToken(network["network"],coinId):
            coin[network["network"]] = getContractOfToken(network["network"],coinId)
    return coin

def getCoinListInDetailForAdd(coinId):
    coin = dict()
    for network in const.coinMap:
        net = network["network"]
        if mustAddToken(net,coinId):
            coin[net] = {"decimal_place": 18, "contract_address": getContractOfToken(net,coinId)}
    return coin


def addNetworkAndContractToCoins(coins: List[Coin]):
    for index, coin in enumerate(coins):
        if mustCoinIdAdd(coin.id):
            if isinstance(coin.platforms, dict):
                cl = getCoinListForAdd(coin.id)
                coins[index].platforms.update(cl)
    return coins

def correctCoinList(jsonStr: str) :
    coins = getCoinList(jsonStr)
    coins = addNetworkAndContractToCoins(coins)
    return getCoinsJson(coins)

def getAllcontractsOfAllNetworks():
    contracts = []
    for network in const.coinMap:
        if "tokens" in network:
            for value in network["tokens"].values():
                if (value not in contracts):
                    contracts.append(value)
    return contracts

def getBscContractMapToContract(contract: str):
    for key,value in const.contractMapWithBsc.items():
        if key.upper() == contract.upper():
            return value
    return contract

def getNetworkContractMapToBscContract(contract: str):
    for key,value in const.contractMapWithBsc.items():
        if value.upper() == contract.upper():
            return key
    return contract

def chagePriceResultForblockscout(res: str):
    for key,value in const.contractMapWithBsc.items():
        res = res.replace(value,key)
    return res

def generateAddressForCoingeckoPrice(contractsAdr : str):
    contracts = contractsAdr.split(",")
    for index, contract in enumerate(contracts):
        contracts[index] = getBscContractMapToContract(contract)
    return  const.coingeckoApiPath + "/simple/token_price/binance-smart-chain?vs_currencies=usd&include_market_cap=true&contract_addresses=" + ",".join(contracts)


    

    




            
        

        

