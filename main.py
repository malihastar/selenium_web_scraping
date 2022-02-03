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
      
    parser.add_argument("--name", nargs='+', help="please enter automobile marks name" 
                        )
    args=vars(parser.parse_args())
    name=args["name"]

    a=Auto.Automobile(name)
    a.main()
