# API WS

### Connection and authenticate
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

Para desconectarse del servidor de la manera correcta:
```json
{"action": "disconnect"}
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

Para crear tópico:
```json
{
    "topic_name": "the_topic_name"
}
```