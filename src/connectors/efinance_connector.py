import httpx
import js2py
from constants import URL
from errors.custom_errors import ErrorGetProjects

class EfinanceConnector:
    def __init__(self, async_mode: bool = False):
        self.async_mode = async_mode

    def extract_data(self, raw_js_text):
        try:
            context = js2py.EvalJs()
            context.execute(f"var response = {raw_js_text};")
            dados_js = context.response["dados"]
            return dados_js.to_list()
        except Exception as e:
            print(f"Error extracting JS data: {e}")
            raise ErrorGetProjects() from e

    async def get_projects(self, token: str) -> list[dict]:
        try:
            data = {
                "start": "0",
                "limit": "100",
                "Acao": "carregaGrid",
                "filtroPeriodo": "-1",
                "loja": "172",
                "equipe": "0",
                "usuario": "-1",
                "finVenda": "-1",
                "statusContratos": "0",
                "procedencia": "-1",
                "fornecedor": "-1",
                "tipoContrato": "9999",
                "codEmpresa": "0",
                "Loja": "0",
                "filtroDataDe": "2023-01-01",
                "filtroDataAte": "2025-08-27"
            }

            efinance_url = f"{URL}/(S({token}))/comercial/gerenciamento_comercial.aspx"

            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(efinance_url, data=data)
                response.raise_for_status()

            return self.extract_data(response.text)

        except Exception as e:
            print(f"Error getting projects: {e}")
            raise ErrorGetProjects() from e

    async def get_environments(self, token: str, order_number: str, contract_number: str) -> list[dict]:
        try:
            data = {
                "Acao": "carregaGrid",
                "loja": "172",
                "cliente": order_number,
                "contrato": contract_number,
            }

            efinance_url = f"{URL}/(S({token}))/cadastros/cad_projetos.aspx"

            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(efinance_url, data=data)
                response.raise_for_status()

            raw_data = self.extract_data(response.text)

            return [
                {
                    "env_code": item.get("PRO_Opcao"),
                    "environment": item.get("LSI_Descricao"),
                    "line": item.get("PRO_Linha"),
                }
                for item in raw_data
            ]

        except Exception as e:
            print(f"Error getting environments: {e}")
            raise ErrorGetProjects() from e

    async def get_reservations(self, token: str, order_number: str, contract_number: str) -> list[dict]:
        try:
            data = {
                "acao": "carregaGridReserva",
                "cliente": order_number,
                "loja": "172",
                "contrato": contract_number,
                "Acao": "carregaGrid",
            }

            efinance_url = f"{URL}/(S({token}))/posVenda/historico_pos_venda.aspx"

            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(efinance_url, data=data)
                response.raise_for_status()

            raw_data = self.extract_data(response.text)

            return [
                {
                    "unit_value": item.get("RES_Unitario"),
                    "total_value": item.get("RES_Total"),
                    "amount": item.get("RES_Qtde"),
                }
                for item in raw_data
            ]

        except Exception as e:
            print(f"Error getting reservations: {e}")
            raise ErrorGetProjects() from e
