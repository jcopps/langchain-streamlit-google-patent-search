<h1 align="center">
📖 Chat with Google Patents using LangChain-Streamlit App Template
</h1>

![UI](ui.png?raw=true)

## 🔧 Features

- Chat with a `patent` that is available on Google
- Provide its link, and start chatting
- Question around any portion of the patent
- A ChatBot using LangChain and Streamlit
- It uses Open AI LLM, other providers will be supported soon

This repo contains an `main.py` file which has a template for a chatbot implementation.

## Adding your chain
To add your chain, you need to change the `load_chain` function in `main.py`.
Depending on the type of your chain, you may also need to change the inputs/outputs that occur later on.
This requires Chrome to be available on the machine where the streamlit is installed and run.
Chrome is used to download the patent as a PDF.
ChromaDB is used for storing the PDF in vectorised form splitting them by pages using NLTK splitter.


## 💻 Running Locally

1. Clone the repository📂

```bash
git clone https://github.com/jcopps/langchain-streamlit-google-patent-search.git
```

2. Install dependencies with [Poetry](https://python-poetry.org/) and activate virtual environment🔨

```bash
poetry install
poetry shell
```

3. Run the Streamlit server🚀

```bash
streamlit run app/main.py 
```

Run App using Docker (Not tested - Chrome dependency)
--------------------
This project includes `Dockerfile` to run the app in Docker container. In order to optimise the Docker Image
size and building time with cache techniques, I have follow tricks in below Article 
https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

Build the docker container

``docker  build . -t google-patent-chat-app:latest ``

To generate Image with `DOCKER_BUILDKIT`, follow below command

```DOCKER_BUILDKIT=1 docker build --target=runtime . -t google-patent-chat-app:latest```

1. Run the docker container directly 

``docker run -d --name google-patent-chat-app -p 8080:8080 google-patent-chat-app ``
``docker run -d --name google-patent-chat-app -p 8080:8080 google-patent-chat-app ``

2. Run the docker container using docker-compose (Recommended)

``docker-compose up``


Deploy App on Streamlit Public Cloud (Not tested - Chrome dependency)
------------------------------------
This app can be deployed on Streamlit Public Cloud using GitHub. Below is the Link to 
Publicly deployed App

https://langchain-docker-template-amjadraza.streamlit.app/


Deploy App on Google App Engine (Not tested - Chrome dependency)
--------------------------------
This app can be deployed on Google App Engine following below steps.

## Prerequisites

Follow below guide on basic Instructions.
[How to deploy Streamlit apps to Google App Engine](https://dev.to/whitphx/how-to-deploy-streamlit-apps-to-google-app-engine-407o)

We added below tow configurations files 

1. `app.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

I have adopted `Dockerfile` to deploy the app on GCP APP Engine.

1. Initialise & Configure the App

``gcloud app create --project=[YOUR_PROJECT_ID]``

2. Deploy the App using

``gcloud app deploy``

3. Access the App using 

https://langchain-chat.ts.r.appspot.com/


Deploy App on Google Cloud using Cloud Run (Not tested - Chrome dependency)
------------------------------------------

This app can be deployed on Google Cloud using Cloud Run following below steps.

## Prerequisites

Follow below guide on basic Instructions.
[How to deploy Streamlit apps to Google App Engine](https://dev.to/whitphx/how-to-deploy-streamlit-apps-to-google-app-engine-407o)

We added below tow configurations files 

1. `cloudbuild.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

we are going to use `Dockerfile` to deploy the app using Google Cloud Run.

1. Initialise & Configure the Google Project using Command Prompt

`gcloud app create --project=[YOUR_PROJECT_ID]`

2. Enable Services for the Project

```
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

3. Create Service Account

```
gcloud iam service-accounts create langchain-app-cr \
    --display-name="langchain-app-cr"

gcloud projects add-iam-policy-binding langchain-chat \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding langchain-chat \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding langchain-chat \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/run.admin"
``` 

4. Generate the Docker

`DOCKER_BUILDKIT=1 docker build --target=runtime . -t australia-southeast1-docker.pkg.dev/langchain-chat/app/google-patent-chat-app:latest`

5. Push Image to Google Artifact's Registry

`configure-docker` authentication     

`gcloud auth configure-docker australia-southeast1-docker.pkg.dev`

In order to push the `docker-image` to Artifact registry, first create app in the region of choice. 

Check the artifacts locations

`gcloud artifacts locations list`

Create the repository with name `app`

```
gcloud artifacts repositories create app \
    --repository-format=docker \
    --location=australia-southeast1 \
    --description="A Langachain Streamlit App" \
    --async
```

Once ready, let us push the image to location

`docker push australia-southeast1-docker.pkg.dev/langchain-chat/app/google-patent-chat-app:latest`

6. Deploy using Cloud Run

Once image is pushed to Google Cloud Artifacts Registry. Let us deploy the image.

```
gcloud run deploy google-patent-chat-app --image=australia-southeast1-docker.pkg.dev/langchain-chat/app/google-patent-chat-app:latest \
    --region=australia-southeast1 \
    --service-account=langchain-app-cr@langchain-chat.iam.gserviceaccount.com
```

## Report Feedbacks

As `langchain-streamlit-docker-template` is a template project with minimal example. Report issues if you face any. 

## DISCLAIMER

This is a template App, when using with openai_api key, you will be charged a nominal fee depending
on number of prompts etc.
