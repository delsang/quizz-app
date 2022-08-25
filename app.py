# Decide what kind of data you want the application to manage. Examples include budget items, work request tickets, investment performance, book reviews, and more.
# Create the .csv file with specific columns and a first row or two as "seed" data for your application to test while developing.
# Create your index route and template that shows all items in the .csv file on the web page, including links to each individual item's details page.
# Complete the show route that displays the details of each item in the .csv
# Include a create route that allows users to add new data to the file. This should accept a POST request with the new data.

from flask import Flask, render_template, request, redirect, url_for # import what we need to use from the flask library
import csv
 
test = []

# Open the CSV file to retreive all informations as a dictionnary
with open('./QuizzQuestionsanswers.csv', mode='r') as file:

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

# Home Page
@app.route("/")
def home():
    return render_template('homepage.html')

# Page where the user can choose the category they want to answer
@app.route("/categories", methods=["GET"])
def categories():
    # Create a list with the unique categories on the database
    unique_categories = []
    for row in test:
        category = row["Category"] 
        if category not in unique_categories:
            unique_categories.append(category)
        else:
            pass    
        
    return render_template('categories.html', Categories=unique_categories)

# The user will be able to add new questions and answers to that page.
@app.route("/addquestion", methods=['GET'])
def newquestion():
    return render_template('newquestion.html')

@app.route('/addquestion',methods = ['POST'])
def newquestions():
    new_question = {}
    new_question["Question"] = request.form["qt"]
    new_question["RightAnswer"] = request.form["ra"]
    new_question["Answer2"] = request.form["wr1"]
    new_question["Answer3"] = request.form["wr2"]
    new_question["Answer4"] = request.form["wr3"]
    new_question["Category"] = request.form["cat"]
    new_question["ID"] = str(len(test)+1)
    test.append(new_question)
    
    with open('./QuizzQuestionsanswers.csv', mode='a') as f:
        new_row = "\n" + new_question["Question"] + "," + new_question["RightAnswer"] + "," + new_question["Answer2"] + "," + new_question["Answer3"] + "," + new_question["Answer4"] + "," + new_question["Category"] + "," + new_question["ID"]
        f.write(new_row)
    return redirect(url_for('home'))


# Will display the page rendering the choosen categories questions
@app.route("/letsanswer/<category>", methods=["GET"])
def show_question(category):
    category_questions = []
    for row in test:
        if row["Category"] == category:
            category_questions.append(row)    
    return render_template("letsanswers.html", questions=category_questions, Category=category), category_questions



# Will handle the answers done and calculate the score
@app.route("/letsanswer/<category>", methods=["POST"])
def calculate_score(category_questions):
    score = 0
    if request.form.get('1') == 'yo':
        score += 1
    if request.form.get('2') == 'yo':
        score += 1
    if request.form.get('3') == 'yo':
        score += 1
    if request.form.get('4') == 'yo':
        score += 1
    else:
        pass

    return redirect(url_for('score')), score

@app.route("/results")
def score():
    return render_template('result.html', score=score)



if __name__ == '__main__':
    app.run(debug=True) # Start the server listening for requests