from controllers.util.upload_orders import util_upload_orders_bp
from controllers.util.insert_orders import util_insert_orders_bp
from controllers.util.insert_douban_orders import util_insert_douban_orders_bp
from controllers.util.insert_framework_orders import util_insert_framework_orders_bp

def util_register_blueprint(app):
    app.register_blueprint(util_upload_orders_bp, url_prefix='/util/upload_orders')
    app.register_blueprint(util_insert_orders_bp, url_prefix='/util/insert_orders')
    app.register_blueprint(util_insert_douban_orders_bp, url_prefix='/util/insert_douban_orders')
    app.register_blueprint(util_insert_framework_orders_bp, url_prefix='/util/insert_framework_orders')
    