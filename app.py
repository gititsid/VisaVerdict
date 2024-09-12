from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from typing import Optional

from src.visa_verdict.constants import APP_HOST, APP_PORT
from src.visa_verdict.pipeline.predict import CustomData, PredictionPipeline
from src.visa_verdict.pipeline.data_transformation import DataTransformationPipeline
from src.visa_verdict.pipeline.model_training import ModelTrainingPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.continent: Optional[str] = None
        self.education_of_employee: Optional[str] = None
        self.has_job_experience: Optional[str] = None
        self.requires_job_training: Optional[str] = None
        self.no_of_employees: Optional[str] = None
        self.company_age: Optional[str] = None
        self.region_of_employment: Optional[str] = None
        self.prevailing_wage: Optional[str] = None
        self.unit_of_wage: Optional[str] = None
        self.full_time_position: Optional[str] = None

    async def get_usvisa_data(self):
        form = await self.request.form()
        self.continent = form.get("continent")
        self.education_of_employee = form.get("education_of_employee")
        self.has_job_experience = form.get("has_job_experience")
        self.requires_job_training = form.get("requires_job_training")
        self.no_of_employees = form.get("no_of_employees")
        self.company_age = form.get("company_age")
        self.region_of_employment = form.get("region_of_employment")
        self.prevailing_wage = form.get("prevailing_wage")
        self.unit_of_wage = form.get("unit_of_wage")
        self.full_time_position = form.get("full_time_position")


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse(
        "usvisa.html", {"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = ModelTrainingPipeline()

        x_data, y_data = DataTransformationPipeline().main()
        train_pipeline.main(x_data=x_data, y_data=y_data)

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_usvisa_data()

        usvisa_data = CustomData(
            continent=form.continent,
            education_of_employee=form.education_of_employee,
            has_job_experience=form.has_job_experience,
            requires_job_training=form.requires_job_training,
            no_of_employees=form.no_of_employees,
            company_age=form.company_age,
            region_of_employment=form.region_of_employment,
            prevailing_wage=form.prevailing_wage,
            unit_of_wage=form.unit_of_wage,
            full_time_position=form.full_time_position,
        )

        model_predictor = PredictionPipeline()

        visa_verdict = model_predictor.predict(usvisa_data)

        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": visa_verdict},
        )

    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)  # Production mode
    # app_run("app:app", host=APP_HOST, port=APP_PORT, reload=True)  # Debug mode

