# Websockets
This project has 2 main microservices which are one is an API in which you can manage the topics and messages queue.
There are a lot of improvements that can be made but the focus of this project is to have the websocket working as expected.

## Actions
The actions that can be performed are the next ones:

Subscribe to public topics.
```json
{"action": "suscribe","topic_name": "public_topic_to_suscribe"}
```

Subscribe users to private topics in which another user is part of.
```json
{"action": "invite","topic_name": "private_topic_name_to_invite","username": "eder"}
```

To send messages to a topic or to a user in specific. In the topic name should be the user if its the case you want to send a directly message.
```json
{"action": "message","topic_name": "noticias","content": "Content of the message"}
```

Disconnect from the server in a normal way.
```json
{"action": "disconnect"}
```

Also something else that can be consider as an indirect action is the functionality to send pending messages if for example a user that is part of a topic but one or more users are not connected then a message is stored in the database so when user is connected again then they receive the pending messages again.

## Good practices
In order to follow a kind of standard for good programming practices I implemented a pylint as a github action to be run every time a push is made to the develop branch, this will help us to correct and follow good practices.

## Considerations
The code has is been developed in python 3.10, so this code will only run in versions of python 3.10 onwards.


Sometimes in windows it cant be run scripts like the same wscat, so in order to be able to execute the wscat we should execute the next command as administrator in the powershell.

To be able to run wscat in powershell:
```powershell
Set-ExecutionPolicy RemoteSigned
```

And to go back to normality:
```powershell
Set-ExecutionPolicy Restricted
```

About authentication for the websocket server there is a endpoint that retrieves the same token to be used, as query params you should include yes or yes the user so the API can generate the token:

So username word should be exactly the username that is going to be used to add to the connected users in the websocket API.
After you get the token below the way to use it to authenticate to the websocket API.

## Connection and authentication
Below we can see some users created with the purpose to test the present exercise so in this case we are going to use wscat which is a nodejs dependency that can be installed through npm, this means also that you should have nodejs, you can click [here](https://nodejs.org/en/download) to go to the official page of nodejs and install it if its the case you want to test with wscat, so follow the instructions in that link.
After nodejs is isntalled in your respective operative system then you should install wscat by running the next command below:
```
npm install -g wscat
```
For more information about wscat you can click [here](https://www.npmjs.com/package/wscat) to go to the documentation of wscat library.

Now commands below can be used to authenticate to the websocket server, in this specific case then we use a script part of this project which is `gen_tokens.py` to generate an updated token, it expires in one day, of course better jwt can be performed but for this case we only need to comply that the jwt is still current. Below after the port and the `/` is the token per user.

omar

```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODIzNDkwMzUsImlhdCI6MTY4MjI2MjYzNSwic3ViIjoib21hciIsInBheWxvYWQiOnsiZGVzY3JpcHRpb24iOiJUZXN0IHRva2VuIn19.BYeL0-7k_bM2BvLS0Me-vvd0om-WkXGSvuhm4WPuxWs
```

diego
```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODIzNDkwMDUsImlhdCI6MTY4MjI2MjYwNSwic3ViIjoiZGllZ28iLCJwYXlsb2FkIjp7ImRlc2NyaXB0aW9uIjoiVGVzdCB0b2tlbiJ9fQ.yiS5HlCEoqUjW0pp9UerpymJJvD_07lJCCSMZr0vAf8
```

satoshi
```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODIzNDkwNTcsImlhdCI6MTY4MjI2MjY1Nywic3ViIjoic2F0b3NoaSIsInBheWxvYWQiOnsiZGVzY3JpcHRpb24iOiJUZXN0IHRva2VuIn19.Mxl6LujulMFeGWF7LvNG5G4NbFwp18HAQKoV7LgmhVM
```

memoor
```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODIzNDkxMTksImlhdCI6MTY4MjI2MjcxOSwic3ViIjoibWVtb29yIiwicGF5bG9hZCI6eyJkZXNjcmlwdGlvbiI6IlRlc3QgdG9rZW4ifX0.DNO5TU4ie8-gPWUx9BEtai1QD_3MyZg7tlDE7kRdcII
```

## About deployment
In this case i took into consideration that the labor of deployment should be part of devops, As you can see inside the folders `api_topics` and `websocket` there is inside a Dockerfile which is responsability of the same developer cause there you need to copy the files necessary to run the script and also to install all dependencies needed to run correctly the microservice. However, the deployment part should be configured by a devops or SRE area and using the Dockerfiles created by the developer, so thats why I dont remember how to do it cause in my actual jobs that part is fully dedicated to a devops or SRE team. But of course, if its needed I can learn.

## Unit tests
In this part I wasnt able to create the unit tests because I have to break myself into several parts to fulfill the responsibilities of my current job and also the times when I should rest, otherwise I would be overloaded if I only code all the time, so I apologize for this case, but eventually I will upload them more calmly and having more time because I dont like to left projects incompleted when are at this point of development.

# API
This API is used by the same websocket service but also some of the endpoints here should be used from the client before going to the websocket server. The postman collection as an example can be found by clicking [here](https://github.com/dmtzs/SmartLockApi/wiki/postman-collection)

# Conceptual challengue
Below are the questions and answers for the conceptual challengue.


1. How would you design and build a payment processing system that can handle a high volume of transactions per second while maintaining high levels of security?
Answer = The answer for this is that we need to take in consideration ssome things like:
    1. System architecture: An system architecture should be designed that allows a high scalability and processing capacity and an architecture that allows multiple transactions simultaneously.
    2. Security: To keep safe the payment data and prevent possible fraud. Of course im talking here about encryption, user authentication, validate the same transactions by an algorithm and a human should be part of the process cause an algorithm is not going to be perfect at all for example, with new fraud cases.
    3. Monitoring: There should be implemented a monitoring tool or tools and tools for managing the risk of possible fraud and system problems or security problems.
    4. Integrations: The system should be compatible with many payment systems to offer a wide range of options to users.
    5. Tests: The system should be tested a lot to be sure that works as expected and also to be sure that is completely resilient to anomalies and to errors so we can understand what is happening if something happens and not only the developers, but also the client can have a little bit of context withput compromising the system security.
    6. Audits: The system should be audited periodically to guarantee the security standards and compliance.

2. How would you develop an algorithm that can identify and prevent fraudulent transactions on a financial platform?
Answer = I think that we should comply with many things and some of them but not all of course are described below:
    1. Collect data: One of the most important thing in my consideration is to collect several data about, in this case, the transactions in which you can include for example data of the client, the type of the transaction, geographic location, transactions history, etc. Everything according to the necesity and the business branch if its the case you have more than one branch that manages money.
    2. Identify patterns: In this part should be used tecniques of data mining and maybe machine learning for data analyzing and detect patterns that can indicate a fraudulent transaction. It can be used algorithms such as decision trees, neural networks, etc.
    3. Rules: Rules should be established after fraudulent patterns are identified, for example a user has been done transactions in mexico all the time but after a while they do a transaction in nigeria, so you can think about that if its something anomalous or if the user is only in vacations.
    4. Check manually: A manual check should be done because after all the algorithms of before is not possible that all the time the algorithm willl do the things correctly so alway a human should do a double check if the algorithm doesnt detect something.
    5. Updates: Finally the algorithm should be keep updating himself like an antivirus, so the algorithm needs too to be updated all the time when new patterns and practices are detected in the world.

3. How would you build a scalable and reliable data processing pipeline that can handle large amounts of financial data from multiple sources?