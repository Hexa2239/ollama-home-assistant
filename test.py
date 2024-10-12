import requests

def send_prompt_over_network():
    request = requests.post("http://192.168.0.3:11434/api/generate", data='{"model" : "llama3.1", "prompt" : "Hello!", "stream": false}')

    print(request.text)

send_prompt_over_network()