from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends,Query,Response,status

from app.dependencies import obter_tarefa_servico
from app.enums import CampoOrdenacao,Ordem,PrioridadeTarefa,StatusTarefa,Prioridade
from app.repositories import FiltroDeTarefas
from app.schemas import TarefaCreate,TarefaUpdate,TarefaOut
from app.services import AlteracoesDaTarefa,TarefaServico

router = APIRouter(prefix="/tarefas",tags=["Tarefas"])

@router.post(
    "",
    response_model=TarefaOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Tarefa",
    responses={404: {"description": "Usuario Não Encontrado"}},
)
def criar_tarefa(
    dados: TarefaCreate,
    servico: Annotated[TarefaServico, Depends(obter_tarefa_servico)],
) -> TarefaServico:
    """Cadastra um novo usuário com a senha armazenada como hash."""
    return servico.criar(usuario_id=dados.usuario_id,
titulo=dados.titulo,
prioridade=dados.prioridade,
prazo=dados.prazo
    )
def _montar_alteracoes(dados:TarefaUpdate) -> AlteracoesDaTarefa:
    return AlteracoesDaTarefa(**dados.model_dump(exclude_unset=True))
@router.post(
    "/{tarefa_id}",
    status_code= status.HTTP_204_NO_CONTENT,
    response_model=TarefaOut,
    summary="Atualizar Tarefa",
    responses={404: {"description": "Tarefa Não Encontrada"}},
)
def remover_tarefa(
    tarefa_id:int,
    servico: Annotated[TarefaServico, Depends(obter_tarefa_servico)],
) -> Response:
    """Cadastra um novo usuário com a senha armazenada como hash."""
    return servico.remover(tarefa_id)
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.get(
    "",
    response_model=list[TarefaOut],
    summary="Criar Tarefa",
   
)
def listar_tarefa(
    servico: Annotated[TarefaServico, Depends(obter_tarefa_servico)],
    usuario_id: Annotated[
        int,Query(alias="usuario_id",description="ID do usuario")
    ],
    status_tarefa:Annotated[
        StatusTarefa | None,Query(alias="status")
    ]=None,
    prioridade: Annotated[
    Prioridade | None,
    Query(alias="prioridade")
] = None,
    prazo_ate: Annotated[
    date | None,
    Query(
        alias="prazoAte",
        description="Somente tarefas com o prazo até esta data"
    )
] = None,
ordem:Annotated[
    Ordem,Query()
]= Ordem.DESC,
limite: Annotated [int,Query(ge=1,le=200,alias="limit")]=50,
deslocamento: Annotated[int,Query(ge=0,alias="offset")]=0,
ordenar_por: Annotated[
    CampoOrdenacao,
    Query(alias="ordenar_por")
] = CampoOrdenacao.CRIADO_EM,
) -> list[TarefaOut]:
    filtro=FiltroDeTarefas(
        usuario_id=usuario_id,
        status=status_tarefa,
        prioridade=prioridade,
        prazo_ate=prazo_ate,
        ordem=ordem,
        limite=limite,
        deslocamento=deslocamento,
        ordenar_por=ordenar_por
    )
    return servico.listar(filtro)

