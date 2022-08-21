# Decide what kind of data you want the application to manage. Examples include budget items, work request tickets, investment performance, book reviews, and more.
# Create the .csv file with specific columns and a first row or two as "seed" data for your application to test while developing.
# Create your index route and template that shows all items in the .csv file on the web page, including links to each individual item's details page.
# Complete the show route that displays the details of each item in the .csv
# Include a create route that allows users to add new data to the file. This should accept a POST request with the new data.

from flask import Flask, render_template, request # import what we need to use from the flask library
import csv
 
test = []

# Open the CSV file to retreive all informations as a dictionnary
with open('./standardised test.csv', mode='r') as file:

    #open the file
    reader = csv.reader(file)

    # Create a dictonnary, starting at the second line
    next(reader)
    for row in reader:
        question = row[0]
        right = row[1]
        answ2 = row[2]
        answ3 = row[3]
        answ = row[4]
        category = row[5]
        question_id = row[6]
        test.append({'Question':question, "RightAnswer":right, "Answer2":answ2, "Answer3":answ3, "Answer4":answ, "Category":category, "ID":question_id})



# Now to the website..
# invoke the Flask clas
app = Flask(__name__) 


@app.route("/")
def index():
    return render_template('index.html', csv_file=test)


# Will display the route depending on the question ID
@app.route("/letsanswer/<question_id>", methods=["GET"])
def show_question(question_id):
    for row in test:
        if int(row["ID"]) == int(question_id):
            question = row
            return render_template("letsanswers.html", question=question)





if __name__ == '__main__':
    app.run(debug=True) # Start the server listening for requests