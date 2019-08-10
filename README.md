# NHLGoals
An analysis of NHL Goals

As I was looking for data on time of goals in the NHL, I could only find it through individual game summaries. As such, I compiled all the game summaries for every game in the NHL 2018-2019 regular season. The CSV files are the data that I complied, divided by division.
There are a lot of questions that could be answered with this data:
•	When are the most goals scored in a game?
•	Which players had the most go-ahead goals?
•	What is the probability that a goal will be scored in the first period?
There are many questions that can be asked, and I hope you will take the chance to answer some of them. 
The structure of the Python files are as follows:
ScheduleFunction.py pulls in all the schedules for each team. You can change the “2019” to an earlier year if you’d like to collect more data.
The HockeyFunctions.py file is where the functions are applied and the dataset is created.
The JustRegularGoals.py file is for those goals where no special type of goal (such as a PP or EN) were scored.
The PPandRegularGoals.py file if for those goals where a special type of goal (such as a PP or EN) were scored. 
The GoalsVisualized.py file is where I've been doing some initial visualization work.
Please feel free to provide feedback or suggestions on how to make this better.

Thank you,
David
