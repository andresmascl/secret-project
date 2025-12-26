I am trying to implement the communication with Google Multimodal Live API to serve as the brains of my local voice assistant. The local assitant will execute the actions either by using local browser automation scripts, or by transforming the Live API text response into audio and playing it localy. The idea is to be able to use the local assitant to ask it to perform tasks using the browser, or to ask direct questions to the LLM. The session (LLM Memory) will be reset after 1 hour, or after the user includes a term in the next message ("Cambiando de tema... <new-instruction-or-message>") to the assitant indicating that it should start a fresh session. The plan is to have the user give an instruction to the assistant, have the assistant open a socket to send the audio to the Live API together with a JSON file indicating the actions the local assistant understands, have the Live API decide the intent, and return a reply also in a JSON format the local assistant can understand. The actions can be such like 'Play one love by bob marley' (the assistant open the browser and plays the song on youtube), or 'what will be the weather for tomorrow in Santiago' (the LLM replies in text format, and the assitant sinthetizes the words into sound locally.

```json
{
	"action": "play_youtube" | "LLM_query",
	"variables":[
		"variable_1": "value 1",
		...,
		"variable_n: "value n"
	],
	"confidence": 0.0-1.0,
}
```