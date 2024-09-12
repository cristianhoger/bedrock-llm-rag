# Introduction
Implementation of a simple application that sends requests to a AWS Bedrock agent, running Titan as LLM and using Pinecone for the RAG.

Services used:

- S3 -> To store projects information and 1 bucket to store the static website.
- Bedrock -> Create embeddings and run LLM Model Titan through an agent..
- Lambda -> Funtion written in Python to get the request from the API and return the response from the model.
- API Gateway -> Publish the post endpoint to execute the Lambda function.
- Pinecone -> Vector database utilized to store the embeddings in order to provide RAG to the LLM model.
  
![Architecture Diagram](images/Bedrock-agent.drawio.svg)

# 1- Creation of the Vector Database
In order to store the embeddings, it is necessary to use what is called a vector database, here some insights:
- AWS Offers by default offers Opensearch engine to create the vector database. Unfortunately this service is not serverless and has daily fixed costs that start in 10 euros. Pinecone was selected because it has a free tier option.

a- Create an Index: Here the main part is the configuration, where you need to define the dimensions of the database. Luckily Pinecone has a wizard where you select the model that you will use for the embeddings.

![Pinecone Wizard](images/Pinecone%20dimension.png)

b- Select cloud provider: Straightforward, for this example select AWS.

c- Select Regions: For this example we will use us-east-1.

d- Once your index is ready, copy the host URL, you will need it to connect with Bedrock.

c- Create an API key, or use the one by default, this is also needed for the connections.
d- Store the API key in Secrets Manager in AWS.

# 2- Knowledge Base Creation

a- Go to Bedrock and under Builder tools select Knowledge bases, then create knowledge base.

b- Now you need assing the IAM permissions, the easiest to select create and use a new service role. Next in the data source you can choose from where you will get the information for the RAG, in this case we use Amazon S3.

c- Next you can select details of the data source, one important part is the data deletion policy, I select retain so I can delete knowledge bases independant from the vector data base.

d- In the step 3 you must select the model for the embeddings, make sure that the vector dimensions is the same as the dimensions of the vector database in Pinecone.

e- Still in step 3, provide the endpoint URL of the vector data base, and the ARN of the stored secret. 

f- When the data source is created, select and press the sync button, with that the embeddings will be created.

# 3- Agent Creation

a- This is quite straightforward, the key is to select a language model and add the knowledge base previously created.

b- Once you have your agent you will need to create an Alias and a version, with this you can start testing it.

# 4- Create the Lambda function

a- For this example we will create a code in python to send the request to the Bedrock agent and return the response.

b- Make sure that you replace the agent ID and alias ID in the code.

https://github.com/cristianhoger/bedrock-rag-agent/blob/6570a13afce7e113ddd83ffcc60ece415920ed39/lambda_function.py#L1-L75

# 5- Create the API Gateway endpoint

a- In order to make things easier just create an endpoint that will receive the request in the body and call the Lambda function.





