from controllers.api.order import api_order_bp
from controllers.api.client import api_client_bp
from controllers.api.medium import api_medium_bp
from controllers.api.account import api_account_bp
from controllers.api.agent import api_agent_bp


def api_register_blueprint(app):
    app.register_blueprint(api_order_bp, url_prefix='/api/order')
    app.register_blueprint(api_client_bp, url_prefix='/api/clients')
    app.register_blueprint(api_medium_bp, url_prefix='/api/mediums')
    app.register_blueprint(api_account_bp, url_prefix='/api/account')
    app.register_blueprint(api_agent_bp, url_prefix='/api/agents')
