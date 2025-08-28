from dotenv import load_dotenv
import os

load_dotenv()

URL=os.getenv("URL")
ENTERPRISE=os.getenv("ENTERPRISE")
STORE=os.getenv("STORE")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")

EDY360LOG_URL=os.getenv("EDY360LOG_URL")

STORES={
    1000: "Pacaembu",
    6462: "Portugal",
    1611: "Aricanduva",
    2603: "Tatuapé",
    1803: "Lar Center",
    11885: "República",
    172: "Matriz"
}
EMAIL_APP=os.getenv("EMAIL_APP")
PASSWORD_APP=os.getenv("PASSWORD_APP")