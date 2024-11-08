import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import models
import constants
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):

    """On application startup, check if DB exists and if not create."""

    initialise()
    yield
    logging.debug("Exiting!")

app = FastAPI(lifespan=lifespan)
logging.basicConfig(
    level = os.environ.get("logLevel", "INFO").upper()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    expose_headers = ["*"]
)

def initialise():

    """Check if DB exists and if not build the database from the model."""

    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists(constants.DB_FILEPATH):
        logging.debug('DB does not exist!')
        engine = create_engine(f"sqlite:///{constants.DB_FILEPATH}")
        models.Base.metadata.create_all(engine)

def get_session():

    """Return a session instance."""

    engine = create_engine(f"sqlite:///{constants.DB_FILEPATH}")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session 

@app.get('/ontologies/{onto}')
async def ontologies(onto: str):

    """
    Lookup ontology information using the [OLS API](https://www.ebi.ac.uk/ols4/about) and return JSON response. 
    This API has a single endpoint `ontologies/<id>`, where the `<id> parameter is taken from the ID column in [ontologies](https://www.ebi.ac.uk/ols4/ontologies).
    """

    async with httpx.AsyncClient() as client:

        try:

            r = await client.get(
                constants.ONTOLOGY_QUERY_URL.format(onto)
            )
            r.raise_for_status()
            json_data = r.json()
            results_dict = {
                "Title": json_data["config"]["title"],
                "Description": json_data["config"]["description"],
                "NumberOfTerms": json_data["numberOfTerms"],
                "Status": json_data["status"]
            }
            return JSONResponse(
                status_code=r.status_code, 
                content=results_dict
            )
        
        except KeyError as e:

            logging.error("--- KeyError ---")
            logging.error(repr(e))

            return JSONResponse(
                status_code = 500,
                content = constants.KEY_ERROR
            )

        except httpx.HTTPStatusError as e:

            logging.error("--- HTTPStatusError ---")
            logging.error(repr(e))

            return JSONResponse(
                    status_code = e.response.status_code, 
                    content = constants.HTTP_STATUS_ERROR
                )
        
        except httpx.RequestError as e:

            logging.error("--- RequestError ---")
            logging.error(repr(e))

            return JSONResponse(
                    status_code = 500, 
                    content = constants.REQUEST_ERROR
                )
