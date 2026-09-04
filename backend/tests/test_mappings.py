from fastapi.testclient import TestClient


def upload(client: TestClient, csv: str, name: str = "mapping.csv") -> dict:
    response = client.post("/api/v1/sources/upload", files={"file": (name, csv.encode(), "text/csv")})
    assert response.status_code == 201
    return response.json()


def suggestions(client: TestClient, source: dict) -> dict:
    dataset_id = source["dataset"]["id"]
    response = client.post(f"/api/v1/datasets/{dataset_id}/mappings/suggest")
    assert response.status_code == 200
    return response.json()


def by_column(payload: dict) -> dict:
    return {item["source_column"]["name"]: item for item in payload["mappings"]}


def test_exact_alias_type_and_ambiguity_rules(client: TestClient) -> None:
    source = upload(client, "customer_id,cust_id,client_id,order_date,amount,revenue_notes\nC1,C1,C1,2026-01-01,10,internal note\nC2,C2,C2,2026-01-02,20,follow up\n")
    mapped = by_column(suggestions(client, source))
    for name in ("customer_id", "cust_id", "client_id"):
        assert mapped[name]["canonical_field"]["code"] == "CUSTOMER_ID"
        assert mapped[name]["confidence_level"] == "HIGH"
    assert mapped["order_date"]["canonical_field"]["code"] == "ORDER_DATE"
    assert mapped["order_date"]["confidence_level"] == "HIGH"
    assert mapped["amount"]["status"] in {"NEEDS_REVIEW", "UNMAPPED"}
    assert mapped["amount"]["status"] != "CONFIRMED"
    assert mapped["revenue_notes"]["canonical_field"] is None or mapped["revenue_notes"]["confidence_level"] != "HIGH"


def test_order_context_strengthens_sales_amount(client: TestClient) -> None:
    contextual = upload(client, "order_id,order_date,sales_amount\nA1,2026-01-01,100\nA2,2026-01-02,120\n", "context.csv")
    isolated = upload(client, "sales_amount\n100\n120\n", "isolated.csv")
    context_map = by_column(suggestions(client, contextual))["sales_amount"]
    isolated_map = by_column(suggestions(client, isolated))["sales_amount"]
    assert context_map["canonical_field"]["code"] == "NET_REVENUE"
    assert context_map["confidence"] > isolated_map["confidence"]
    assert context_map["status"] == "NEEDS_REVIEW"
    assert any("order identifier" in item["message"] for item in context_map["evidence"])


def test_override_confirmation_rejection_and_version_lineage(client: TestClient) -> None:
    source = upload(client, "sales,customer_id\n100,C1\n120,C2\n")
    payload = suggestions(client, source)
    mapped = by_column(payload)
    catalog = client.get("/api/v1/canonical-fields").json()
    net_revenue = next(item for item in catalog if item["code"] == "NET_REVENUE")
    sales = mapped["sales"]
    response = client.post(f"/api/v1/mappings/{sales['id']}/confirm", json={"canonical_field_id": net_revenue["id"]})
    assert response.status_code == 200
    confirmed = response.json()
    assert confirmed["status"] == "CONFIRMED"
    assert confirmed["canonical_field"]["code"] == "NET_REVENUE"
    assert confirmed["mapping_method"] == "USER" and confirmed["confirmed_by_user"] is True
    customer = mapped["customer_id"]
    rejected = client.post(f"/api/v1/mappings/{customer['id']}/reject").json()
    assert rejected["status"] == "REJECTED"
    dataset_id = source["dataset"]["id"]
    persisted = by_column(client.get(f"/api/v1/datasets/{dataset_id}/mappings").json())
    assert persisted["sales"]["status"] == "CONFIRMED"
    assert persisted["customer_id"]["status"] == "REJECTED"
    assert all(item["dataset_version_id"] == source["latest_version"]["id"] for item in persisted.values())


def test_leave_unmapped_persists(client: TestClient) -> None:
    source = upload(client, "mystery\nalpha\nbeta\n")
    mapping = suggestions(client, source)["mappings"][0]
    response = client.patch(f"/api/v1/mappings/{mapping['id']}", json={"status": "UNMAPPED"})
    assert response.status_code == 200
    assert response.json()["status"] == "UNMAPPED" and response.json()["canonical_field"] is None
