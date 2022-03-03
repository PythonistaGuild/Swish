# WebSocket Payloads

Payloads being sent and received by Swish should be JSON objects and match the following format.

```json
{
  "op": "",
  "d": {}
}
```

Received payloads that do not match this format are ignored.

- The `op` key should contain a string value indicating the payload type being sent or received. See [Op Codes](#op-codes) for a list of possible values.
- The `d` key should be another JSON object containing the payload data. All keys shown in the `d` key are required unless otherwise noted.

# Op Codes

| Op                                  | Description                                                            |
|:------------------------------------|:-----------------------------------------------------------------------|
| [voice_update](#voice_update)       | instructs a player to connect to the given discord voice server.       |
| [destroy](#destroy)                 | destroys a player.                                                     |
| [play](#play)                       | tells a player to play the given track.                                |
| [stop](#stop)                       | stops a players current track.                                         |
| [set_pause_state](#set_pause_state) | sets a players pause state.                                            |
| [set_position](#set_position)       | sets a players position within its current track.                      |
| [set_filter](#set_filter)           | sets or updates a players active audio filters.                        |
| \***[event](#event)**               | an update containing useful information about swish or a player event. |

*<sub>payloads that are sent *from* Swish to clients.</sub>

## voice_update

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
- `guild_id`: the ID of the guild this `voice_update` is for.
- `session_id`: voice state session ID received from a discord [`VOICE_STATE_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-state-update) event.
- `token`: voice connection token received from a discord [`VOICE_SERVER_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-server-update) event.
- `endpoint`: voice server endpoint from a discord [`VOICE_SERVER_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-server-update) event.

<sub>the `endpoint` key can be null when discord is 'awaiting endpoint', swish accommodates for clients sending a null `endpoint` by ignoring the `voice_update`.</sub> 

## destroy

```json
{
  "op": "destroy",
  "d": {
    "guild_id": "490948346773635102"
  }
}
```

## play

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

## stop

```json
{
  "op": "stop",
  "d": {
    "guild_id": "490948346773635102"
  }
}
```

## set_pause_state

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

## set_position

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

## set_filter

<sub>Not implemented lol</sub>

## event

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102",
    "type": ""
  }
}
```
