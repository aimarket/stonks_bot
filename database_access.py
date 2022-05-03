from firebase import firebase
from PIL import Image, ImageDraw, ImageFont

import yfinance as yf
import json

class Student:
  def __init__(self, ID, name):
    self.firebase = firebase.FirebaseApplication('https://Linktorealtime_database.com', None)
    self.ID = str(ID)
    self.name = name
    if(self.getFile() == None):
      self.balance = 20000
      self.portfolio = {}
      self.putFile()
    else:
      file = self.getFile()
      self.balance = file['balance']
      self.portfolio = json.loads(file['portfolio'].replace("\'", "\""))

  def putFile(self):
    data = {'name':self.name,
            'balance':self.balance,
            'portfolio':str(self.portfolio)}
    self.firebase.put('Student',self.ID,data)
  
  def getFile(self):
    return self.firebase.get("Student/"+self.ID,'')
    
  def getBalance(self):
    return self.balance
  
  def getPort(self):
    return self.portfolio
  
  def buy(self, stock):
    self.balance = self.balance - stock.getTotal()
    if stock.getTicker() in self.portfolio:
      self.portfolio[stock.getTicker()] = self.portfolio[stock.getTicker()] + stock.getShares()
    else:
      self.portfolio[stock.getTicker()] = stock.getShares()
    self.putFile()
  
  def sell(self, stock):
    self.balance = self.balance + stock.getTotal()
    self.portfolio[stock.getTicker()] = self.portfolio[stock.getTicker()] - stock.getShares()
    if self.portfolio[stock.getTicker()] == 0: #added a way to remove the key in the dictionary if 0 is owned
      self.portfolio.pop(stock.getTicker())
    self.putFile()
  
  def sellAll(self):
    portList = []
    for x in self.portfolio:
      stock = wallStreet(x, self.portfolio[x])
      self.balance = self.balance + stock.getTotal()
      portList.append(x)
    for x in portList:
      self.portfolio.pop(x)
    self.putFile()

  def totalInvestments(self):
    total = 0.0
    for stock in self.portfolio:
      x = wallStreet(stock, self.portfolio[stock])
      total += x.getTotal()
    return total

  def getImage(self):
    W, H= (300,500)
    # create an image
    out = Image.new("RGB", (W,H), (40,40,40))

    # get a font
    fnt = ImageFont.truetype("stock_font.ttf", 20)

    # get a drawing measurements
    d = ImageDraw.Draw(out)
    msg_title = self.name +" Portfolio"
    msg = "Ticker : Shares"
    w, h = d.textsize(msg, font=fnt)
    w_title, h_title = d.textsize(msg_title, font=fnt)
    
    #TODO concatenate the strings of stocks and shares
    concateString = ""
    for stock in self.portfolio:
      concateString = concateString +"\n{:5} : {:5}".format(stock,str(self.portfolio[stock]))

    # draw multiline text
    d.text(((W-w_title)/2,10), self.name+" Portfolio\nBuy Power : ${0}".format(format(self.balance, ".2f")),font=fnt, fill=(200,200,200))
    d.multiline_text(((W-w)/2,60), "Ticker : Shares"+concateString,font = fnt, fill=(0, 255, 0))
    d.text((50,470),"Total ${0}".format(format(self.balance+self.totalInvestments(), ".2f")),font=fnt, fill=(200,200,200))

    out.save("portfolios/"+self.ID+".png")
    return("portfolios/"+self.ID+".png")


class wallStreet:
  def __init__(self, ticker, shares):
    self.ticker = ticker
    self.shares = shares
    self.tickerPrice = self.Price(ticker)
    self.verify
    self.info
  def getTotal(self):
    return self.tickerPrice * self.shares
  def Price(self, ticker):
    try:    
      print("Entering api")
      stock = yf.Ticker(ticker)
      self.verify = True
      self.info = stock.info
      print("API successful exit")
      return float(stock.info['currentPrice'])
    except TypeError:
      self.verify = False
    except KeyError:
      self.verify = False
  def getInfo(self):
    return self.info
  def getVerify(self):
    return self.verify
  def getTicker(self):
    return self.ticker
  def getShares(self):
    return self.shares
  def getPrice(self):
    return self.tickerPrice

class coin:
  def __init__(self, ticker, shares):
    self.ticker = ticker
    self.shares = shares
    self.tickerPrice = self.Price(ticker)
    self.verify
    self.info
  def getTotal(self):
    return self.tickerPrice * self.shares
  def Price(self, ticker):
    try:    
      print("Entering api")
      stock = yf.Ticker(ticker)
      self.verify = True
      self.info = stock.info
      print("API successful exit")
      return float(stock.info['regularMarketPrice'])
    except TypeError:
      self.verify = False
    except KeyError:
      self.verify = False
  def getInfo(self):
    return self.info
  def getVerify(self):
    return self.verify
  def getTicker(self):
    return self.ticker
  def getShares(self):
    return self.shares
  def getPrice(self):
    return self.tickerPrice

