import requests

url = "http://localhost:8000/tts/finetuned"
data = {"text": "Habari, karibu kwenye mfumo wetu wa kusikiliza kwa Kiswahili."}
response = requests.post(url, json=data)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.wav")
else:
    print(f"Error: {response.json()['detail']}")