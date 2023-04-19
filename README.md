# API WS

### Conexion
omar

```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE5OTg4MjQsImlhdCI6MTY4MTkxMjQyNCwic3ViIjoib21hciIsInBheWxvYWQiOnsiZGVzY3JpcHRpb24iOiJUZXN0IHRva2VuIn19.xiXwJ8Z5LNSC35wBMjVw6V6Jn56wW7ltfPUH3_LXqR8
```

diego

```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE5OTg4MDYsImlhdCI6MTY4MTkxMjQwNiwic3ViIjoiZGllZ28iLCJwYXlsb2FkIjp7ImRlc2NyaXB0aW9uIjoiVGVzdCB0b2tlbiJ9fQ.8copNWFY6etWJBwrF11sMJ3WCYizKXjRAGsbRA4TY7U
```

satoshi

```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE5OTg3NzksImlhdCI6MTY4MTkxMjM3OSwic3ViIjoic2F0b3NoaSIsInBheWxvYWQiOnsiZGVzY3JpcHRpb24iOiJUZXN0IHRva2VuIn19.5QorLl_ITxLL4Br3PjlGAtjiwdKJ91DNHFyP6lFljrg
```

memoor

```
wscat -c ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE5OTg4NDQsImlhdCI6MTY4MTkxMjQ0NCwic3ViIjoibWVtb29yIiwicGF5bG9hZCI6eyJkZXNjcmlwdGlvbiI6IlRlc3QgdG9rZW4ifX0.AWAfwiKvEgfHEDOzrpcya0fUYUKantH_QQEXtie7tw4
```

### Autenticate

omar
{"action" : "authenticate", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE4NTg3NDgsImlhdCI6MTY4MTc3MjM0OCwic3ViIjoib21hciIsInBheWxvYWQiOnsiZGVzY3JpcGNpb24iOiJjdWFscXVpZXJfY29zYSJ9fQ.wNEyAllFh4wVK_typ0ll2GGQBdIFq9a2MjJBK-5T0zM"}

diego
{"action" : "authenticate", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE4NTc0MDAsImlhdCI6MTY4MTc3MTAwMCwic3ViIjoiZGllZ28iLCJwYXlsb2FkIjp7ImRlc2NyaXBjaW9uIjoiY3VhbHF1aWVyX2Nvc2EifX0.OBt4FOwHzHEprbwLqh_3ErEgkyzEc6iNAyhCgDc-JEs"}

satoshi
{"action" : "authenticate", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE4NTg3NzgsImlhdCI6MTY4MTc3MjM3OCwic3ViIjoic2F0b3NoaSIsInBheWxvYWQiOnsiZGVzY3JpcGNpb24iOiJjdWFscXVpZXJfY29zYSJ9fQ.ZwyPrg1ZD19z3ydooBZAV1S8kHc-qXQG-S3-mYFUybg"}


### Acciones
Listar tópicos públicos
```json
{"action": "list_topics"}
```

Suscribirse a tópicos públicos
```json
{"action": "suscribe","topic_name": "public_topic_to_suscribe"}
```

Suscribir usuarios a tópicos privados a los que pertenece un usuario
```json
{"action": "invite","topic_name": "private_topic_name_to_invite"}
```

Crear tópicos sean públicos o privados
```json
{"action": "create","topic_name": "create_new_topic"}
```

Para mandar mensajes a un tópico o usuario en concreto, en donde se debe de saber el nombre del tópico o el usuario en caso
de mensaje directo
```json
{"action": "message","topic_name": "noticias","content": "Content of the message"}
```

Para traer mensajes faltantes de entregar al query de la base donde se manda mensajes se debe hacer por los tópicos a los 
que el usuario está suscrito más el tópico de usuario del propio usario, haciendo el query en la BD por topic_id del mensaje guardado en la BD de mensajes

El mensaje a publicar en un tópico o de mensaje directo sería de la siguiente manera:

```json
{
    "source": "gdcode (este es el tópico o el usuario que mando el mensaje directo)",
    "content": "The content of the message"
}
```

Pregunta sobre buenas prácticas para este proyecto con chat gpt:
Entonces listar tópicos y crear nuevos tópicos mejor por api rest y suscribirse a un websocket por el mismo web socket sería lo mejor correcto?

Sí, esa sería una buena práctica. Usar un API REST para listar y crear nuevos tópicos proporcionaría una interfaz clara y fácil de usar para los clientes que desean interactuar con su aplicación, mientras que usar WebSockets para la suscripción permitiría una comunicación en tiempo real y eficiente entre el cliente y el servidor.

Aparte un API rest para crear usuarios y eliminarlos
Un API rest para gestionar tópicos, crearlos, listar tópicos de X usuario

En windows luego no se pueden correr scripts como el mismo wscat, se debe de ejecutar lo siguiente en powershell como administrador:

```
Set-ExecutionPolicy RemoteSigned
```

Y para volver a la normalidad:

```
Set-ExecutionPolicy Restricted
```