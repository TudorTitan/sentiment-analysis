from openai import OpenAI
import numpy as np
#All OpenAI manipulations go here
#OpenAI API key is used as local env.
client = OpenAI()

model="text-embedding-ada-002"

#compute cosine similarity between two vectors
def cosine_similarity(v1, v2):
   dp = np.dot(v1,v2)
   mag1 = np.linalg.norm(v1)
   mag2 = np.linalg.norm(v2)
   return dp/ (mag1 * mag2)

#send text and receive a vector embedding
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding
