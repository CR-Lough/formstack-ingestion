import dlt
import duckdb
from dlt.sources.helpers import requests
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator, SinglePagePaginator


def _create_auth_headers(api_secret_key):
    """Constructs Bearer type authorization header which is the most common authorization method"""
    headers = {"Authorization": f"Bearer {api_secret_key}"}
    return headers

def run_duckdb_query(query):
    with duckdb.connect('/Users/crlough/Code/ChowaCo/SCC/formstack/scc_formstack.duckdb') as conn:
        result = conn.execute(query)
        return [row[0] for row in result.fetchall()]

def transform_data_field(data):
    """
    Transforms the 'data' field from a dictionary with nested keys to a list of dictionaries.
    """
    # Transform the 'data' field to remove the outer keys
    if isinstance(data, dict):
        # Convert each key-value pair into a list of dictionaries (ignoring the key)
        return [field_info for field_id, field_info in data.items()]
    return []


@dlt.resource(write_disposition="replace", name="forms")
def forms(api_secret_key=dlt.secrets.value):
    formstack_client = RESTClient(
        base_url="https://www.formstack.com/api/v2",
        headers=_create_auth_headers(api_secret_key),
        paginator=SinglePagePaginator(),
        data_selector="forms",
    )
    for page in formstack_client.paginate(
        "/form.json?folders=false",
    ):
        yield page

@dlt.resource(write_disposition="replace", name="submissions")
def submissions(forms_list, api_secret_key=dlt.secrets.value):
    other_formstack_client = RESTClient(
        base_url="https://www.formstack.com/api/v2",
        headers=_create_auth_headers(api_secret_key),
        paginator=PageNumberPaginator(
            total_path="pages"
        ),
        data_selector="submissions",
    )
    
    for form_id in forms_list:
        print(f"Processing form_id: {form_id}...")
        for page in other_formstack_client.paginate(
            f"/form/{form_id}/submission.json?per_page=100&data=true",
        ):
            for submission in page["submissions"]:
                # Transform the 'data' field in each submission
                if "data" in submission:
                    submission["data"] = transform_data_field(submission["data"])
                yield submission

pipeline = dlt.pipeline(
    pipeline_name='scc_formstack',
    destination='duckdb',
    dataset_name='scc_formstack_data',
    import_schema_path="schemas/import",
    export_schema_path="schemas/export",
    progress=dlt.progress.tqdm(colour="yellow"),
    dev_mode=False
)

# forms data
forms_info = pipeline.run(forms())
print(forms_info)

# get the form ids as a list
query = "SELECT id FROM scc_formstack_data.forms"
forms_list = run_duckdb_query(query)

# submissions data
submissions_info = pipeline.run(submissions(forms_list))
print(submissions_info)
