# Forecasting Financial Data Using LSTM and Sentiment Analysis

This project explores enhancing stock price forecasting by incorporating market sentiment into deep learning models. The idea was inspired in part by the GameStop pump, which highlighted how collective investor sentiment—particularly from social media—can significantly impact stock prices.

In our analysis, we focused on Nvidia (NVDA) and developed a model that combines **3-day lag features** of historical closing prices with **sentiment scores** derived from Stocktwits messages. The time frame analyzed spans from 2014 to 2021.

- **Sentiment Data:** Sourced from [this Kaggle dataset](https://www.kaggle.com/datasets/frankcaoyun/stocktwits-2020-2022-raw), containing raw Stocktwits posts.
- **Price Data:** Collected using the `yfinance` API, which provided daily historical closing prices for Nvidia.

We then trained a **Long Short-Term Memory (LSTM)** neural network to evaluate whether the inclusion of sentiment data improves the accuracy of stock price predictions compared to using price data alone.

## How to Run

To run our code, the dataset are already included within the repository so everything should run smoothly. Given that you wanted to recreate our project using a different stock. You can change the ticker symbol in our ClosingPriceModel notebook. To run our combined model notebook with a new stock you would need to find sentiment data on the given stock then re-adjust our NvidiaSentiment notebook that creates sentiment quickly by levearge batched inference.