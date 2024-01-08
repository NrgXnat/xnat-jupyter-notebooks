from dash import Dash, html
import os

port = 8050

jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX') # /jupyterhub/user/{username}/

isJupyterLab = 'ServerApp' in os.environ.get('JUPYTERHUB_SINGLEUSER_APP','') # vs dashboard

# if running in JupyterLab, need to add proxy prefix to base URL
# e.g. /jupyterhub/user/{username}/proxy/{port}/ as expected by juptyer-server-proxy
# if running as a dashboard, jhsingle-native-proxy will use the base URL as is
if isJupyterLab:
    jupyterhub_base_url = f"{jupyterhub_base_url}proxy/{port}/"

app = Dash(
    __name__,
    requests_pathname_prefix=jupyterhub_base_url,
)

app.layout = html.Div('Hello World, from Dash')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)