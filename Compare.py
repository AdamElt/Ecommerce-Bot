
from itertools import product
import discord 
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup

PATH = "C:\Program Files (x86)\chromedriver"
driver = webdriver.Chrome(PATH)

client = discord.Client()
@client.event
async def on_ready():
    print('Bot is now online')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    product = message.content

    print("Product being searched ",product)

    # Amazon

    driver.get("https://www.amazon.com/")

    time.sleep(2)

    searchA = driver.find_element(By.ID,"twotabsearchtextbox")

    searchA.send_keys(product)

    searchA.send_keys(Keys.RETURN)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    resultA = soup.findAll('div', {'data-component-type': 's-search-result'})
    
    print("WE OUT HERE")
    print(resultA)

    itemA1 = resultA[0] # Item 1
    itemA2 = resultA[1] # Item 2
   
    atag = itemA1.h2.a
    atag2 = itemA2.h2.a

    atitle = atag.text.strip()      # Name of Product
    atitle2 = atag2.text.strip()

    print(atitle)
    print(atitle2)

    aprice_parent = itemA1.find('span','a-price')
    priceA1 = aprice_parent.find('span','a-offscreen').text

    aprice_parent = itemA2.find('span','a-price')
    priceA2 = aprice_parent.find('span','a-offscreen').text

    # Best Buy

    driver.get("https://www.bestbuy.com/")

    time.sleep(.5)
    
    searchB = driver.find_element(By.ID,"gh-search-input")

    searchB.send_keys(product)

    searchB.send_keys(Keys.RETURN)

    try:
        itemBTitle = driver.find_element(By.CSS_SELECTOR,(".sku-title"))    # Name of Product

        ritemBTitle = itemBTitle.text

        print(itemBTitle.text)

        print("Best Buy Price")

        itemBP = driver.find_element(By.CSS_SELECTOR,(".priceView-hero-price"))

        itemBPrice = (itemBP.text[0:7])

    except:
        print("Couldn't find product at Best Buy")                  #Product not at Best Buy

    # Target
	
    driver.get("https://www.target.com/")

    time.sleep(2)

    searchW = driver.find_element(By.CSS_SELECTOR,'#search')

    searchW.send_keys(product) 

    searchW.send_keys(Keys.RETURN)

    time.sleep(1)

    searchTPrice = driver.find_element(By.CSS_SELECTOR,".h-padding-r-tiny")

    itemTPrice = (searchTPrice.text)

    embed = discord.Embed(title = product, description = "Price Comparison: ", color=0xa92323)

    embed.set_author(name = message.author)

    embed.add_field(name = "Amazon", value = "{} : {}  {} : {}".format(atitle,priceA1,atitle2,priceA2), inline = False)

    embed.add_field(name = "Best Buy", value = "{} : {}".format(ritemBTitle,itemBPrice), inline = False)

    embed.add_field(name = "Target", value = "{} : {}".format(product,itemTPrice), inline = False)

    await message.author.send(embed = embed)

    # Add an image to the embeded message
    # embed.set_image  
    # Add Ebay
    # Add URLS
    # Trim Amazons titles in the embeded message

client.run('')
