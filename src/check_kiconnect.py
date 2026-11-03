import csv
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

url = os.getenv("KICONNECT_BASE_URL") + "/chat/completions"
key = os.getenv("KICONNECT_API_KEY")
model = os.getenv("KICONNECT_MODEL")

while True:
    try:
        start = time.time()

        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Antworte mit OK"}],
                "max_tokens": 2,
                "temperature": 0,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        answer = data["choices"][0]["message"]["content"]
        used_model = data.get("model", model)
        usage = data.get("usage", {})

        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)
        latency = round((time.time() - start) * 1000)
        timestamp = datetime.now().isoformat(timespec="seconds")

        print(f"Modell: {used_model}")
        print(f"Antwort: {answer}")
        print(f"Tokens: {input_tokens} + {output_tokens} = {total_tokens}")
        print(f"Antwortzeit: {latency} ms\n")

        with open("kiconnect_health.csv", "a+", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow([
                    "timestamp",
                    "model",
                    "answer",
                    "input_tokens",
                    "output_tokens",
                    "total_tokens",
                    "latency_ms",
                ])

            writer.writerow([
                timestamp,
                used_model,
                answer,
                input_tokens,
                output_tokens,
                total_tokens,
                latency,
            ])

    except Exception as error:
        print(datetime.now(), error)

    time.sleep(30 * 60)