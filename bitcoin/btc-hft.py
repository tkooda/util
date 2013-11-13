#!/usr/bin/python

## tkooda : 2011-08-25 : Bitcoin High Frequency Trading

## just a web app to extimate potential profit from trading between bitcoin exchanges


## TODO:
##  - figure out actual cost of a trade and compare that instead of listed cost
##    - also factor in withdrawl cost (from account)
##  - need to be able to examine my own outstanding orders, and cancel them if needed
##  - 
##  - 
##  - 


import os
import sys
import time
import json
import urllib2


## market volumes:  http://bitcoincharts.com/markets/


def poll_mtgox():
    # no BTC deposit fee : https://en.bitcoin.it/wiki/MtGox#Fees , https://mtgox.com/fee-schedule
#    url = "http://data.mtgox.com/api/1/BTCUSD/ticker"
#                   "ask_usd": float( data[ "return" ][ "sell" ][ "value" ] ),
#                   "bid_usd": float( data[ "return" ][ "buy"  ][ "value" ] ),
    url = "http://data.mtgox.com/api/1/BTCUSD/depth/fetch"
    # https://data.mtgox.com/api/1/generic/order/lag
    try:
        data = json.load( urllib2.urlopen( url ) )
#        print json.dumps( data, indent = 2 )
        if data[ "result" ] != "success":
            return
        
        max_bid = None
        for bid in data[ "return" ][ "bids" ]:
            if not max_bid or float( bid[ "price" ] ) > float( max_bid[ "price" ] ):
                max_bid = bid
        
        min_ask = None
        for ask in data[ "return" ][ "asks" ]:
            if not min_ask or float( ask[ "price" ] ) < float( min_ask[ "price" ] ):
                min_ask = ask
        
        mydata = { "time": time.time(),
                   "name": "mtgox",
                   "ask_usd": min_ask[ "price" ],
                   "ask_qty": min_ask[ "amount" ],
                   "bid_usd": max_bid[ "price" ],
                   "bid_qty": max_bid[ "amount" ],
                   "fee_percent": 0.006,
                   }
        return mydata
    except:
        import traceback
        traceback.print_exc( file=sys.stderr )
        sys.stderr.flush()
        pass



def poll_bitstamp():
#    url = "https://www.bitstamp.net/api/ticker/"
#                   "ask_usd": float( data[ "ask" ] ),
#                   "bid_usd": float( data[ "bid" ] ),
    url = "https://www.bitstamp.net/api/order_book/"
    try:
        data = json.load( urllib2.urlopen( url ) )
#        print json.dumps( data, indent = 2 )
        
        max_bid = None
        for bid in data[ "bids" ]:
            if not max_bid or float( bid[ 0 ] ) > float( max_bid[ 0 ] ):
                max_bid = bid
        
        min_ask = None
        for ask in data[ "asks" ]:
            if not min_ask or float( ask[ 0 ] ) < float( min_ask[ 0 ] ):
                min_ask = ask
        
        mydata = { "time": time.time(),
                   "name": "bitstamp",
                   "ask_usd": float( min_ask[ 0 ] ),
                   "ask_qty": float( min_ask[ 1 ] ),
                   "bid_usd": float( max_bid[ 0 ] ),
                   "bid_qty": float( max_bid[ 1 ] ),
                   "fee_percent": 0.005,
                   }
        return mydata
    except:
        import traceback
        traceback.print_exc( file=sys.stderr )
        sys.stderr.flush()
        pass



def poll_bitfloor():
    url = "https://api.bitfloor.com/book/L1/1" # includes order pair
    try:
        data = json.load( urllib2.urlopen( url ) )
#        print json.dumps( data, indent = 2 )
        mydata = { "time": time.time(),
                   "name": "bitfloor",
                   "ask_usd": float( data[ "ask" ][ 0 ] ),
                   "ask_qty": float( data[ "ask" ][ 1 ] ),
                   "bid_usd": float( data[ "bid" ][ 0 ] ),
                   "bid_qty": float( data[ "bid" ][ 1 ] ),
                   "fee_percent": 0.004,
                   }
        return mydata
    except:
        import traceback
        traceback.print_exc( file=sys.stderr )
        sys.stderr.flush()
        pass


def poll_btce():
    url = "https://btc-e.com/api/2/btc_usd/depth"
    try:
        data = json.load( urllib2.urlopen( url ) )
#        print json.dumps( data, indent = 2 )
        
        max_bid = None
        for bid in data[ "bids" ]:
            if not max_bid or float( bid[ 0 ] ) > float( max_bid[ 0 ] ):
                max_bid = bid
        
        min_ask = None
        for ask in data[ "asks" ]:
            if not min_ask or float( ask[ 0 ] ) < float( min_ask[ 0 ] ):
                min_ask = ask
        
        mydata = { "time": time.time(),
                   "name": "btce",
                   "ask_usd": float( min_ask[ 0 ] ),
                   "ask_qty": float( min_ask[ 1 ] ),
                   "bid_usd": float( max_bid[ 0 ] ),
                   "bid_qty": float( max_bid[ 1 ] ),
                   "fee_percent": 0.002,
                   }
        return mydata
    except:
        import traceback
        traceback.print_exc( file=sys.stderr )
        sys.stderr.flush()
        pass


def poll_btc24():
    url = "https://bitcoin-24.com/api/USD/orderbook.json"
    try:
        data = json.load( urllib2.urlopen( url ) )
#        print json.dumps( data, indent = 2 )
        
        max_bid = None
        for bid in data[ "bids" ]:
            if not max_bid or float( bid[ 0 ] ) > float( max_bid[ 0 ] ):
                max_bid = bid
        
        min_ask = None
        for ask in data[ "asks" ]:
            if not min_ask or float( ask[ 0 ] ) < float( min_ask[ 0 ] ):
                min_ask = ask
        
        mydata = { "time": time.time(),
                   "name": "btc24",
                   "ask_usd": float( min_ask[ 0 ] ),
                   "ask_qty": float( min_ask[ 1 ] ),
                   "bid_usd": float( max_bid[ 0 ] ),
                   "bid_qty": float( max_bid[ 1 ] ),
                   "fee_percent": 0, # FIXME: really?
                   }
        return mydata
    except:
        import traceback
        traceback.print_exc( file=sys.stderr )
        sys.stderr.flush()
        pass



poll_sets = []
poll_sets.append( poll_mtgox() )
poll_sets.append( poll_btce() )
poll_sets.append( poll_bitstamp() )
poll_sets.append( poll_bitfloor() )
poll_sets.append( poll_btc24() )


#poll_sets = [{'ask_qty': '?', 'fee_sell': 1, 'name': 'mtgox', 'fee_buy': 1, 'time': 1365643952.267199, 'bid_qty': '?', 'ask_usd': 178.0, 'bid_usd': 176.5}, {'ask_qty': '?', 'fee_sell': 1, 'name': 'bitstamp', 'fee_buy': 1, 'time': 1365643952.610707, 'bid_qty': '?', 'ask_usd': 175.0, 'bid_usd': 174.03}, {'ask_qty': 0.858, 'fee_sell': 1, 'name': 'bitfloor', 'fee_buy': 1, 'time': 1365643952.829987, 'bid_qty': 5.88736, 'ask_usd': 183.82, 'bid_usd': 177.89}]
#poll_sets = [{'ask_qty': '?', 'fee_sell': 1, 'name': 'mtgox', 'fee_buy': 1, 'time': 1365644122.113184, 'bid_qty': '?', 'ask_usd': 174.1119, 'bid_usd': 174.111}, {'ask_qty': '?', 'fee_sell': 1, 'name': 'bitstamp', 'fee_buy': 1, 'time': 1365644123.337326, 'bid_qty': '?', 'ask_usd': 174.99, 'bid_usd': 174.02}, {'ask_qty': 5.20292, 'fee_sell': 1, 'name': 'bitfloor', 'fee_buy': 1, 'time': 1365644124.783869, 'bid_qty': 0.1, 'ask_usd': 182.9, 'bid_usd': 178.02}]
#poll_sets = [{'ask_qty': '?', 'fee_sell': 0.006, 'name': 'mtgox', 'fee_buy': 0.006, 'time': 1365645072.947743, 'bid_qty': '?', 'ask_usd': 170.0, 'bid_usd': 168.777}, {'ask_qty': 2.00020054, 'fee_sell': 1, 'name': 'bitstamp', 'fee_buy': 1, 'time': 1365645073.188281, 'bid_qty': 1.24400361, 'ask_usd': 98000.0, 'bid_usd': 162.01}, {'ask_qty': 0.28, 'fee_sell': 1, 'name': 'bitfloor', 'fee_buy': 1, 'time': 1365645073.449127, 'bid_qty': 25.542, 'ask_usd': 175.99, 'bid_usd': 175.0}] # net profit: $ 127.71
# [{'ask_qty': 20.12683961, 'fee_sell': 0.006, 'name': 'mtgox', 'fee_buy': 0.006, 'time': 1365648952.319572, 'bid_qty': 0.08994817, 'ask_usd': 172, 'bid_usd': 157.44999}, {'ask_qty': 20.17465997, 'fee_sell': 1, 'name': 'bitstamp', 'fee_buy': 1, 'time': 1365648952.585542, 'bid_qty': 4.0, 'ask_usd': 156.82, 'bid_usd': 155.5}, {'ask_qty': 20.0, 'fee_sell': 1, 'name': 'bitfloor', 'fee_buy': 1, 'time': 1365648952.812141, 'bid_qty': 1.99184, 'ask_usd': 173.08, 'bid_usd': 167.26}] # $20

print "HTTP/1.0 200 OK"
print "Content-Type: text/plain"
print


#print json.dumps( poll_sets, indent = 2 )
print poll_sets
print

max_ask = None
min_ask = None
max_bid = None
min_bid = None

## find min/max ask/bid ..
print "polling exchanges:",
for poll_set in poll_sets:
    if not poll_set:
        continue
    
    print poll_set[ "name" ],
    
    if not max_ask or poll_set[ "ask_usd" ] > max_ask[ "ask_usd" ]:
        max_ask = poll_set
    
    if not min_ask or poll_set[ "ask_usd" ] < min_ask[ "ask_usd" ]:
        min_ask = poll_set
    
    if not max_bid or poll_set[ "bid_usd" ] > max_bid[ "bid_usd" ]:
        max_bid = poll_set
    
    if not min_bid or poll_set[ "bid_usd" ] < min_bid[ "bid_usd" ]:
        min_bid = poll_set
print
print


print "min_bid:", min_bid[ "name" ], ": $%0.2f" % float( min_bid[ "bid_usd" ] )
print "min_ask:", min_ask[ "name" ], ": $%0.2f" % float( min_ask[ "ask_usd" ] )
print "max_bid:", max_bid[ "name" ], ": $%0.2f" % float( max_bid[ "bid_usd" ] )
print "max_ask:", max_ask[ "name" ], ": $%0.2f" % float( max_ask[ "ask_usd" ] )
print


## buy as low as possible, sell as high as possible ..
if min_ask[ "name" ] == max_bid[ "name" ]:
    print "no profit possible"
else:
    print "info A:", min_ask[ "name" ], "will sell", min_ask[ "ask_qty" ], "BTC at $%0.2f" % float( min_ask[ "ask_usd" ] )
    print "info B:", max_bid[ "name" ], "will buy",  max_bid[ "bid_qty" ], "BTC at $%0.2f" % float( max_bid[ "bid_usd" ] )
    print
    
    if min_ask[ "ask_qty" ] < max_bid[ "bid_qty" ]:
        min_ammt = float( min_ask[ "ask_qty" ] )
    else:
        min_ammt = float( max_bid[ "bid_qty" ] )
    
    buy_usd_total = float( min_ammt * float( min_ask[ "ask_usd" ] ) )
    buy_usd_fee = float( buy_usd_total * float( min_ask[ "fee_percent" ] ) )
    print "order 1: buy",  min_ammt, "BTC from", min_ask[ "name" ], "at $", min_ask[ "ask_usd" ], "(value: $%0.2f" % buy_usd_total , "%s%%" % ( "+%f" % ( 100 * min_ask[ "fee_percent" ] ) ).rstrip("0").rstrip("."), "fee: ~$%0.2f" % buy_usd_fee ,")"
    
    sell_usd_total = float( min_ammt * float( max_bid[ "bid_usd" ] ) )
    sell_usd_fee = float( sell_usd_total * float( min_ask[ "fee_percent" ] ) )
    print "order 2: sell", min_ammt, "BTC to", max_bid[ "name" ], "at $", max_bid[ "bid_usd" ], "(value: $%0.2f" % sell_usd_total , "%s%%" % ( "+%f" % ( 100 * max_bid[ "fee_percent" ] ) ).rstrip("0").rstrip(".") , "fee: ~$%0.2f" % sell_usd_fee ,")"
    print
    
    print "capitol required: $%0.2f" % ( buy_usd_total + buy_usd_fee ), "at", min_ask[ "name" ], "and", min_ammt, "BTC at", max_bid[ "name" ]
    print
    
    print "net profit for just this pair of trades: $%0.2f" % ( ( sell_usd_total + sell_usd_fee ) - ( buy_usd_total + buy_usd_fee ) )
    print

