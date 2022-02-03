# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 18:42:15 2022

@author: Maliha
"""

import pandas as pd
import json
from selenium import webdriver
import time
import logging
from selenium.webdriver.chrome.options import  Options
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
options = Options()
import pymongo
from pymongo import MongoClient
import config

class Automobile:
    
    logging.basicConfig(
    filename="logfile.txt",
    format="%(asctime)s - %(levelname)s - %(message)s ",
    filemode="w",level=logging.DEBUG)
    
    def __init__(self, marks):
        
        self.marks=marks
        self.model_list=[]
        self.value_list=[]
        self.price_list=[]
        self.date_list=[]
        self.province_list=[]
        self.title_list=[]
        self.marks_list=[] 
        
      
    def main(self): 
        PATH="C:/Users/lenovo/Desktop/web/chromedriver"
        self.driver = webdriver.Chrome(PATH)
        # self.driver.get("https://www.sahibinden.com/kategori/otomobil")
        for self.j in self.marks:
              self.driver.maximize_window()
              self.driver.get("https://www.sahibinden.com/"+str(self.j))
              self.main_process()
        self.send_mangodb() 
        self.driver.close()
    def main_process(self):
        
        while True:
                try:
                    model =  self.driver.find_elements_by_css_selector(".searchResultsTagAttributeValue")
                    value =  self.driver.find_elements_by_css_selector(".searchResultsAttributeValue")
                    price =  self.driver.find_elements_by_css_selector(".searchResultsPriceValue")
                    date =   self.driver.find_elements_by_css_selector(".searchResultsDateValue")
                    province = self.driver.find_elements_by_css_selector(".searchResultsLocationValue")
                    
                    for i in model:
                        self.model_list.append(i.text)
                    for i in value:
                        self.value_list.append(i.text)
                    for i in price:
                        self.price_list.append(i.text)
                    for i in date:
                        self.date_list.append(i.text)
                    for i in province:
                        self.province_list.append(i.text)

                    self.driver.execute_script("window.scrollTo(0,2500)")
                    time.sleep(2)
                    self.driver.find_element_by_link_text("Sonraki").click()
                    time.sleep(2)
                except (NoSuchElementException,StaleElementReferenceException):
                     break
        self.data_process()     

    def data_process(self):
        
        try: 
            seri=[]
            model=[]
          
            for i in range(0,len(self.model_list),2):
                seri.append(self.model_list[i])
                model.append(self.model_list[i+1])
                
            km=[]        
            year=[]
            color=[]  
            
            for i in range(0,len(self.value_list),3):
                year.append(self.value_list[i])
                km.append(self.value_list[i+1])
                color.append(self.value_list[i+2])  
                
                
            date=[]    
            
            for sub in self.date_list:
                date.append(sub.replace("\n"," ")) 
                
            province=[]  
            
            for sub in self.province_list:
                province.append(sub.replace("\n"," ")) 
                
          
            df2=pd.DataFrame(seri,columns=['seri'])
            
            df3=pd.DataFrame(model,columns=['model'])
            
            df4=pd.DataFrame(year,columns=['yil'])
            
            df5=pd.DataFrame(km,columns=['km'])
            
            df6=pd.DataFrame(color,columns=['renk']) 
            
            df7=pd.DataFrame(self.price_list,columns=['fiyat'])
            
            df8=pd.DataFrame(date,columns=['tarih'])
            
            df9=pd.DataFrame(province,columns=['il-ilce'])
        
            for i in range(len(df9)-len(self.marks_list)):
                 self.marks_list.append(self.j)    
              
            df1=pd.DataFrame(self.marks_list,columns=['marks'])  
            
            data=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9], axis=1)
     
            final=data.to_json(r'Data.json',orient='records',force_ascii=False)
            data.to_csv('Data.csv')
            
        except(IndexError, NoSuchElementException, StaleElementReferenceException):
            print("series not exist")
            self.model_list=[]
            self.value_list=[]
            self.price_list=[]
            self.date_list=[]
            self.province_list=[]
            self.marks_list=[]
            
    def send_mangodb(self):
        try:
          
            cluster = pymongo.MongoClient(config.mongo)
            
            db=cluster['Database']
            collection=db['data']
            print('connected')
            with open('Data.json') as f:
                data=json.load(f)
            if isinstance(data, list):
                collection.insert_many(data)  
            else:
                collection.insert_one(data)
        except :
            print('not coneccted')  
        
   
