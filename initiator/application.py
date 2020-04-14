#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
# from datetime import datetime
import quickfix as fix
import quickfix42 as fix42
import quickfix44 as fix44
import time
import logging
from model.logger import setup_logger
from model import Field

# configured
__SOH__ = chr(1)

# Logger
setup_logger('FIX', 'Logs/message.log')
logfix = logging.getLogger('FIX')


class Application(fix.Application):
    """FIX Application"""

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogon(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogout(self, sessionID): 
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        #logfix.info("S >> (%s)" % msg)
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        #logfix.info("R >> (%s)" % msg)
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        self.onMessage(message, sessionID)
        return

   
    def onMessage(self, message, sessionID):
        """on Message"""
        pass

    def run(self):
        """Run"""
        while 1:
            action = self.queryAction()
            if action == '1':
                self.queryEnterOrder()
            elif action == '2':
                self.queryCancelOrder()
            elif action == '3':
                self.queryReplaceOrder()
            elif action == '4':
                self.queryMarketDataRequest()
            elif action == '5':
                break
            elif action == '6':
                print( self.sessionID.getSenderCompID() )

    def queryAction(self):
        print("1) Enter Order\n2) Cancel Order\n3) Replace Order\n4) Market data test\n5) Quit")
        action  = input("Action: ")
        return action
    
    def queryEnterOrder(self):
        version = self.queryVersion()
        print(version)
        while version == 0:
            print("Invalid input")
            version = self.queryVersion()
        
        orderMsg = fix.Message()

        if version == 42:
            order = self.queryNewOrderSingle42()
        elif version == 44:
            order = self.queryNewOrderSingle44()
        else:
            print("No test for version " + str(version))

        if self.queryConfirm( "Send order (Y/N): " ):
            fix.Session.sendToTarget(order)
    
    def queryCancelOrder(self):
        print("queryCancelOrder called")
    
    def queryReplaceOrder(self):
        print("queryReplaceOrder called")
    
    def queryMarketDataRequest(self):
        print("queryMarketDataRequest called")

    def queryVersion(self):
        print("\n1) FIX.4.2\n2) FIX.4.4")
        value = input("BeginString: ")
        swichter = {
            '1': 42,
            '2': 44
        }

        return swichter.get(value, 0)
    
    def queryNewOrderSingle42(self):
        ordType = fix.OrdType()

        message = fix.Message()
        message.setField(self.queryClOrdID())
        message.setField(fix.HandlInst('1'))
        message.setField(self.querySymbol())
        message.setField(self.querySide())
        message.setField(fix.TransactTime())
        ordType = self.queryOrdType()
        message.setField(ordType)
        message.setField(self.queryOrderQty())
        message.setField(self.queryTimeInForce())

        if abc.getValue() == fix.OrdType_LIMIT or abc.getValue() == fix.OrdType_STOP_LIMIT:
            message.setField(self.queryPrice())

        if abc.getValue() == fix.OrdType_STOP or abc.getValue() == fix.OrdType_STOP_LIMIT:
            message.setField(self.queryStopPx())

        header = message.getHeader()
        self.queryHeader(header)

        newOrderSingle = fix42.NewOrderSingle(message)

        return newOrderSingle

    def queryNewOrderSingle44(self):
        ordType = fix.OrdType()

        message = fix44.NewOrderSingle()
        message.setField(self.queryClOrdID())
        message.setField(fix.HandlInst('1'))
        message.setField(self.querySymbol())
        message.setField(self.querySide())
        message.setField(fix.TransactTime())
        ordType = self.queryOrdType()
        message.setField(ordType)
        message.setField(self.queryOrderQty())
        message.setField(self.queryTimeInForce())
        message.setField(self.querySecurityExchange())
        message.setField(self.queryAccount())

        if ordType.getValue() == fix.OrdType_LIMIT or ordType.getValue() == fix.OrdType_STOP_LIMIT:
            message.setField(self.queryPrice())

        if ordType.getValue() == fix.OrdType_STOP or ordType.getValue() == fix.OrdType_STOP_LIMIT:
            message.setField(self.queryStopPx())

        header = message.getHeader()
        self.queryHeader(header)

        return message

    def queryClOrdID(self):
        value = input("ClOrdID: ")
        return fix.ClOrdID(value)
    
    def querySymbol(self):
        value = input("Symbol: ")
        return fix.Symbol( value )
    
    def querySide(self):
        print("1) Buy\n2) Sell\n3) Sell Short\n4) Sell Short Exempt\n5) Cross\n6) Cross Short\n7) Cross Short Exempt")
        value = input("Side: ")

        if value == '1':
            return fix.Side( fix.Side_BUY )
        elif value == '2':
            return fix.Side( fix.Side_SELL )
        elif value == '3':
            return fix.Side( fix.Side_SELL_SHORT )
        elif value == '4':
            return fix.Side( fix.Side_SELL_SHORT_EXEMPT )
        elif value == '5':
            return fix.Side( fix.Side_CROSS )
        elif value == '6':
            return fix.Side( fix.Side_CROSS_SHORT )
        elif value == '7':
            return fix.Side( 'A' )
        else:
            pass
    
    def queryOrdType(self):
        print("1) Market\n2) Limit\n3) Stop\n4) Stop Limit")
        value = input("OrdType: ")

        if value == '1':
            return fix.OrdType( fix.OrdType_MARKET )
        elif value == '2':
            return fix.OrdType( fix.OrdType_LIMIT )
        elif value == '3':
            return fix.OrdType( fix.OrdType_STOP )
        elif value == '4':
            return fix.OrdType( fix.OrdType_STOP_LIMIT )
        else:
            pass
    
    def queryOrderQty(self):
        value = input("OrderQty: ")
        return fix.OrderQty( int(value) )
    
    def queryTimeInForce(self):
        print("1) Day\n2) IOC\n3) OPG\n4) GTC\n5) GTX")
        value = input("TimeInForce: ")

        if value == '1':
            return fix.TimeInForce( fix.TimeInForce_DAY )
        elif value == '2':
            return fix.TimeInForce( fix.TimeInForce_IMMEDIATE_OR_CANCEL )
        elif value == '3':
            return fix.TimeInForce( fix.TimeInForce_AT_THE_OPENING )
        elif value == '4':
            return fix.TimeInForce( fix.TimeInForce_GOOD_TILL_CANCEL )
        elif value == '5':
            return fix.TimeInForce( fix.TimeInForce_GOOD_TILL_CROSSING )
    
    def queryPrice(self):
        value = input("Price: ")
        return fix.Price( value )
    
    def queryStopPx(self):
        value = input("StopPx: ")
        return fix.StopPx( value )
    
    def queryHeader(self, header):
        header.setField( self.querySenderCompID() )
        header.setField( self.queryTargetCompID() )
    
    def querySenderCompID(self):
        return self.sessionID.getSenderCompID()

    def queryTargetCompID(self):
        return self.sessionID.getTargetCompID()
    
    def queryConfirm(self, label):
        value = input(label)

        if value == 'Y':
            return True

        return False

    def querySecurityExchange(self):
        securityExchanges = ['AGGREGATOR', 'ALGO', 'ASE', 'SX' ,
                'B3', 'BitMEX', 'BrokerTec', 'CBOT', 'CFE', 'CME', 
                'Coinbase', 'CoinFLEX', 'CurveGlobal', 'CZCE', 'DCE', 
                'DGCX', 'EEX', 'Eurex', 'Euronext', 'Fenics', 'FEX', 
                'HKEX', 'ICE', 'ICE_L', 'IDEM', 'INE', 'KCG', 'LME', 
                'LSE', 'MEFF', 'MOEX', 'MX', 'MX', 'NDAQ_EU', 'NFI', 
                'NFX', 'OSE', 'SGX', 'TFX', 'TOCOM']
        print('Possible values include: ')
        print(', '.join(securityExchanges))
        value = input('Option: ')
        while value not in securityExchanges:
            print('Invalid Value. Please try again')
            value = input('Option: ')
        
        return fix.SecurityExchange(value)

    def queryAccount(self):
        value = input('Account: ')
        return fix.Account(value)

