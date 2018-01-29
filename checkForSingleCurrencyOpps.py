# Name: 
# Author: Patrick Mullaney
# Date Created: 1-20-2018
# Last Edited: 1-9-2018
# Description: This script checks for arbitrage opportunities.

# Opportunity object stores the potential info about an exchange.
class Opportunity():
    currency = None
    buyExchange = None
    sellExchange = None
    amount = None
    profitLoss = 0.00

# Exchange object contains information relevant to that exchange.    
class Exchange(): 
    name = None
    currency = None
    price = None
    depositFee = None
    withdrawFee = None
    exchangeFee = None
    # Add different fees for maker/taker?

# Returns exchange fee.
def getExchangeFee(exchange):
    if exchange is "gdax":
        fee = 1.0
    elif exchange is "gemini":
        fee = 0.5
    return fee

# Takes the amount of coins, information about the high-price exchange, low-price exchange, and returns info about arbitrage opportunity.
def calculateProfitLoss(amount, high, low):
    # amountCoins = amount
    # Fiat deposit fee in %.
    depositCost = (100.00 - low.depositFee)/100.00
    
    # Exchange fee of lower currency in %.
    exchangeCostLow = (100.00 - low.exchangeFee)/100.00
  
    # Exchange fee of higher currency in %.
    exchangeCostHigh = (100.00 - high.exchangeFee)/100.00
    
    # Fiat withdrawal fee in %.
    withdrawCost = (100.00 - high.withdrawFee)/100.00
    
    # Calculate revenue.
    revenue = ((((amount * low.price) * depositCost)/low.price * exchangeCostLow) * high.price * exchangeCostHigh) * withdrawCost
 
    # Profit/loss = revenue - investment.
    profit = revenue - (low.price * amount)
    # Round down to two decimals.
    profit = '${:,.2f}'.format(profit)
    # Create opportunity object
    arbitrage = Opportunity()
    arbitrage.buyExchange = low.name
    arbitrage.sellExchange = high.name
    arbitrage.profitLoss = profit
    # Optimize by include exchange prices/fees?
    
    return arbitrage

# Check opportunity
def checkOpportunity(amount, gdax, gemini):
    
    # If GDAX price is higher.
    if gdax.price > gemini.price:
        # Calculate profit/loss opportunity.
        opportunity = calculateProfitLoss(amount, gdax, gemini)
        return opportunity
    # Else if Gemini price is higher.
    elif gdax.price < gemini.price:
        # Calculate profit/loss opportunity.
        opportunity = calculateProfitLoss(amount, gemini, gdax)
        return opportunity
    # Else prices equal, no arbitrage opportunity.
    elif gdax.price == gemini.price:
        return None

def checkAllCurrencies():
    # Optimize amounts?
    amount = 100
    
    # Bitcoin Cash (BCH)
    # GDAX bitcoin exchange info.
    gdaxBch = Exchange()
    gdaxBch.name = "gdax"
    gdaxBch.currency = "BCH"
    gdaxBch.price = 650.00
    gdaxBch.withdrawFee = 2
    gdaxBch.exchangeFee = getExchangeFee(gdaxBch.name)
    gdaxBch.depositFee = 1

    # Gemini bitcoin exchange info.
    geminiBch = Exchange()
    geminiBch.name = "gdax"
    geminiBch.currency = "BCH"
    geminiBch.price = 636.00
    geminiBch.withdrawFee = 1
    geminiBch.exchangeFee = getExchangeFee(geminiBch.name)
    geminiBch.depoositFee = 1

    # Check opportunities for bitcoin.
    oppBch = checkOpportunity(amount, gdaxBch, geminiBch)
    
    # Ethereum (ETH)
    # GDAX ethereum exchange info.
    gdaxEth = Exchange()
    gdaxEth.name = "gdax"
    gdaxEth.currench = "ETH"
    gdaxEth.price = 250.00
    gdaxEth.withdrawFee = 2
    gdaxEth.exchangeFee = getExchangeFee(gdaxEth.name)
    gdaxEth.depositFee = 1
    
    # Gemini ethereum exchange info.
    geminiEth = Exchange()
    geminiEth.name = "gemini"
    geminiEth.currency = "ETH"
    geminiEth.price = 200.00
    geminiEth.withdrawFee = 1
    geminiEth.exchangeFee = getExchangeFee(geminiEth.name)
    geminiEth.depoositFee = 1

    # Check opportunities for ethereum.
    oppEth = checkOpportunity(amount, gdaxEth, geminiEth)
    
    # Litecoin (LTC)
    # GDAX litecoin exchange info.
    gdaxLtc = Exchange()
    gdaxLtc.name = "gdax"
    gdaxLtc.currency = "LTC"
    gdaxLtc.price = 350.00
    gdaxLtc.withdrawFee = 2
    gdaxLtc.exchangeFee = getExchangeFee(gdaxLtc.name)
    gdaxLtc.depositFee = 1

    # Gemini litecoin exchange info.
    geminiLtc = Exchange()
    geminiLtc.name = "gemini"
    geminiLtc.currency = "LTC"
    geminiLtc.price = 300.00
    geminiLtc.withdrawFee = 1
    geminiLtc.exchangeFee = getExchangeFee(geminiLtc.name)
    geminiLtc.depoositFee = 1

    # Check opportunities for litecoin.
    oppLtc = checkOpportunity(amount, gdaxLtc, geminiLtc)
    
    # Bitcoin Core (BTC)
    # GDAX BTC exchange info.
    gdaxBtc = Exchange()
    gdaxBtc.name = "gdax"
    gdaxBtc.currency = "BTC"
    gdaxBtc.price = 450.00
    gdaxBtc.withdrawFee = 2
    gdaxBtc.exchangeFee = getExchangeFee(gdaxBtc.name)
    gdaxBtc.depositFee = 1

    # Gemini BTC exchange info.
    geminiBtc = Exchange()
    geminiBtc.name = "gemini"
    geminiBtc.currency = "BTC"
    geminiBtc.price = 400.00
    geminiBtc.withdrawFee = 1
    geminiBtc.exchangeFee = getExchangeFee(geminiBtc.name)
    geminiBtc.depoositFee = 1

    # Check opportunities for litecoin.
    oppBtc = checkOpportunity(amount, gdaxBtc, geminiBtc)
    
    # Return array of arbitrage opportunities.
    arbOpps = [oppBch, oppEth, oppLtc, oppBtc]
    return arbOpps