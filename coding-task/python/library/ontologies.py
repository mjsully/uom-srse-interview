import os
import logging
import constants
import httpx
import argparse 
import pprint

logging.basicConfig(
    level = os.environ.get("logLevel", "INFO").upper()
)

def main():

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--onto")
    args = argparser.parse_args()
    pprint.pp(get_ontology_info(args.onto))

def get_ontology_info(onto: str):

    """
    Lookup ontology information using the [OLS API](https://www.ebi.ac.uk/ols4/about) and return JSON response. 
    This API has a single endpoint `ontologies/<id>`, where the `<id> parameter is taken from the ID column in [ontologies](https://www.ebi.ac.uk/ols4/ontologies).
    """

    try:

        r = httpx.get(
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
        return results_dict
    
    except KeyError as e:

        logging.error("--- KeyError ---")
        logging.error(repr(e))

        return constants.KEY_ERROR

    except httpx.HTTPStatusError as e:

        logging.error("--- HTTPStatusError ---")
        logging.error(repr(e))

        return constants.HTTP_STATUS_ERROR
    
    except httpx.RequestError as e:

        logging.error("--- RequestError ---")
        logging.error(repr(e))

        return constants.REQUEST_ERROR

if __name__ == "__main__":
    main()