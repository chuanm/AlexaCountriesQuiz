# AlexaCountriesQuiz
For the winter 2017-2018 student alexa skill dev challenge.

## Inspiration
When entering the challenge, I wanted some way to integrate Alexa's visual cards into whatever I was doing. I also wanted a game-style skill to keep kids entertained while providing some kind of educational value at the same time. What I came up with was the Country Flag Quiz.

## What it does
Each time a new game is launched, the Country Flag Quiz asks 10 questions. For each question, the picture of a country's flag is show on a skill card on alexa.amazon.com. The player then has to provide the name of the country related to the flag. If they guess correct, a fun fact about the country is read. If the answer is incorrect, the skill will inform the user of what the correct answer was.

## How I built it
I used the flask-ask library and python to build the Alexa skill. The data for all the country names, images, and fun facts are stored in a csv file.

## Challenges I ran into
Doing a trivia game which requires different phrase recognition depending on the stage of the game the user was at was challenging with amazon alexa. For example, after asking "would you like to start a new game?", saying "no" would have to trigger the skill to close. On the other hand, in a game after asking "can you guess what country this flag belongs to?", saying "no" would have to identify that the user did not know the correct answer. Also Alexa's lack of any kind of robust wildcard detection for slots meant that incorrect answers were sometimes being relegated to unexpected or incorrect intents.

Another issue I ran into were time constraints for implementing the full scope of the skill. Given that there are 195 countries recognized by the UN, and this was a one person project started around a week before the due date of the skill, this proved to be an impractically large amount of manual data entry for me given my schedule in the past week. I do plan to eventually have all 195(+) countries in the skill, but for now the skill will have to ship with closer to 30 or 40 countries.

## Accomplishments that I'm proud of/What I learned
This was definitely the largest alexa skill I've worked on in my own free time, and it was done entirely independently. I've learned a lot about the alexa skills kit, more specifically what it does well, and what it does not. Using the flask-ask library on this project also allowed me to become more acclimated with how flask and a RESTful API works. Working on this project also allowed me to brush up on my python skills which I haven't been able to put to use for a few years in any major capacity.

## What's next for Country Flag Quiz
-Entries for all 195(+) world countries
-Allow the user to specify how many questions they want to be asked
-Multiple fun facts for each country
-Built in help prompt/more clear instructions on how to play
-Clean up wording and formatting of cards
-Echo show version