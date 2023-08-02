# CollegeBot
This project is done as part of the course Spoken Dialogue Systems. It represents a CollegeBot that helps prospective U.S. bachelor's students to guide their university choice.
This [poster](https://github.com/jule-go/college_adviser/blob/master/Poster_collegebot.pdf) provides an overview over the project and our findings.
The initial proposal and timeplan of this project can be found [here](https://github.com/jule-go/college_adviser/blob/master/proposal_timeplan.md). In the course of the project some refinements have been taken though.

Group members:
* [Jule Godbersen](mailto:st168018@stud.uni-stuttgart.de)
* [Georgi Panayotov](mailto:st185424@stud.uni-stuttgart.de)
* [Urs Zaberer](mailto:st168124@stud.uni-stuttgart.de)

In case of questions: Don't hesitate to email us!

## Installation and Using the CollegeBot
You need to install python and create a virtual environment (e.g. with help of conda). Clone this repository and install the requirements in the [``requirements_CollegeAdviser.txt``-file](https://github.com/jule-go/college_adviser/blob/master/requirements_CollegeAdviser.txt)

To be able to run the CollegeBot you need to have access to GPUs. You can specify the cuda device in the [``collegebot_server.py``-file](https://github.com/jule-go/college_adviser/blob/master/soloist/examples/college_bot/collegebot_server.py).

The checkpoint of the trained soloist model is not included in this repository. This should not be a problem if you run the CollegeBot from the IMS servers. If this is not the case for you, please contact us.

After activating the environment, make sure to be in the ``college_adviser`` directory. To use the CollegeBot run ``python test_full_system.py``. You can communicate with the bot by using the console. After typing "Goodbye" or similar, the dialogue ends.

## Example Dialogues


<pre>
CollegeBot:  Hello, I'm CollegeBot. How can I help you?
User:        Hi! I'm looking for a college in North Carolina.
CollegeBot:  duke university is in north carolina.
             ...
</pre>

<pre>
CollegeBot:  Hello, I'm CollegeBot. How can I help you?
User:        I want to study in Stuttgart
CollegeBot:  i couldn't find any colleges matching your query. would you like to try again?
             ... 
</pre>                                                                         

## Some information on this repository
* [``adviser``](https://github.com/jule-go/college_adviser/tree/master/adviser): Contains the files related to the [Adviser framework](https://digitalphonetics.github.io/adviser/).
  * As Services we use the [ConsoleInput](https://github.com/jule-go/college_adviser/blob/master/adviser/services/hci/console.py), [CollegeAdviser](https://github.com/jule-go/college_adviser/blob/master/adviser/services/soloist_interaction/college_system.py) and [ConsoleOutput](https://github.com/jule-go/college_adviser/blob/master/adviser/services/hci/console.py)
* [``data``](https://github.com/jule-go/college_adviser/tree/master/data): This project is based on data from the [U.S. College Scorecard](https://collegescorecard.ed.gov/data/documentation/).
  * Apart from manually creating dialogues we also did a [simple automatic approach](https://github.com/jule-go/college_adviser/blob/master/data/example_dialogues/create_dialogues.ipynb)
* [``evaluation``](https://github.com/jule-go/college_adviser/tree/master/evaluation):
  * Includes the dialogues used for evaluations
  * The evaluation of the belief state prediction is done on automatically generated test dialogues. The evaluation of the system output is done manually by annotating adequancy and fluency of the generated sentences
* [``soloist``](https://github.com/jule-go/college_adviser/tree/master/soloist): Contains the files related to the [SOLOIST model](https://github.com/pengbaolin/soloist).
  * The adaptation of soloist for the domain of colleges happened in the [``college_bot``-file](https://github.com/jule-go/college_adviser/tree/master/soloist/examples/college_bot)
  * [``combined_lowercase.json``-file](https://github.com/jule-go/college_adviser/blob/master/soloist/examples/college_bot/combined_lowercase.json) represents the set of manual dialogues that were used for training the soloist model

