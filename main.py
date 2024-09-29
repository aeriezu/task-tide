from enum import IntEnum
import os
import google.generativeai as genai
#from flask import Flask
#app = Flask(__name__)

#@app.route('/')

os.environ["GOOGLE_API_KEY"] = "AIzaSyD_eKLpGgxx8iSn7EZjbeod_v9oFErSNNQ"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

class Gemini:
    def __init__(self, schedule):
        self.schedule = schedule

    def summary(self):
        # Format the schedule into a string prompt or any other meaningful format
        schedule_info = "\n".join(str(item) for item in self.schedule)

        # Call the API with the generated prompt
        response = model.generate_content(
            f"Here is the student's schedule: {schedule_info}. Tell them how many hours they should study based on how much time they spend in the class",
            generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                temperature=0.2,
            ),
        )
        
        # Return the API response
        return response.text

schedule = []

class Tools():
    def splitDays(daysInput):
        return [days.strip() for days in daysInput.split(', ')]
    
    def WeeklyReport(s: list):
        courses = {}
        for c in schedule:
            courses[c.name] = 0
        return s

courses = Tools.WeeklyReport(schedule)
print(courses)

class Days(IntEnum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

class Subjects():

    def __init__(self, name, days, startTime, endTime):
        self.name = name # name of subject
        self.days = days # day(s) of the week its on
        self.startTime = startTime # time the class is on
        self.endTime = endTime # time the class ends

    def __str__(self):
        days_str = " and ".join(self.days)
        return f"{self.name} on {days_str} at {self.startTime}-{self.endTime}"

    def addClass(name, days, startTime, endTime):
        newClass = Subjects(name, days, startTime, endTime)
        schedule.append(newClass)
    
    # def removeClass(name, day):

class Test():
    addNew = True

    while addNew == True:
        userInputName = input("What is the name of your class?\n>")
        userInputDays = input("What day(s) is your class in?\n>")
        userInputStartTime = input("What time does your class start?\n>")
        userInputEndTime = input("What time does your class end?\n>")

        days = Tools.splitDays(userInputDays)
        Subjects.addClass(userInputName, days, userInputStartTime, userInputEndTime)
        addNew = (input("Do you want to add another class? Y/N\n>") == "y")
        print(addNew)

    print("Your schedule:")
    for subject in schedule:
        print(subject)

if __name__ == "__main__":
    Test()

gemini_instance = Gemini(schedule)
summary = gemini_instance.summary()
print(summary)