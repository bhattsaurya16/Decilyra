from fastapi.testclient import TestClient

CSV = b"order_id,order_date,amount,description,region\n1,2026-01-01,10.50,First order,North\n2,2026-01-02,20.00,Second order,South\n2,2026-01-02,20.00,Second order,South\n3,2026-01-03,,Third order,North\n"

def upload(client: TestClient, content: bytes = CSV, name: str = "orders.csv"):
    return client.post("/api/v1/sources/upload", files={"file": (name, content, "text/csv")})

def test_successful_upload_profile_preview_and_retrieval(client: TestClient) -> None:
    response = upload(client); assert response.status_code == 201
    source = response.json(); version = source["latest_version"]
    assert version["row_count"] == 4 and version["column_count"] == 5 and version["duplicate_row_count"] == 1
    assert "storage_key" not in str(source)
    assert client.get("/api/v1/sources").json()[0]["id"] == source["id"]
    assert client.get(f"/api/v1/sources/{source['id']}").status_code == 200
    dataset_id = source["dataset"]["id"]
    assert client.get(f"/api/v1/datasets/{dataset_id}").status_code == 200
    assert len(client.get(f"/api/v1/datasets/{dataset_id}/versions").json()) == 1
    detail = client.get(f"/api/v1/datasets/{dataset_id}/versions/{version['id']}").json()
    columns = {item["name"]: item for item in detail["columns"]}
    assert columns["order_id"]["inferred_type"] == "integer" and columns["order_id"]["generic_role"] == "possible_id"
    assert columns["order_date"]["inferred_type"] == "date"
    assert columns["amount"]["inferred_type"] == "decimal"
    assert columns["description"]["inferred_type"] == "text"
    assert columns["amount"]["profile"]["null_percentage"] == 25.0
    assert "duplicate_rows" in {issue["code"] for issue in detail["quality_issues"]}
    assert client.get(f"/api/v1/datasets/{dataset_id}/versions/{version['id']}/profile").status_code == 200
    preview = client.get(f"/api/v1/datasets/{dataset_id}/preview?limit=2").json()
    assert len(preview["rows"]) == 2 and preview["rows"][0]["order_id"] == 1

def test_invalid_extension_empty_and_malformed_csv(client: TestClient) -> None:
    assert upload(client, CSV, "orders.txt").status_code == 415
    assert upload(client, b"", "empty.csv").status_code == 422
    assert upload(client, b'a,b\n1,"unterminated\n', "bad.csv").status_code == 422

def test_header_only_csv_records_empty_dataset(client: TestClient) -> None:
    response = upload(client, b"id,name\n"); assert response.status_code == 201
    dataset_id = response.json()["dataset"]["id"]; version_id = response.json()["latest_version"]["id"]
    detail = client.get(f"/api/v1/datasets/{dataset_id}/versions/{version_id}").json()
    assert detail["row_count"] == 0
    assert "empty_dataset" in {issue["code"] for issue in detail["quality_issues"]}

def test_delete_removes_source(client: TestClient) -> None:
    source = upload(client).json()
    assert client.delete(f"/api/v1/sources/{source['id']}").status_code == 204
    assert client.get(f"/api/v1/sources/{source['id']}").status_code == 404
