# DD2480 - LAB 2, Continuous Integration

## A small continuous integration CI server
This server was made to solve lab 2 Continuous Integration in the course DD2480 at KTH. It's a small CI server that only includes some core features of continuous integration.

## Prerequisite
* Python 3.10
(The program is only tested on Python 3.10. We can not guarantee it will work for other versions of Python) 

## How to run the server
* Run `git clone git@github.com:jenniferclarsson/dd2480-lab-2.git` to clone the repository
* Run `cd dd2480-lab-2`
* Run `pip3 install -r requirements.txt` to install required dependencies.
To run the server you need to authenticate a Git user with push access to the repository in which you add the webhook. To do this, set up an .env file in project root with the following:
```
GIT_USER = '**GIT USERNAME THAT HAS PUSH ACCESS TO THE REPO IN WHICH YOU ADD THE WEBHOOK**'
GIT_TOKEN = '**GIT PERSONAL ACCESS TOKEN TO GIT_USER**'
**AND ALL OTHER VARIABLES NEEDED TO RUN THE PROJECT AND TESTS ON WHICH YOU USE THE SERVER**
```
### Note
If you want to test the CI server on it's own source code, you will need to add all the env variables which are required for the tests. See: How to run the tests.

* Run `python3 src/server.py` to run the server and make it visable on the internet. This command will output a public URL `xyz.ngrok.io`.
* Add a webhook on github using this payload URL `xyz.ngrok.io/github`. Content type should be `application/json`, the rest of the settings should be default.

### Note
The server assumes that 
* The project is a python project
* There is a `src` folder in the root directory 
* All test files are located in `src`
* All test files follows the name convention `*tests.py`

## How to run the tests
* Run `git clone git@github.com:jenniferclarsson/dd2480-lab-2.git` to clone the repository
* Run `cd dd2480-lab-2`
* Run `pip3 install -r requirements.txt` to install required dependencies.
To run the unit tests you need to authenticate a Git user with push access to a repository in order to set commit status.  To do this, set up an .env file in project root with the following:
```
GIT_USER = '**GIT USERNAME THAT HAS PUSH ACCESS TO GIT_REPO**'
GIT_TOKEN = '**GIT PERSONAL ACCESS TOKEN TO GIT_USER**'
GIT_REPO_OWNER = '**OWNER OF REPO WHERE COMMIT STATUS WILL BE SET**'
GIT_REPO = '**NAME OF REPO WHERE COMMIT STATUS WILL BE SET**'
GIT_SHA = '**SHA OF COMMIT TO SET STATUS ON**'
GIT_BROKEN_SHA = '**SHA OF A NON EXISTING COMMIT**'
```
* Run `python3 src/unit_tests.py` to run all unit tests. If all tests succeed, the program will output `OK`.

## Team (Essence)
The states of the team are: Seeded, formed, collaborating, performing, adjourned.
The seeded state was quickly passed in the first meeting. In the meetings to come, the state formed was also passed. Short before the deadline of assignment 1, the group had moved into the collaborating state, where the team is working is one cohesive unit and trust each other. As of now, the team is on it's way into the performing state, where they work efficiently and effectively. However, not enough time has been given to the team to fully adapt to changing contexts, and it’s hard to assess how a team is performing in just two/three weeks. As new groups will be formed for the next assignments, the team now moves into the adjourned state.

## List of contributions

- August Tengland: Dummy repos to test against. Build history for P+. Implementation of build log. Automatic wrapping around Ngrok. Implementing build history website.

- Edvin Baggman: Setting notification status for build fails. Implementation of the git cloning. Update README. Stitching all sub-steps together.

- Erik Hedlund: Implement automatic test running. Integrating the repositories' test cases. Integrate dummy repositories test cases. Update README.

- Jennifer Larsson: Setting up git interfacing library. Set up main repository. Implementing static syntax checking. Stitching all sub-steps together. Parsing request json-object.
