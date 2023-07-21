# Precision Feedback Pipeline
This is the pipeline service that implements the Precision Feedback Pipeline.
See the [wiki page](https://github.com/Display-Lab/precision-feedback-pipeline/wiki) to learn how to test the pipeline.

Start [here](https://github.com/Display-Lab/precision-feedback-pipeline/wiki/Postman-Testing-Workflow) with Postman setup instructions

Local Testing instructions are complete for [MacOS](https://github.com/Display-Lab/precision-feedback-pipeline/wiki/Testing-Local-MacOS-Pipeline) and [Windows](https://github.com/Display-Lab/precision-feedback-pipeline/wiki/Testing-Local-Windows-Pipeline) users

See [this page](https://github.com/Display-Lab/precision-feedback-pipeline/wiki/Testing-with-Heroku) for instructions on using Postman to test the PFP in Heroku

To test in Google Cloud, see the cloud testing wiki [here](https://github.com/Display-Lab/precision-feedback-pipeline/wiki/Testing-with-Google-Cloud/_edit)
<!--
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
    poetry export PATHWAYS=https://github.com/Display-Lab/knowledge-base/tree/main/causal_pathways
    poetry export measures=https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/measures.json
    poetry export templates=https://github.com/Display-Lab/knowledge-base/tree/main/message_templates
    or
    export PATHWAYS=/Users/username/knowledge-base/causal_pathways
    export templates=/Users/username/knowledge-base/templates
    export measures='file:///Users/username/knowledge-base/measures.json'
    

    Then use the command
    poetry uvicorn main:app --reload



To test the pipeline service hosted in Google cloud platform of Michigan Medicine

1. Login to your umich level 1 account
2. Open google chrome  and try accessing anyone of the links below
    
        https://pfp.test.app.med.umich.edu/, 
        https://pfp.lab.app.med.umich.edu/,
        https://pfp.prod.app.med.umich.edu/
        
3. If the request resulted in a failure message- reach out to Display lab administrator and request them to add you to displaylab-dev@umich.edu Mcommunity group
4. If your request to above links were successful, download postman from the link "https://www.postman.com/downloads/" and install it in your computer.

5. Open google chrome and install the postman interceptor plugin
6. open the postman desktop app, at the bottom there is a satelite icon call capture requests and go to via interceptor and enable capture request there, alternatively you can capture request from the google chrome postman plugin
7. Again at the bottom of the postman desktop app you should see a cookie icon. Click on the icon and select the sync cookies add "google.com" and 

        https://pfp.test.app.med.umich.edu/, 
        https://pfp.lab.app.med.umich.edu/,
        https://pfp.prod.app.med.umich.edu/
        
  and click sync cookies

8. go to the new request of postman try any one of the following links


        https://pfp.test.app.med.umich.edu/, 
        https://pfp.lab.app.med.umich.edu/,
        https://pfp.prod.app.med.umich.edu/ 
        
        
    You should see a succesful response
9. Convert the request from Get to post, Add the contents of input message to the body part of the request and change the url to any one of the following links


        https://pfp.test.app.med.umich.edu/createprecisionfeedback, 
        https://pfp.lab.app.med.umich.edu/createprecisionfeedback, 
        https://pfp.prod.app.med.umich.edu/createprecisionfeedback
-->
