# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 18:40:46 2022

@author: Maliha
"""

import Auto
import argparse
from selenium import webdriver

    

if __name__ == '__main__':
      
  
    parser=argparse.ArgumentParser()
      
    parser.add_argument("--name", nargs='+', help="please enter automobile marks seris" 
                        )
    args=vars(parser.parse_args())
    name=args["name"]
    name=[i.title() for i in name]
   
    def main2(name): 
    
        title_list=[]
        PATH="C:/Users/lenovo/Desktop/web/chromedriver"
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.sahibinden.com/kategori/otomobil")
        
        box_link2=driver.find_element_by_class_name("jspPane")
        li=box_link2.find_elements_by_tag_name("li")
        
        for i in li:
            aTag=i.find_element_by_tag_name("a")
            title = aTag.get_attribute("title")
            title_list.append(title)
        
            
        list1=[]
        for i in range(len(title_list)):
            if title_list[i] in name:
                list1.append(i+1)
       
        a=Auto.Automobile(list1)
        a.main()

    main2(name)
    