from qScience import create_app
from qScience.log import enable_logging
import click
import os

'''
@click.command()
@click.option('--config', default='config/QScience.cfg', help='Configuration file of flask (default=config/easryis.cfg)')
@click.option('--database_name', default='QScience', help='The database name to be used. (default=QScience)')
@click.option('--database_port', default=27017, help='The port with the database service (default=27017)')
@click.option('--permanent_session_lifetime', default=24, help='Duration time of the session (default=24 (hours))')
'''
def init_app(**kwargs):
    
    #config = kwargs.pop('config')

    app = create_app()
    return app
    

if __name__ == '__main__':
    
    app = init_app()
        
    ssl_path = app.config['SSL_PATH']
    print os.path.join(ssl_path, "certs", "serve-nginx-selfsigned.crt")
    print os.path.join(ssl_path, "private","serve-nginx-selfsigned.key")
    app.run(host='0.0.0.0', 
            port=5000, 
            debug=True,
            threaded=True,
            ssl_context=(os.path.join(ssl_path, "certs", "serve-nginx-selfsigned.crt"),
                         os.path.join(ssl_path, "private","serve-nginx-selfsigned.key")
                         )
          )
    
    app.toolbar.init_app(app)