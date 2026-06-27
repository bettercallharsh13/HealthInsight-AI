HealthInsight AI
Video Demo: https://youtu.be/bhtBsrYWU1Y
Description

For my CS50P final project, I created HealthInsight AI, a simple Python program that analyzes a user's basic health information. The idea behind this project was to build something practical while applying the Python concepts I learned throughout the course.

The program asks the user for their name, age, weight, height, average sleeping hours, and daily water intake. Using this information, it calculates the user's Body Mass Index (BMI), determines their BMI category, calculates a health score, provides health recommendations, and generates a short AI-style health summary. Every time the program is used, a report is also saved in a JSON file so previous results are not lost.

One of my goals was to organize the project using object-oriented programming instead of writing everything inside one function. I created a User class to store the user's information and a HealthAnalyzer class that contains all of the health-related calculations. Separating these responsibilities made the code cleaner and easier to understand.

The HealthAnalyzer class contains methods for calculating BMI, determining the BMI category, calculating a health score, generating recommendations, and creating an AI insight. Each method performs one specific task, which makes the project easier to maintain and extend in the future.

I also wanted the program to remember previous analyses, so I implemented a save_report() function. This function stores each health report in a file named history.json. If the file does not already exist, it is created automatically. This allowed me to practice working with JSON files as well as exception handling.

The health score starts at 100 and decreases based on simple health indicators. If the user's BMI is outside the normal range, some points are deducted. Additional points are deducted if the user sleeps less than seven hours or drinks less than two liters of water per day. Although this scoring system is intentionally simple, it demonstrates how multiple health factors can be combined into a single score.

The recommendation system provides personalized suggestions based on the user's input. For example, if the BMI is high, the program recommends increasing physical activity. If the BMI is low, it suggests increasing calorie intake. It also reminds users to sleep more or drink more water whenever necessary.

Finally, I added an AI-style insight that summarizes the user's BMI and health score in a natural sentence. While this is not powered by a machine learning model, I wanted the output to feel more conversational than simply displaying numbers.

Throughout this project, I used several Python concepts from CS50P, including classes, functions, conditional statements, exception handling, file handling, JSON, modules, and the datetime library. Working on this project helped me better understand how these concepts fit together in a real application.

If I continue developing this project, I would like to add features such as graphical health charts, PDF report generation, exercise tracking, nutrition analysis, and a web interface where users can access their health history more easily.

Overall, this project gave me the opportunity to combine programming with a real-world problem while practicing clean code organization and object-oriented design.
