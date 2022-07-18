# Opening a Connection

Opening a websocket connection requires all of the following headers to be set.

```
Authorization: Password as defined in your swish.toml file.
User-Id: The user id of the bot connecting to Swish.
User-Agent: The client library and version used to connect to Swish.
```

# Close Codes

All intentional websocket close codes are listed below.

| Close code | Reason                                        |
|:-----------|:----------------------------------------------|
| 4000       | `User-Id` or `User-Agent` header is missing.  |
| 4001       | `Authorization` header is missing or invalid. |
