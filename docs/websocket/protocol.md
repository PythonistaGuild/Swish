# Protocol

### Opening a connection:

Opening a websocket connection requires all the following headers be set.

```
Authorization: Swish password as defined in your swish.toml file.
User-Id: The user id of the bot connecting to Swish.
User-Agent: The client library and version used to connect to Swish.
```

### Close codes

All the intentional websocket close codes are listed below.

| Close code | Reason                                     |
|:-----------|:-------------------------------------------|
| 4000       | Missing 'User-Id' or 'User-Agent' header.  |
| 4001       | 'Authorization' header missing or invalid. |
