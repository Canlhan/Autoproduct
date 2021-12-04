import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager




print("enter the category")
filename=input()

print("password")
sifre=input()
filename.lower().strip()
browser = webdriver.Chrome(ChromeDriverManager().install())
url = "https://bayi.nettechstore.com/index.php?route=account/login"
browser.get(url)

eposta = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div/div[2]/div/form/div[1]/input")
password = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div/div[2]/div/form/div[2]/input")
eposta.send_keys("example_user_email")

password.send_keys(sifre)

oturum = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div/div[2]/div/form/div[3]/div/button")
oturum.click()

browser.get("https://bayi.nettechstore.com/index.php?route=checkout/cart")


urun = len(browser.find_elements_by_xpath("//*[@id='content']/div/form/div/table/tbody/tr"))

#****************************************** EXCEL DOSYAALRI YARATILIYOR*********************************





workbook =xlsxwriter.Workbook(f"{filename}.xlsx")
worksheet = workbook.add_worksheet()



#*************************************************bilgileri aktarma*************************************
#file=exists(f"{filename}.xlsx")
#print(file)



for ur in range(urun):

    #print(urun)
    ur+=1
    content = browser.find_element_by_xpath(f"//*[@id='content']/div/form/div/table/tbody/tr[{ur}]/td[2]").find_element_by_css_selector("a")
    #time.sleep(5)

    browser.execute_script("arguments[0].click();",content)
    #WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a")))

    #content.click()

    productname=browser.find_element_by_xpath("//*[@id='product']/div[1]")
    worksheet.write(ur,0, productname.text)
    productPrice = str(browser.find_element_by_xpath("//*[@id='product']/div[3]/div[1]/div/div").text[1:]).replace(',','.')


    currentdolars=str(browser.find_element_by_xpath("//*[@id='main-menu-2']/ul/li/a/span").text[14:]).replace(',','.')

    productRealPrice = float(productPrice) * float(currentdolars)
    productRealPrice=round(productRealPrice,2)
    print(productRealPrice)
    #print("sd")
    featuresofProduct=browser.find_element_by_class_name("block-content").find_element_by_css_selector("table").find_elements_by_css_selector("td")
    print("ÜRÜN İSMİ: "+productname.text)

    worksheet.write(0,0,"ÜRÜN İSMİ")
    worksheet.write(0,1,"ÜRÜN AÇIKLAMA")


    worksheet.write(0,2,"ÜRÜN FİYAT")
    #worksheet.set_column(ur,1,)
    worksheet.set_column(ur,100,50)

    print("----------------------------ÜRÜN ÖZELLİKLERİ----------------------------")
    featureToUnit=""
    for feature in featuresofProduct:
        featureToUnit +="   "+feature.text


    #****************************************************************** fotolar*******************************************************
    tent = browser.find_element_by_xpath("//*[@id='content']/div[1]/div[1]")

    imagesClass=tent.find_elements_by_css_selector("img")







    imagess=""
    i=0
    for imageLink in imagesClass:
      imagess+= imageLink.get_attribute("src")

    worksheet.write(ur, 3, imagess)
    print(imagess)
    #print(imagess)


    #*********************************************************************************************************************************
    print(featureToUnit)
    worksheet.write(ur,1,featureToUnit)
    worksheet.write(ur,2,productRealPrice)
    print(" *************************yeni ürün ******************************************")



    #print(featuresofProduct)









    ur -= 1
    browser.back()


workbook.close()





