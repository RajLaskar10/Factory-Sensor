import logging
import azure.functions as func
import json

def main(event: func.EventHubEvent, outBlob: func.Out[str]):
    data = json.loads(event.get_body().decode())
    logging.info(f"Received: {data}")
    # If it’s super hot, save it!
    if data.get('temperature', 0) > 80:
        outBlob.set(json.dumps(data))
        logging.info("🔥 Hot alert saved!")