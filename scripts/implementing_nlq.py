from openai import OpenAI
from llama_index.core import Document, VectorStoreIndex
import json

# Initialize OpenAI API with your key
llm_client = OpenAI()

# Define the static data for Northern and Southern California
static_data = {
    "states": [
        {
            "name": "Northern California",
            "code": "N-CA",
            "bounding_box": {
                "min_latitude": 36.7783,  # Lower boundary of Northern California
                "max_latitude": 42.0095,  # Northern boundary of the state
                "min_longitude": -124.4096,  # Western boundary of the state
                "max_longitude": -119.4179  # Eastern boundary of Northern California
            },
            "agencies": [
                {
                    "id": "unitrans",
                    "name": "Unitrans",
                    "bounding_box": {
                        "min_latitude": 38.533043,
                        "max_latitude": 38.560875,
                        "min_longitude": -121.78493,
                        "max_longitude": -121.71184
                    },
                    "routes": [
                        {"tag": "A", "name": "Route A"},
                        {"tag": "B", "name": "Route B"},
                    ],
                    "vehicles": [
                        {"id": "LMU_4000", "route": "A"},
                        {"id": "LMU_4001", "route": "B"},
                    ]
                }
            ]
        },
        {
            "name": "Southern California",
            "code": "S-CA",
            "bounding_box": {
                "min_latitude": 32.5343,  # Southern boundary of the state
                "max_latitude": 36.7783,  # Lower boundary of Northern California
                "min_longitude": -124.4096,  # Western boundary of the state
                "max_longitude": -114.1312  # Eastern boundary of Southern California
            },
            "agencies": [
                {
                    "id": "lametro",
                    "name": "LA Metro",
                    "bounding_box": {
                        "min_latitude": 34.052235,
                        "max_latitude": 34.052235,
                        "min_longitude": -118.243683,
                        "max_longitude": -118.243683
                    },
                    "routes": [
                        {"tag": "Blue", "name": "Blue Line"},
                        {"tag": "Red", "name": "Red Line"},
                    ],
                    "vehicles": [
                        {"id": "LACMTA_100", "route": "Blue"},
                        {"id": "LACMTA_101", "route": "Red"},
                    ]
                },
                {
                    "id": "glendale",
                    "name": "Glendale Beeline",
                    "bounding_box": {
                        "min_latitude": 34.142507,
                        "max_latitude": 34.159913,
                        "min_longitude": -118.245004,
                        "max_longitude": -118.226487
                    },
                    "routes": [
                        {"tag": "1", "name": "Route 1"},
                        {"tag": "2", "name": "Route 2"},
                    ],
                    "vehicles": [
                        {"id": "GLN_500", "route": "1"},
                        {"id": "GLN_501", "route": "2"},
                    ]
                }
            ]
        }
    ]
}


# Function to create a document for each static data entry, with relationships
def create_documents(data):
    documents = []

    for state in data["states"]:
        # Create a document for each state
        state_json = json.dumps({
            "State": state["name"],
            "Code": state["code"],
            "BoundingBox": state["bounding_box"],
            "Agencies": [agency["id"] for agency in state["agencies"]]
        }, indent=4)

        state_doc = Document(text=state_json, metadata={"type": "state", "code": state["code"]})
        documents.append(state_doc)

        for agency in state["agencies"]:
            # Create a document for each agency within the state
            agency_json = json.dumps({
                "Agency": agency["name"],
                "ID": agency["id"],
                "BoundingBox": agency["bounding_box"],
                "State": state["name"],
                "Routes": [route["tag"] for route in agency["routes"]],
                "Vehicles": [vehicle["id"] for vehicle in agency["vehicles"]]
            }, indent=4)

            agency_doc = Document(text=agency_json,
                                  metadata={"type": "agency", "id": agency["id"], "state": state["name"]})
            documents.append(agency_doc)

    return documents


# Initialize a vector store
documents = create_documents(static_data)

# Build the index using the documents
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Query function to demonstrate usage
def query_static_data(query):
    results = query_engine.query(query)
    return results


# Example query: "What are the agencies in Northern California?"
query_result = query_static_data("What are the agencies in Northern California?")
print(query_result)


# Query function to retrieve context from LlamaIndex
def query_static_data_combined(query):
    # Retrieve context from Northern and Southern California
    result_n_ca = query_engine.query("What are the agencies in Northern California?")
    result_s_ca = query_engine.query("What are the agencies in Southern California?")

    # Combine the results (assuming 'result_n_ca' and 'result_s_ca' contain lists of results)
    return result_n_ca.response + result_s_ca.response  # Assuming result_n_ca and result_s_ca are lists


# Example user query
user_query = "What is the average speed of vehicles in Northern California?"

# Query combined results for N-CA and S-CA
context_result = query_static_data_combined(user_query)


# Query with OpenAI's updated API using the combined context
def query_with_openai(user_query, context):
    prompt = f"""
    You are an AI agent managing a streaming API for transit data. Based on the following user query and context, you need to 
    determine the correct web agent (country, state, agency, or vehicle) and the appropriate lane to query.
    All states are represented by their two-letter state code except California, which is split into N-CA and S-CA.

    Context: {context}

    User Query: {user_query}

    The Web Agents are:
    - Country: /country/:id (e.g., /country/US)
    - State: /state/:country/:state (e.g., /state/US/N-CA and /state/US/S-CA for California)
    - Agency: /agency/:country/:state/:id (e.g., /agency/US/N-CA/unitrans)
    - Vehicle: /vehicle/:country/:state/:agency/:id (e.g., /vehicle/US/S-CA/west-hollywood/116)

    Your job is to output a JSON object with the nodeUri and laneUri for the correct agent and lane based on the user query. 
    Example response: {{"nodeUri": "/agency/US/N-CA/unitrans", "laneUri": "vehicles"}}
    """

    # Call OpenAI API for response
    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant for managing a streaming API."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()  # Fixed API response access


# Example usage of OpenAI function
response = query_with_openai(user_query, context_result)
print(response)
