# Payloads

| Op                                  | Description   |
|:------------------------------------|:--------------|
| [voice_update](#voice_update)       | do cool stuff |
| [destroy](#destroy)                 | do cool stuff |
| [play](#play)                       | do cool stuff |
| [stop](#stop)                       | do cool stuff |
| [set_pause_state](#set_pause_state) | do cool stuff |
| [set_position](#set_position)       | do cool stuff |
| [set_filter](#set_filter)           | do cool stuff |
| \***[event](#event)**               | do cool stuff |

*<sub>Payloads that are sent *from* Swish to clients.</sub>

### voice_update

```json
{
  "op": "voice_update",
  "d": {
    "guild_id": "490948346773635102",
    "session_id": "e791a05f21b28e088e654865050b29bb",
    "token": "baa182102d236205",
    "endpoint": "rotterdam2601.discord.media:443"
  }
}
```

### destroy

```json
{
  "op": "destroy",
  "d": {
    "guild_id": "490948346773635102"
  }
}
```

### play

```json
{
  "op": "play",
  "d": {
    "guild_id": "490948346773635102",
    "track_id": "eyJ0aXRsZSI6ICJEdWEgTGlwYSAtIFBoeXNpY2FsIChPZmZpY2lhbCBWaWRlbykiLCAiaWRlbnRpZmllciI6ICI5SERFSGoyeXpldyIsICJ1cmwiOiAiaHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj05SERFSGoyeXpldyIsICJsZW5ndGgiOiAyNDQwMDAsICJhdXRob3IiOiAiRHVhIExpcGEiLCAiYXV0aG9yX2lkIjogIlVDLUotS1pmUlY4YzEzZk9Da2hYZExpUSIsICJ0aHVtYm5haWwiOiBudWxsLCAiaXNfbGl2ZSI6IG51bGx9",
    "start_time": 0,
    "end_time": 0,
    "replace": true
  }
}
```

### stop

```json
{
  "op": "stop",
  "d": {
    "guild_id": "490948346773635102"
  }
}
```

### set_pause_state

```json
{
  "op": "set_pause_state",
  "d": {
    "guild_id": "490948346773635102",
    "state": true
    // true = pause, false = resume.
  }
}
```

### set_position

```json
{
  "op": "set_position",
  "d": {
    "guild_id": "490948346773635102",
    "position": 1000
    // milliseconds, 1 second = 1000 milliseconds.
  }
}
```

### set_filter

<sub>Not implemented lol</sub>

### event

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102"
    // stuff soon
  }
}
```
