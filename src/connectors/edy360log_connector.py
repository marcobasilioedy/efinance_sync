import requests
import logging
import json
from constants import (
    EDY360LOG_URL,
    EMAIL_APP,
    PASSWORD_APP
)
from pathlib import Path
from typing import List, Dict, Any
from errors.custom_errors import (
    ErrorUpdatingProject,
    HttpError,
    InvalidJsonResponse,
)

logger = logging.getLogger(__name__)


class Edy360LogConnector:
    def __init__(self, url: str = EDY360LOG_URL, timeout: int = 10, error_file: str = "edy360log_errors.txt"):
        self.url = url
        self.timeout = timeout
        self.token = None
        self.error_file = Path(error_file)
        self.error_file.touch(exist_ok=True)


    def __authenticate(self) -> str:
        try:
            payload = {"email": EMAIL_APP, "password": PASSWORD_APP}

            response = requests.post(f"{self.url}/users/validate_credentials", json=payload, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token") or data.get("token")
                if not token:
                    raise ValueError("Token não encontrado na resposta da API")
                self.token = token
                return token
            else:
                raise HttpError(response.status_code, response.text)

        except Exception as e:
            logger.error(f"Erro ao obter token: {e}")
            raise
        
    def _save_error(self, payload: dict, error: str):
        try:
            with self.error_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"payload": payload, "error": error}, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Erro ao salvar log de falha: {e}")

    def update_project(self, payloads: List[Dict[str, Any]], batch_size: int = 500):

        if not self.token:
            self.__authenticate()

        headers = {"Authorization": f"Bearer {self.token}"}

        results = []

        for i in range(0, len(payloads), batch_size):
            batch = payloads[i : i + batch_size]

            for payload in batch:
                try:
                    response = requests.post(
                        f"{self.url}/backup_projects/create_backup_projects",
                        json=payload,
                        headers=headers,
                        timeout=self.timeout
                    )

                    if response.status_code != 200:
                        error_msg = f"HTTP {response.status_code} - {response.text}"
                        self._save_error(payload, error_msg)
                        raise HttpError(response.status_code, response.text)

                    try:
                        data = response.json()
                    except ValueError:
                        error_msg = "Resposta não é JSON válido"
                        self._save_error(payload, error_msg)
                        raise InvalidJsonResponse("edy360log")

                    if not data.get("Successful update"):
                        error_msg = f"Falha na atualização: {data}"
                        self._save_error(payload, error_msg)
                        raise ErrorUpdatingProject(data)

                    results.append(
                        {"contract_number": payload.get("vme_contract"), "status": "success"}
                    )

                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    logger.error(f"Falha de conexão com EDY360Log: {e}")
                    self._save_error(payload, str(e))
                    results.append(
                        {"contract_number": payload.get("vme_contract"), "status": "failed"}
                    )
                except requests.exceptions.RequestException as e:
                    logger.error(f"Erro inesperado de request: {e}")
                    self._save_error(payload, str(e))
                    results.append(
                        {"contract_number": payload.get("vme_contract"), "status": "failed"}
                    )
                except Exception as e:
                    logger.error(f"Erro ao atualizar projeto: {e}")
                    self._save_error(payload, str(e))
                    results.append(
                        {"contract_number": payload.get("vme_contract"), "status": "failed"}
                    )

        logger.info(f"{len(results)} payloads processados (API: {self.url})")
        return results
