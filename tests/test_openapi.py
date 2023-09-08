"""Get the openapi.json from the API container via NGinx proxy"""
from typing import Tuple
import logging

import requests


LOGGER = logging.getLogger(__name__)


def test_get_openapi_json(
    localmaeher_api: Tuple[str, str], openapi_version: Tuple[str, str]
) -> None:
    """Fetch openapi spec and check certain things exist"""
    url = f"{localmaeher_api[0]}/openapi.json"
    response = requests.get(url, json=None, headers=None, verify=False, timeout=2.0)
    assert response.status_code == 200
    payload = response.json()
    LOGGER.debug("payload={}".format(payload))
    assert payload["openapi"] == f"{openapi_version[0]}"
    assert payload["info"] is not None
    assert payload["info"]["title"] == "FastAPI"
    assert payload["info"]["version"] == f"{openapi_version[1]}"
    assert payload["paths"] is not None
    assert payload["paths"][f"/api/{localmaeher_api[1]}/healthcheck"] is not None
    assert payload["components"] is not None
    assert payload["components"]["schemas"] is not None
    assert payload["components"]["schemas"]["CertificatesRequest"] is not None
    assert payload["components"]["securitySchemes"] is not None
    assert payload["components"]["securitySchemes"]["JWTBearer"] is not None
