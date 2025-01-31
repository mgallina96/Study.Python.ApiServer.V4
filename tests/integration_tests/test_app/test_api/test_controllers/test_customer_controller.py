import pytest
from fastapi import status
from fastapi.testclient import TestClient

from system.database.session import DatabaseSession
from system.database.settings import DatabaseId
from utils.assertions import assert_api_error_format
from utils.queries import execute_raw_queries
from utils.uuids import mock_uuid


class TestGetAll:
    ENDPOINT = "/api/v4/customers"

    @pytest.fixture(scope="function", autouse=True)
    def reset_data(self):
        with DatabaseSession.get(DatabaseId.MAIN) as session:
            execute_raw_queries(session, "TRUNCATE TABLE main.customer CASCADE")
            session.commit()

    def test_ok(self, client: TestClient):
        # Arrange
        with DatabaseSession.get(DatabaseId.MAIN) as session:
            execute_raw_queries(
                session,
                f"""INSERT INTO main.customer (id, name, email, phone, address) 
                    VALUES ('{mock_uuid(1)}', 'test_customer', 'test_email', 'test_phone', 'test_address'),
                           ('{mock_uuid(2)}', 'test_customer2', 'test_email2', 'test_phone2', 'test_address2')""",
            )
            session.commit()

        # Act
        response = client.get(self.ENDPOINT)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "data": [
                {
                    "id": mock_uuid(1),
                    "name": "test_customer",
                    "email": "test_email",
                    "phone": "test_phone",
                    "address": "test_address",
                },
                {
                    "id": mock_uuid(2),
                    "name": "test_customer2",
                    "email": "test_email2",
                    "phone": "test_phone2",
                    "address": "test_address2",
                },
            ],
            "meta": {"count": 2},
        }

    def test_no_values(self, client: TestClient):
        # Arrange
        # Act
        response = client.get(self.ENDPOINT)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "data": [],
            "meta": {"count": 0},
        }


class TestGet:
    ENDPOINT = "/api/v4/customers/{customer_id}"

    @pytest.fixture(scope="function", autouse=True)
    def reset_data(self):
        with DatabaseSession.get(DatabaseId.MAIN) as session:
            execute_raw_queries(session, "TRUNCATE TABLE main.customer CASCADE")
            session.commit()

    def test_ok(self, client: TestClient):
        # Arrange
        with DatabaseSession.get(DatabaseId.MAIN) as session:
            execute_raw_queries(
                session,
                f"""INSERT INTO main.customer (id, name, email, phone, address) 
                            VALUES ('{mock_uuid(1)}', 'test_customer', 'test_email', 'test_phone', 'test_address'),
                                   ('{mock_uuid(2)}', 'test_customer2', 'test_email2', 'test_phone2', 'test_address2')""",
            )
            session.commit()

        # Act
        response = client.get(self.ENDPOINT.format(customer_id=mock_uuid(1)))

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "data": {
                "id": mock_uuid(1),
                "name": "test_customer",
                "email": "test_email",
                "phone": "test_phone",
                "address": "test_address",
            },
        }

    def test_not_found(self, client: TestClient):
        # Arrange
        with DatabaseSession.get(DatabaseId.MAIN) as session:
            execute_raw_queries(
                session,
                f"""INSERT INTO main.customer (id, name, email, phone, address) 
                            VALUES ('{mock_uuid(1)}', 'test_customer', 'test_email', 'test_phone', 'test_address'),
                                   ('{mock_uuid(2)}', 'test_customer2', 'test_email2', 'test_phone2', 'test_address2')""",
            )
            session.commit()

        # Act
        response = client.get(self.ENDPOINT.format(customer_id=mock_uuid(3)))

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert_api_error_format(response)
