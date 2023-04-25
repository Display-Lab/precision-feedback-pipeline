# precision-feedback-pipeline

This is the pipeline service that implements Precision Feedback Pipeline.

To test the pipeline hosted in heroku:
1. Download, postman app from ```https://www.postman.com/downloads/``` and install it.

2. send a POST request  to the ip address ```https://pfpapi.herokuapp.com/createprecisionfeedback/```
with the details present in input_message.json using the postman app.
3. If you are running the pipeline in heroku have the debug="no" in input

To test the pipeline locally:

1. Install poetry using the command ```pip install poetry```(assuming that python and pip are already installed in the computer in which you test locally)

2. Once poetry is installed- use the following command to install the package dependencies
    ```poetry install```

3. In command line where pfp_api codebase is existing,type the command -``` poetry run uvicorn main:app --reload```

4. Download ,postman app from ```https://www.postman.com/downloads/``` and install it.

5. Send a POST request to the ip address ```127.0.0.1:8000/createprecisionfeedback/``` with details present in [input_message.json](input_message.json) using the postman app

6. If you are running the pipeline locally and want to see intermediate files have the debug="yes" in input_message.json 

7. if you want to set export variable for the causal pathways in the pipeline, you can do so by using the   command
    poetry export PATHWAYS='url'
    or
    poetry export PATHWAYS='file//'
    example:     
    poetry export PATHWAYS=https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/causal_pathways/social_better.json

    poetry export PATHWAYS= file:///Users/ayshjag/knowledge-base/causal_pathways/social_better.json

    Then use the command
    poetry uvicorn main:app --reload
