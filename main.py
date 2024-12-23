import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

# OpenWeatherMap API 키 (본인의 유효한 API 키를 입력)
API_KEY = "c1ac6f67f00acd407aa4d44c0c6bd671"  # 본인의 API 키로 변경

# 사용자가 원하는 도시 입력
city = st.text_input("Enter the city name:", "Seoul")

# 날씨 데이터 가져오기 (실시간 날씨 정보)
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=kr"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == 200:
        return data
    else:
        return None

# 3일 날씨 예보 가져오기
def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=kr"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "200":
        forecast_data = []
        for forecast in data['list']:
            date = forecast['dt_txt']
            temp = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            forecast_data.append([date, temp, humidity])
        
        # pandas 데이터프레임으로 변환
        forecast_df = pd.DataFrame(forecast_data, columns=["Date", "Temperature", "Humidity"])
        forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
        return forecast_df
    else:
        return None

# 시각화 함수 (온도 및 습도 변화 그래프)
def plot_weather_forecast(forecast_df):
    # 날짜가 3일 이상이면 3일로 자르기
    forecast_df = forecast_df[forecast_df["Date"] < forecast_df["Date"].min() + timedelta(days=3)]
    
    # 새 figure 객체 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 첫 번째 서브플롯: 온도 그래프
    plt.subplot(2, 1, 1)
    plt.plot(forecast_df["Date"], forecast_df["Temperature"], label="Temperature (°C)", color='tab:red')
    plt.title('Temperature Forecast for Next 3 Days')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # 두 번째 서브플롯: 습도 그래프
    plt.subplot(2, 1, 2)
    plt.plot(forecast_df["Date"], forecast_df["Humidity"], label="Humidity (%)", color='tab:blue')
    plt.title('Humidity Forecast for Next 3 Days')
    plt.xlabel('Date')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # 레이아웃 조정
    plt.tight_layout()

    # Streamlit에서 그림 출력
    st.pyplot(fig)

# 날씨 데이터를 가져오고 시각화하는 함수
def show_weather(city):
    forecast_df = get_forecast(city)
    if forecast_df is not None:
        st.write(f"Weather forecast for {city} for the next 3 days:")
        plot_weather_forecast(forecast_df)
    else:
        st.write(f"Unable to get weather data for {city}.")

# 사용자가 입력한 도시의 날씨 예보 시각화
show_weather(city)
