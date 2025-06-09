import requests
from tkinter import *
from PIL import Image, ImageTk
from condition import conditionpicture, nightCondition

# create root window
root = Tk()

# Create Frames
home_frame = Frame(root)
data_frame = Frame(root)

# Title
root.title('Weather App')

# Establish Size
root.geometry('400x200')
root.resizable(False, False)

#### Frame 1
# Load the image
bg_image = Image.open("APIs/background_images/ClearSkyFinal.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label with the image
bg_label = Label(home_frame, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)


# Create a label with some text and postion in center
intro = Label(home_frame, text="Enter Location", font=("Helvetica", 18, "bold"), fg="black")
intro.place(relx=0.5, rely=0.4, anchor='center')

# Add input box for location
locationInput = Entry(home_frame, font=("Helvetica", 18), fg="black")
locationInput.place(relx=0.5, rely=0.6, anchor='center')

# Location Entered
def enterKey(optionalLocation):
    # Hide home_frame
    home_frame.pack_forget()
    data_frame.pack(fill='both', expand=True)

    # Get weather data
    currentLocation = locationInput.get()
    url = "http://api.weatherapi.com/v1/current.json?key=KEY&q=" + currentLocation

    try:
        response = requests.get(url)

        data = response.json()
        location = data['location']['name']
        locationState = data['location']['region']
        temperature = data['current']['temp_f']
        condition = data['current']['condition']['text']
        feelsLike = data['current']['feelslike_f']
        windMag = data['current']['wind_mph']
        windDir = data['current']['wind_dir']
        conditionCode = data['current']['condition']['code']
        isDay = data['current']['is_day']
        lastUpdate = data['location']['localtime']

        ## Frame 2
        ## Get background
        updateBackground(isDay, conditionCode)

        ## Place Weather Data
        displayData(location, locationState, temperature, feelsLike, windMag, windDir, condition)

        ## Last Updated Time
        newTime = updateTime(lastUpdate)

        lastUpateTime = Label(data_frame, text="Last Updated: " + newTime[1], font=("Helvetica", 9), fg="black")
        lastUpateTime.place(relx=0.15, rely=0.95, anchor='center')
    
        refreshButton = Button(data_frame, text='Refresh', command=lambda:refreshButtonFunc(currentLocation))
        refreshButton.place(relx=0.9, rely=0.9, anchor='center')

    except requests.exceptions.RequestException as e:
        errorScreen = Label(data_frame, text=location + " Not Found" + locationState, font=("Helvetica", 34, "bold"), fg="black")
        errorScreen.place(relx=0.5, rely=0.5, anchor='center')
        print("An error occurred:", e)
    return

def escapeKey(event):
    locationInput.delete(0, END)
    data_frame.pack_forget()
    home_frame.pack(fill='both', expand=True)

    for widget in data_frame.winfo_children():
        widget.destroy()
    return

def updateTime(lastUpdateTime):
    tempTimeArr = lastUpdateTime.split()
    if (int(tempTimeArr[1][:2])) > 12:
        tempNum = int(tempTimeArr[1][:2]) - 12
        if tempNum < 10:
            newNum = '0' + str(tempNum)
        else:
            newNum = str(tempNum)
        tempTimeArr[1] = newNum + tempTimeArr[1][2:]

    return tempTimeArr

def updateBackground(is_day, condition_code):
    if is_day == 1:
        conditionBg = Image.open(conditionpicture(str(condition_code)))
    else:
        conditionBg = Image.open(nightCondition(str(condition_code)))
    
    conditionBgImage = ImageTk.PhotoImage(conditionBg)
    data_frame.bg_image = conditionBgImage
    conditionLabel = Label(data_frame, image=conditionBgImage)
    conditionLabel.place(relwidth=1, relheight=1)

    return

def displayData(location, locationState, temperature, feelsLike, windMag, windDir, condition):
    userLocation = Label(data_frame, text=location + ", " + locationState, font=("Helvetica", 25, "bold"), fg="black")
    userLocation.place(relx=0.5, rely=0.18, anchor='center')

    locationTemp = Label(data_frame, text=str(temperature) + "°F", font=("Helvetica", 27), fg="black")
    locationTemp.place(relx=0.5, rely=0.5, anchor='center')

    feelsLikeTitle = Label(data_frame, text="Feels like", font=("Helvetica", 10), fg="black")
    feelsLikeTitle.place(relx=0.8, rely=0.45, anchor='center')
    feelsLikeTemp = Label(data_frame, text=str(feelsLike) + "°F", font=("Helvetica", 14), fg="black")
    feelsLikeTemp.place(relx=0.8, rely=0.55, anchor='center')

    windTitle = Label(data_frame, text="Wind (mph)", font=("Helvetica", 10), fg="black")
    windTitle.place(relx=0.2, rely=0.45, anchor='center')
    locationWind = Label(data_frame, text=str(windMag) + " " + windDir, font=("Helvetica", 14), fg="black")
    locationWind.place(relx=0.2, rely=0.55, anchor='center')

    locationCondition = Label(data_frame, text=str(condition), font=("Helvetica", 12), fg="black")
    locationCondition.place(relx=0.5, rely=0.75, anchor='center')
    
    return

def refreshButtonFunc(previousLocation):
    for widget in data_frame.winfo_children():
        widget.destroy()

    url = "http://api.weatherapi.com/v1/current.json?key=KEY&q=" + previousLocation

    try:
        response = requests.get(url)

        data = response.json()
        location = data['location']['name']
        locationState = data['location']['region']
        temperature = data['current']['temp_f']
        condition = data['current']['condition']['text']
        feelsLike = data['current']['feelslike_f']
        windMag = data['current']['wind_mph']
        windDir = data['current']['wind_dir']
        conditionCode = data['current']['condition']['code']
        isDay = data['current']['is_day']
        lastUpdate = data['location']['localtime']

        ## Frame 2
        ## Get background
        updateBackground(isDay, conditionCode)

        ## Place Weather Data
        displayData(location, locationState, temperature, feelsLike, windMag, windDir, condition)

        ## Last Updated Time
        newTime = updateTime(lastUpdate)

        lastUpateTime = Label(data_frame, text="Last Updated: " + newTime[1], font=("Helvetica", 9), fg="black")
        lastUpateTime.place(relx=0.15, rely=0.95, anchor='center')
    
        refreshButton = Button(data_frame, text='Refresh', command=lambda:refreshButtonFunc(previousLocation))
        refreshButton.place(relx=0.9, rely=0.9, anchor='center')

    except requests.exceptions.RequestException as e:
        errorScreen = Label(data_frame, text=location + " Not Found" + locationState, font=("Helvetica", 34, "bold"), fg="black")
        errorScreen.place(relx=0.5, rely=0.5, anchor='center')
        print("An error occurred:", e)
    return

home_frame.pack(fill='both', expand=True)

root.bind("<Return>", enterKey)
root.bind("<Escape>", escapeKey)

# Tkinter event loop
root.mainloop()
