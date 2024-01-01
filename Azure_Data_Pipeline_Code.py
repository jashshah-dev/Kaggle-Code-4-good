import urllib.request
import json
import os
import ssl
import pandas as pd 
from googletrans import Translator 

def translate_to_english(text):
    try:
        # Create a Translator instance
        translator = Translator()

        # Translate the text to English
        translated_text = translator.translate(text, dest='en')

        return translated_text.text
    except Exception as e:
        return str(e)


# Transcripts
with open('input_1.json') as f:
  transcripts = json.load(f)

def get_answer_object(context, question):

  def allowSelfSignedHttps(allowed):
      # bypass the server certificate verification on client side
      if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
          ssl._create_default_https_context = ssl._create_unverified_context

  allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service

  # Request data goes here
  # The example below assumes JSON formatting which may be updated
  # depending on the format your endpoint expects
  # More information can be found here:
  # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
  data = {
    "inputs": {
      "question": question,
      "context": context
      }
  }

  body = str.encode(json.dumps(data))

  url = 'https://roberta.eastus.inference.ml.azure.com/score'
  api_key = 'KcgCu6pRg9zK9CvT8Q4dtkRbuGpzY7gf' # Replace this with the key or token you obtained


  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)

      #result = response.read()
      return response
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(context)
      print(question)
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))
      print('-------------------------------------')

def get_answer(response):
  result = response.read()

  # Decode bytes to string
  result_str = result.decode('utf-8')

  # Parse the JSON string
  result_dict = json.loads(result_str)

  # Access the values
  score = result_dict['score']
  answer = result_dict['answer']

  return score, answer

import pandas as pd 
from googletrans import Translator

questions_list = [
    "What is the patient's name?",
    "What is the patient's age?",
    "What is the patient's condition?",
    "What symptoms is the patient experiencing?",
    "What precautions did the doctor advise?",
    "What drugs or medications did the doctor prescribe?"
]

# Initialize a list to store data for each transcript
data = []

for id, transcript in transcripts.items():
    context = translate_to_english(transcript)

    # Initialize lists for each transcript
    ids = [id] * len(questions_list)
    questions = questions_list.copy()
    answers = []
    scores = []

    # Get answers for each question
    for question in questions:
        answer_object = get_answer_object(context, question)
        score, text = get_answer(answer_object)

        scores.append(score)
        answers.append(text)

    # Append data for the current transcript to the list
    data.extend(list(zip(ids, questions, answers, scores)))

# Create the global DataFrame
df_global = pd.DataFrame(data, columns=['Id', 'Question', 'Answer', 'Scores'])
output_file_name='input_1.csv'
df_global.to_csv(output_file_name,index=False)

from azure.storage.blob import BlobServiceClient


adls_conn_string_value = "DefaultEndpointsProtocol=https;AccountName=azmld4gcomp2906763747;AccountKey=BYhwVGvTbM6wBF+e4I0IbrBTpcLBbLRYaZKlBWJVfBky+8UyqGD8p99T1V11zxoNcEWl3xqQvdBz+AStPiju0Q==;EndpointSuffix=core.windows.net"

def get_container_client():
    connection_string = adls_conn_string_value
    container_name = "competition"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
 
    return container_client


  
container_client= get_container_client()


target_file_location='competition'

with open(output_file_name, "rb") as data:
    container_client.upload_blob(name=f"{target_file_location}/{output_file_name}", data=data,overwrite=True)



