import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Replace this with your real OpenWeatherMap API key
API_KEY = "546ed5e8c5b84924527f86e278a9d762"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            result_label.config(text="City not found. Try again.", fg="red")
            weather_icon_label.config(image="")
            return

        # Extract info
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        icon_code = data["weather"][0]["icon"]

        # Update text
        result = (
            f"City: {city.title()}\n"
            f"Temperature: {temp} °C\n"
            f"Condition: {weather}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )
        result_label.config(text=result, fg="black")

        # Show icon
        icon_code = data["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = Image.open(BytesIO(icon_response.content))
        icon_image = ImageTk.PhotoImage(icon_data)
        weather_icon_label.image = icon_image # prevents garbage collection
        weather_icon_label.config(image=icon_image) #type: ignore

    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Request failed: {e}", fg="red")
        weather_icon_label.config(image="")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x450")
root.configure(bg="#f0f0f0")

# Fonts
label_font = ("Arial", 14)
entry_font = ("Arial", 12)

# Widgets
tk.Label(root, text="Enter City Name", font=label_font, bg="#f0f0f0").grid(pady=10)

city_entry = tk.Entry(root, font=entry_font, justify="center")
city_entry.grid(pady=5, ipadx=20, ipady=5)

tk.Button(root, text="Get Weather", font=label_font, command=get_weather, bg="#4CAF50", fg="white").grid(pady=10)

weather_icon_label = tk.Label(root)
weather_icon_label.grid(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left", bg="#f0f0f0")
result_label.grid(pady=10)

# Run
root.mainloop()