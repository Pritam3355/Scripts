# This repository contains various scripts for Backtesting strategies , Technical analysis, Stock screening,Fundamental Analysis,Web scrapping


1. Commodity Price - Historical Gold price from Indian Commodity market (without using any api)
   website link - https://in.investing.com/commodities/
   This script can be customized to suit the needs of user (like customizing frequency interval,commodity type etc ).
   
   Link to Dataset - https://www.kaggle.com/datasets/tsr564/goldpriceindianmarket

2. Backtesting 
      
      1. Backtesting 0 - Basic use cases of of availabe library to fetch ,preprocess data from NSE
      2. Backtesting 1 - Mean Reversal Strategy
      
3. Technical Analysis - Various functions from Ta-Lib library along with custom function integration 

4. Managemen-Discussion-Analysis-Annual-Report-Nifty - Scrapped last 5 years Annual Report link from (Managemen-Discussion-Analysis-Annual-Report-Nifty) . Downloaded the files(from https://www.screener.in/) & Extracted Management Discussion & Analysis section for nifty-smappcap-250 ( https://www.nseindia.com/products-services/indices-niftysmallcap250-index). This script extract data for 10 companies but it can be extended to all companies under any index just comment out the part that select last 10 companies in alphabetic order (inside script)
