import asyncio
import logging
from connectors import EfinanceConnector, Edy360LogConnector
from utils import GetToken, normalize_string
from errors.custom_errors import NotFoundToken
from constants import STORES

logger = logging.getLogger(__name__)

class ProjectsController:
    def __init__(self, batch_size: int = 500):
        self.efinance_connector = EfinanceConnector()
        self.edy360log_connector = Edy360LogConnector()
        self.get_token = GetToken()
        self.batch_size = batch_size

    async def _process_project(self, token: str, project: dict):
        contract_number = project["VME_Contrato"].split("-")[0]
        order_number = project["VME_Cliente"]
        store = STORES.get(int(project["VME_Loja"]))

        environments_data, reservations_data = [], []

        try:
            environments_data = await self.efinance_connector.get_environments(
                token=token,
                order_number=order_number,
                contract_number=contract_number,
                store=project["VME_Loja"]
            )
        except Exception as e:
            logger.warning(f"Failed to fetch environments for {contract_number}: {e}")

        try:
            reservations_data = await self.efinance_connector.get_reservations(
                token=token,
                order_number=order_number,
                contract_number=contract_number,
                store=project["VME_Loja"]
            )
        except Exception as e:
            logger.warning(f"Failed to fetch reservations for {contract_number}: {e}")

        environments, description, env_codes, lines = [], [], [], []
        for env in environments_data:
            environments.append(normalize_string(env.get("environment", "")))
            description.append(env.get("description", ""))
            env_codes.append(env.get("env_code", ""))
            lines.append(env.get("line", ""))

        unit_values, total_values, amounts = [], [], []
        for res in reservations_data:
            unit_values.append(res.get("unit_value", 0))
            total_values.append(res.get("total_value", 0))
            amounts.append(res.get("amount", 0))
            
        payload = {
            "cash_without_indicator": [project["AvistaSemIndicador"]],
            "contract_signature_date": project["CAS_DataAssinatura"],
            "client_signature_date": project["CAS_DataAssinaturaCliente"],
            "factory_code": [project["CLI_CodigoFabrica"]],
            "client_phone1": project["CLI_CorFone1"],
            "client_phone2": project["CLI_CorFone2"],
            "client_registration_date": project["CLI_DataCadastro"],
            "client_email": project["CLI_Email"],
            "client_building_entrance": project["CLI_EntEdificio"], 
            "client_name": project["CLI_Nome"],
            "referral_description": [project["CPR_Descricao"]],
            "conclusion_date": project["CTAG_DataConclusao"],
            "linked_contract": project["ContratoVinculado"],
            "description": [project["DFB_Descricao"]],
            "direct_sale_type": project["DFB_TipoVendaDireta"],
            "release_date": project["DataLiberacao"],
            "score_release_date": project["DataPontuacaoLiberada"],
            "request_date": project["DataSolicitacao"],
            "days_delay": project["DiasAtraso"],
            "order_days": project["DiasPedido"],
            "financial_difference": project["DifFinanceira"],
            "equipment_code": project["EQP_Codigo"],
            "equipment_initial": project["EQP_Sigla"],
            "overflow": project["Estouro"],
            "sale_overflow": project["EstouroVenda"],
            "ef_client_name": project["FAB_NomeClienteEfinance"],
            "credit_analysis_model": project["FIN_AnaliseCreditoModelo"],
            "finance_description": project["FIN_Descricao"],
            "payment_form": project["FP"],
            "store_order_limit_days": project["LOJ_DiasLimitePedido"],
            "financial_proposal_list": project["ListaFinanceiraPropostas"],
            "exclusion_reason": project["MotivoExclusao"],
            "approved_by": project["NomeUsuarioAprovou"],
            "requested_by": project["NomeUsuarioSolicitou"],
            "fabric_order": project["PRF_Pedido_Fab"],
            "factory_description": project["PRO_DescFabrica"],
            "delivery_time": project["PRO_HoraEntrega"],
            "total_term_without_reservation": project["PRO_TotalPrazoSemReserva"],
            "supplier_value_without_score": project["PRO_ValorFornecedorSemPontuacao"],
            "erp_orders": project["PedidosERP"],
            "score": project["Pontuacao"],
            "released_score": project["PontuacaoLiberada"],
            "base_proposal": project["ProBase"],
            "sold_score_project": project["ProjetoPontuacaoVendido"],
            "projects_count": project["Projetos"],
            "projects_sent": project["ProjetosEnviados"],
            "installment_quantity": project["QtdeParcelas"],
            "shipping_notes": project["Romaneios"],
            "se_flag": project["SE"],
            "factory_shipping_status": [project["SituacaoEnvioFabrica"]],
            "sync1": project["Sync1"],
            "sync2": project["Sync2"],
            "sync3": project["Sync3"],
            "sync_folder1": project["Sync_Pasta1"],
            "sync_folder2": project["Sync_Pasta2"],
            "sync_folder3": project["Sync_Pasta3"],
            "financial_proposal_tooltip": project["ToolTipFinanceiraPropostas"],
            "total_indicator": project["TotalIndicador"],
            "total_reservation": project["TotalReserva"],
            "user_code": project["USU_Codigo"],
            "user_name": project["USU_Nome"],
            "assumed_user": project["UsuarioAssumido"],
            "user_score_released": project["UsuarioPontuacaoLiberada"],
            "user_score_requested": project["UsuarioPontuacaoSolicitada"],
            "responsible_user": project["UsuarioResponsavel"],
            "vme_change": project["VME_Alteracao"],
            "vme_authorization": project["VME_Autorizacao"],
            "vme_client": order_number,
            "vme_security_code": project["VME_CodigoSeguranca"],
            "vme_condition": project["VME_Condicao"],
            "vme_contract": contract_number,
            "vme_contract_version": project["VME_ContratoVersao"],
            "vme_change_date": project["VME_DataAlterado"],
            "vme_programming_available_date": project["VME_DataDisponivelProgramacao"],
            "vme_delivery_date": project["VME_DataEntrega"],
            "vme_partial_fin_date": project["VME_DataFINParcial"],
            "vme_release_date": project["VME_DataLiberacao"],
            "vme_factory_order_date": project["VME_DataPedidoFabrica"],
            "vme_shipping_note_date": project["VME_DataRomaneio"],
            "vme_sale_date": project["VME_DataVenda"],
            "vme_company": project["VME_Emp"],
            "vme_delivery_neighborhood": project["VME_EntBairro"],
            "vme_delivery_zipcode": project["VME_EntCep"],
            "vme_delivery_city": project["VME_EntCidade"],
            "vme_delivery_address": project["VME_EntEndereco"],
            "vme_delivery_state": project["VME_EntEstado"],
            "vme_ws_send": project["VME_Envio_WS"],
            "vme_ws_fail": project["VME_Falha_WS"],
            "vme_finance": project["VME_Financeira"],
            "vme_store": [store],
            "vme_finance_score": project["VME_PontuacaoFIN"],
            "vme_indicator_percent": project["VME_PorcIndicador"],
            "vme_shipping_note_final": project["VME_RomaneioF"],
            "vme_shipping_note_initial": project["VME_RomaneioI"],
            "vme_type": project["VME_Tipo"],
            "vme_sale_type": project["VME_TipoVenda"],
            "vme_total_cost": project["VME_TotalCusto"],
            "vme_user_registration": project["VME_UserCadastro"],
            "vme_user_team": project["VME_UserEquipe"],
            "vme_user_responsible": project["VME_UserResponsavel"],
            "vme_cash_value": project["VME_ValorAvista"],
            "vme_sale_value": project["VME_ValorVenda"],
            "vme_sale_canceled": project["VME_VendaCancelada"],
            "vme_version": project["VME_Versao"],
            "original_contract": project["VVC_ContratoOriginal"],
            "original_contract_link_date": project["VVC_DataVinculoContratoOriginal"],
            "addendum_tooltip": project["tooltipAdendo"],
            "dle_tooltip": project["tooltipDLE"],
            "assumed_user_tooltip": project["tooltipUsuarioAssumido"],
            "env_codes": env_codes,
            "environments": [
                {"environment": env, "description": desc} 
                for env, desc in zip(environments, description)
            ],

            "lines": lines,
            "unit_values": unit_values,
            "total_values": total_values,
            "amounts": amounts
        }

        return payload

    async def get_projects(self):
        token = self.get_token.get_token()
        if not token:
            raise NotFoundToken()

        projects = await self.efinance_connector.get_projects(token)

        tasks = [self._process_project(token, p) for p in projects]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        payloads = [r for r in results if isinstance(r, dict)]

        self.edy360log_connector.update_project(payloads, batch_size=self.batch_size)

        return [{"status": "success", "contract_number": p["vme_contract"]} for p in payloads]

