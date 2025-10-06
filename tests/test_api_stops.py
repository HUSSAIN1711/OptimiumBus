from typing import Dict

def test_create_bus_stop_success(client):
    # Arrange
    payload: Dict = {
        "name": "Main & Center",
        "description": "Central stop",
        "latitude": 33.6846,
        "longitude": -117.8265,
        "demand_weight": 0.7
    }

    # Act
    response = client.post("/api/v1/stops/", json=payload, params={"snap_to_road": False})

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["name"] == payload["name"]
    assert abs(data["latitude"] - payload["latitude"]) < 1e-6
    assert abs(data["longitude"] - payload["longitude"]) < 1e-6
    assert data["demand_weight"] == payload["demand_weight"]


def test_create_bus_stop_invalid_data(client):
    # Arrange: missing longitude
    payload: Dict = {
        "name": "Invalid Stop",
        "latitude": 33.68,
        # "longitude": -117.82,  # intentionally omitted
        "demand_weight": 0.5
    }

    # Act
    response = client.post("/api/v1/stops/", json=payload, params={"snap_to_road": False})

    # Assert
    assert response.status_code == 422
