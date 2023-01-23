# pfp_API

This is the pipeline service that implements Precision Feedback Pipeline.

To test the pipeline hosted in heroku:
1. Download-postman.exe
2. send a POST request  to the ip address '''https://pfpapi.herokuapp.com/createprecisionfeedback/''
with the details present in input_message.json

To test the pipeline locally:
1. In command line where pfp_api codebase is existing,type the command -'''uvicorn main:app --reload'''
2. Send a POST request to the ip address '''127.0.0.1:8000/createprecisionfeedback/''' with details present in input_message.json
