from sap_cloud_sdk.aicore import set_aicore_config

set_aicore_config()

import logging
import os

import click
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from sap_cloud_sdk import bootstrap
from starlette.middleware.base import BaseHTTPMiddleware

from agent_executor import AgentExecutor
from mcp_providers.agw import set_user_token, reset_user_token
from instrumentation import get_metrics_summary, log_m3_achieved
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))


@click.command()
@click.option("--host", default=HOST)
@click.option("--port", default=PORT)
def main(host: str, port: int):
    skill = AgentSkill(
        id="hr-information-agent",
        name="hr-information-agent",
        description="An AI-powered HR self-service assistant that answers employee questions about HR policies, leave rules, and benefits, and retrieves personal HR data from SAP SuccessFactors to reduce helpdesk tickets by 30%.",
        tags=["hr", "information", "agent", "successfactors", "self-service"],
        examples=["How many days of annual leave do I have left?", "What is the company bereavement leave policy?"],
    )
    agent_card = AgentCard(
        name="hr-information-agent",
        description="An AI-powered HR self-service assistant that answers employee questions about HR policies, leave rules, and benefits, and retrieves personal HR data from SAP SuccessFactors to reduce helpdesk tickets by 30%.",
        url=os.environ.get("AGENT_PUBLIC_URL", f"http://{host}:{port}/"),
        version="1.0.0",
        default_input_modes=["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True, push_notifications=False),
        skills=[skill],
    )
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=DefaultRequestHandler(
            agent_executor=AgentExecutor(),
            task_store=InMemoryTaskStore(),
        ),
    )
    app = server.build()

    # Add metrics endpoint for ticket deflection tracking (R8)
    async def metrics_endpoint(request: Request) -> JSONResponse:
        return JSONResponse(get_metrics_summary())

    app.routes.append(Route("/metrics/summary", metrics_endpoint, methods=["GET"]))

    class JWTContextMiddleware(BaseHTTPMiddleware):
        """Extracts JWT token from Authorization header and sets it in context."""

        async def dispatch(self, request, call_next):
            auth_header = request.headers.get("authorization", "")
            token = auth_header[7:] if auth_header.lower().startswith("bearer ") else None
            token_ctx = set_user_token(token)
            try:
                response = await call_next(request)
                if token:
                    log_m3_achieved()
                return response
            finally:
                reset_user_token(token_ctx)

    app.add_middleware(JWTContextMiddleware)

    bootstrap(app)

    logger.info(f"Starting A2A server at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter  # type: ignore[call-arg]
