import csv
from random import shuffle
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

COUNTRIES_CSV = 'countries.csv'  # Country CSV filename

game_started = False  # Keeps track of whether or not user is currently in a game
questions_correct = 0  # Keeps track of number of questions answered correctly
number_questions = 10  # How many questions to ask
# Key = country No. , Value = [Flag URL, Country Name, Fun Fact]
countries_dict = dict()
question_order = []  # Contains ints which are country ids. Order to ask questions in
list_pos = 0  # Keeps track of how far down the question list we've gone

# On launch ask if user would like to start a new game


@ask.launch
def newGame():

    print "1"

    global game_started
    game_started = False
    welcome_msg = render_template('welcome')

    return question(welcome_msg)

# If user indicates they want to start a new game


@ask.intent("StartGame")
def initGame():

    print "2"

    global game_started
    global questions_correct
    global countries_dict
    global question_order
    global list_pos
    # Init new game as long as not already in game
    if not game_started:
        game_started = True
        questions_correct = 0
        # Read countries CSV and take them in as dictionary
        with open(COUNTRIES_CSV, 'rb') as csvfile:
            country_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for country in country_reader:
                countries_dict[int(country[0])] = [
                    country[1], country[2].split(","), country[3]]
        # Randomize countries order
        question_order = range(0, 20)
        shuffle(question_order)
        # Initialize list_pos
        list_pos = 0
        # Get the flag image of the first country in question_order and ask user with flag displayed on card
        what_country = render_template('which_country')
        return question(what_country).standard_card(title="Which Country?", small_image_url=countries_dict[question_order[list_pos]][0], large_image_url=countries_dict[question_order[list_pos]][0])
    else:
        return question("That's not a country, please name a country, or say I don't know")
# If user indicates they do not want to start a new game, exit


@ask.intent("DontStartGame")
def dontStartGame():

    print "3"

    return statement("Ok, see you next time")

# If user indicates they do not know while in game, count the question wrong, otherwise exit skill


@ask.intent("SayNo")
def sayNo():

    print "4"

    global game_started
    global list_pos
    global questions_correct
    global countries_dict
    global question_order
    global number_questions

    if not game_started:
        return statement("Ok, see you next time")
    else:
        list_pos += 1
        
    if list_pos >= number_questions:
        return statement("Sorry, that is not correct. The correct answer was %s. Out of %s questions you got %s correct. Thanks for playing" % (countries_dict[question_order[list_pos - 1]][1][0], str(number_questions), str(questions_correct))).simple_card(title="Final Score", content="%d correct out of %d" % (questions_correct, number_questions))
    else:
        return question("Sorry, that is not correct. The correct answer was %s. Now, can you guess what country this flag belongs to?" % (countries_dict[question_order[list_pos - 1]][1][0])).standard_card(title="Which Country?", small_image_url=countries_dict[question_order[list_pos]][0], large_image_url=countries_dict[question_order[list_pos]][0])

# If user provides answer, check to see if it is correct, then either end the game if number_questions have been asked
# Or provide the next question


@ask.intent("ProvideAnswer", convert={'country_name': str})
def checkAnswer(country_name):
    global list_pos
    global questions_correct
    global countries_dict
    global question_order
    global number_questions
    if game_started:
        if country_name is not None:
            country_name = country_name.lower()  # Sanitize input to lowercase
            correct_name = countries_dict[question_order[list_pos]][1]
            list_pos += 1
            # If the allotted number of questions have been asked
            if list_pos >= number_questions:
                if country_name in correct_name:
                    questions_correct += 1
                    return statement("Yes that is correct. Here is a fun fact about %s: %s. Out of %s questions you got %s correct. Thanks for playing" % (countries_dict[question_order[list_pos - 1]][1][0], countries_dict[question_order[list_pos - 1]][2], str(number_questions), str(questions_correct))).simple_card(title="Final Score", content="%d correct out of %d" % (questions_correct, number_questions))
                else:
                    return statement("Sorry, that is not correct. The correct answer was %s. Out of %s questions you got %s correct. Thanks for playing" % (countries_dict[question_order[list_pos - 1]][1][0], str(number_questions), str(questions_correct))).simple_card(title="Final Score", content="%d correct out of %d" % (questions_correct, number_questions))
            # Otherwise, get info about the next question to ask and ask it
            if country_name in correct_name:
                questions_correct += 1
                return question("Yes that is correct. Here is a fun fact about %s: %s. Now, can you guess what country this flag belongs to?" % (countries_dict[question_order[list_pos - 1]][1][0], countries_dict[question_order[list_pos - 1]][2])).standard_card(title="Which Country?", small_image_url=countries_dict[question_order[list_pos]][0], large_image_url=countries_dict[question_order[list_pos]][0])
            else:
                return question("Sorry, that is not correct. The correct answer was %s. Now, can you guess what country this flag belongs to?" % (countries_dict[question_order[list_pos - 1]][1][0])).standard_card(title="Which Country?", small_image_url=countries_dict[question_order[list_pos]][0], large_image_url=countries_dict[question_order[list_pos]][0])
        else:
            return question("Please provide a proper answer.")
@ask.intent('AMAZON.HelpIntent')

def help():
    global game_started
    if not game_started:
        return question("Indicate whether or not you'd like to start a new game by saying yes, or no. Once the game starts, look at the card displayed in the alexa app and try to guess which country the flag belongs to. If you don't know say I don't know.")
    else:
        return question("Look at the card displayed in the alexa app and try to guess which country the flag belongs to. If you don't know say I don't know.")


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Ok, see you next time")

@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Ok, see you next time")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Ok, see you next time")

if __name__ == '__main__':
    app.run(debug=True)
