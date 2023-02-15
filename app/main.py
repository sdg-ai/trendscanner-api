from pydantic import BaseModel
from fastapi import FastAPI
import http3, requests
import dotenv, os, json

from models.coordinator import EnrichmentCoordinator

#TODO: Add services hostname and port as env variables
#TODO: Add health check of all services
#TODO: Make parallel calls to the services

class InputText(BaseModel):
    text: str

dotenv.load_dotenv()
client = http3.AsyncClient()
ec = EnrichmentCoordinator(True)

app = FastAPI()

@app.post("/trends")
def process_trends(input_text:InputText):
    output_data = ec.process(input_text.text)
    return output_data
