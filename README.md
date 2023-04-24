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

Create topics, it can be publics or private.
```json
{"action": "create","topic_name": "create_new_topic", "is_private": true}
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

## Considerations
Sometimes in windows it cant be run scripts like the same wscat, so in order to be able to execute the wscat we should execute the next command as administrator in the powershell.

To be able to run wscat in powershell:
```powershell
Set-ExecutionPolicy RemoteSigned
```

And to go back to normality:
```powershell
Set-ExecutionPolicy Restricted
```

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