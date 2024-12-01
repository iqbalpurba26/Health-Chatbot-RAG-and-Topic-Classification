# GET STARTED

To learn more about this project, you can access the detailed information [[HERE]](https://github.com/iqbalpurba26/Health-Chatbot-RAG-and-Topic-Classification/blob/main/ABOUT%20PROJECT.md)

Before running this project, there are a few things you need to pay attention to:

- Make sure you have a knowledge base containing information about medications, allergies, and menstruation. The chatbot's knowledge base should be stored in a folder named ```vectorstore```.
- Ensure you've created a .env file that includes the API_KEY and other information needed to connect the project with GPT.

Then you can run the project by following these steps:
1. Clone this repository https://github.com/iqbalpurba26/Healt-Chatbot-RAG-And-Intent-Classification
2. Prepare the environment
```
python -m venv env

env\Scripts\activate.bat

pip install -r requirements.txt
```
3. Run the project
```
uvicorn main:app --reload
```

4. (Optional) You can try accessing the API through Postman by providing an input body like this:
```
{
    "prompt": "Your prompt"
}
```