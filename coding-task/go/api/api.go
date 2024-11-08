package main

import (
	"fmt"
	"net/http"
	"log"
	"encoding/json"
)

// Generated by https://mholt.github.io/json-to-go/
type Ontology struct {
	Languages           []string `json:"languages"`
	Lang                string   `json:"lang"`
	OntologyID          string   `json:"ontologyId"`
	Loaded              string   `json:"loaded"`
	Updated             string   `json:"updated"`
	Status              string   `json:"status"`
	Message             string   `json:"message"`
	Version             any      `json:"version"`
	FileHash            any      `json:"fileHash"`
	LoadAttempts        int      `json:"loadAttempts"`
	NumberOfTerms       int      `json:"numberOfTerms"`
	NumberOfProperties  int      `json:"numberOfProperties"`
	NumberOfIndividuals int      `json:"numberOfIndividuals"`
	Config              struct {
		ID                     string   `json:"id"`
		VersionIri             string   `json:"versionIri"`
		Namespace              string   `json:"namespace"`
		PreferredPrefix        string   `json:"preferredPrefix"`
		Title                  string   `json:"title"`
		Description            string   `json:"description"`
		Homepage               string   `json:"homepage"`
		Version                any      `json:"version"`
		MailingList            any      `json:"mailingList"`
		Tracker                any      `json:"tracker"`
		Logo                   any      `json:"logo"`
		Creators               []any    `json:"creators"`
		Annotations            any      `json:"annotations"`
		FileLocation           string   `json:"fileLocation"`
		OboSlims               bool     `json:"oboSlims"`
		LabelProperty          string   `json:"labelProperty"`
		DefinitionProperties   []string `json:"definitionProperties"`
		SynonymProperties      []string `json:"synonymProperties"`
		HierarchicalProperties []string `json:"hierarchicalProperties"`
		BaseUris               []string `json:"baseUris"`
		HiddenProperties       []any    `json:"hiddenProperties"`
		PreferredRootTerms     []any    `json:"preferredRootTerms"`
		IsSkos                 bool     `json:"isSkos"`
		AllowDownload          bool     `json:"allowDownload"`
	} `json:"config"`
	BaseUris []string `json:"baseUris"`
	Links    struct {
		Self struct {
			Href string `json:"href"`
		} `json:"self"`
		Terms struct {
			Href string `json:"href"`
		} `json:"terms"`
		Properties struct {
			Href string `json:"href"`
		} `json:"properties"`
		Individuals struct {
			Href string `json:"href"`
		} `json:"individuals"`
	} `json:"_links"`
}

func main() {

	fmt.Println("Starting REST API on :8080")

	mux := http.NewServeMux()
	mux.HandleFunc("GET /ontologies/{onto}", getOntologyById)
	log.Fatal(http.ListenAndServe(":8080", mux))

}

func getOntologyById(w http.ResponseWriter, r *http.Request) {

	id := r.PathValue("onto")

	resp, err := http.Get("https://www.ebi.ac.uk/ols4/api/ontologies/" + id)
	
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	switch statusCode := resp.StatusCode; statusCode {
	case 200:
		var ontology Ontology
		json.NewDecoder(resp.Body).Decode(&ontology)
	
		fmt.Println(fmt.Sprintf("Title: %s", ontology.Config.Title))
		fmt.Println(fmt.Sprintf("Description: %s", ontology.Config.Description))
		fmt.Println(fmt.Sprintf("Status: %s", ontology.Status))
		fmt.Println(fmt.Sprintf("Terms: %d", ontology.NumberOfTerms))
	
		w.Header().Set("Content-Type", "application/json")
	
		data := map[string]interface{}{
			"Title": ontology.Config.Title,
			"Description": ontology.Config.Description,
			"Status": ontology.Status,
			"NumberOfTerms": ontology.NumberOfTerms,
		}
	
		json.NewEncoder(w).Encode(data)
	default:
		fmt.Fprint(w, fmt.Sprintf("Something went wrong - error code %d", statusCode))
		fmt.Println(fmt.Sprintf("Something went wrong - error code %d", statusCode))
	}

}