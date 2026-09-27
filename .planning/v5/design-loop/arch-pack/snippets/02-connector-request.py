from datetime import date

from gridflow.connectors.elexon.endpoints import ENDPOINTS, build_params

endpoint = ENDPOINTS["system_prices"]
path = f"{endpoint.path}/{date(2026, 9, 8).isoformat()}"
print(path, build_params(endpoint, page=1))
