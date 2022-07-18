# Payload Format

Payloads being sent and received by Swish should be JSON objects that match the following format.

```json
{
  "op": "",
  "d": {}
}
```

Received payloads that do not match this format are ignored.

- The `op` field should contain a string value indicating the payload type being sent or received. See [Op Codes](#op-codes) for a list of possible values.
- The `d` field should contain another JSON object containing the payload data.

# Op Codes

| Op                                  | Description |
|:------------------------------------|:------------|
| [voice_update](#voice_update)       | TBD         |
| [destroy](#destroy)                 | TBD         |
| [play](#play)                       | TBD         |
| [stop](#stop)                       | TBD         |
| [set_pause_state](#set_pause_state) | TBD         |
| [set_position](#set_position)       | TBD         |
| [set_filter](#set_filter)           | TBD         |
| \***[event](#event)**               | TBD         |

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

- `guild_id`: The id of the player this `voice_update` is for.
- `session_id`: voice state session id received from a
  discord [`VOICE_STATE_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-state-update) event.
- `token`: voice connection token received from a
  discord [`VOICE_SERVER_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-server-update) event.
- `endpoint`: voice server endpoint received from a
  discord [`VOICE_SERVER_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-server-update) event.

<sub>the `endpoint` field of a [`VOICE_SERVER_UPDATE`](https://discord.com/developers/docs/topics/gateway#voice-server-update) event can sometimes be null when the voice server is unavailable. Make sure you check for this before sending a `voice_update` payload type.</sub>

## destroy

```json
{
  "op": "destroy",
  "d": {
    "guild_id": "490948346773635102"
  }
}
```

- `guild_id`: The id of the player you want to destroy.

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

- `guild_id`: The id of the player you want to play a track on.
- `track_id`: The id of the track you want to play.
- (optional) `start_time`: The time (in milliseconds) to start playing the given track at.
- (optional) `end_time`: The time (in milliseconds) to stop playing the given track at.
- (optional) `replace`: Whether this track should replace the current track or not.

## stop

```json
{
  "op": "stop",
  "d": {
    "guild_id": "490948346773635102"
  }
}
```

- `guild_id`: The id of the player you want to stop playing a track on.

## set_pause_state

```json
{
  "op": "set_pause_state",
  "d": {
    "guild_id": "490948346773635102",
    "state": true
  }
}
```

- `guild_id`: The id of the player you want to set the pause state for.
- `state`: A true or false value indicating whether the player should be paused or not.

## set_position

```json
{
  "op": "set_position",
  "d": {
    "guild_id": "490948346773635102",
    "position": 1000
  }
}
```

- `guild_id`: The id of the player you want to the set the position for.
- `position`: The position (in milliseconds) to set the current track to.

## set_filter

<sub>Not implemented lol</sub>

## event

### track_start

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102",
    "type": "track_start"
  }
}
```

### track_end

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102",
    "type": "track_end"
  }
}
```

### track_error

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102",
    "type": "track_error"
  }
}
```

### player_update

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102",
    "type": "player_update"
  }
}
```

### player_debug

```json
{
  "op": "event",
  "d": {
    "guild_id": "490948346773635102",
    "type": "player_debug"
  }
}
```
