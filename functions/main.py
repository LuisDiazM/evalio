import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import pytz
subject = "GESTIONES ADMINISTRATIVAS"
group_id = "E041"
period = "2025-1"
timelocal = datetime.now(pytz.timezone("America/Bogota"))
print(timelocal)
professor = "Ingri Rojas"
df = pd.read_csv("students.csv")
students = df.to_dict(orient="records")
group = {
    "name": group_id,
    "period": period,
    "subject_name": subject,
    "professor_name": professor,
    "professor_id": "2312321"
    "students": [{"name": x.get("Nombre",""), "identification": x.get("Documento","")} for x in students],
    "created_at": timelocal
}

# Conexión a MongoDB (ajusta la URI según tu configuración)
client = MongoClient("mongodb://developer:89c2ff58768d4d2afaa137f8@localhost:27017/")

# # Seleccionar base de datos y colección
db = client["manager"]
colection = db["groups"]

colection.insert_one(group)
