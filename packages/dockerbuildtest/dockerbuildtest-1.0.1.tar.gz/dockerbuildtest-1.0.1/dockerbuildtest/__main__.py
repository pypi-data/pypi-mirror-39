
import sys
sys.path.append("..")

"""Entry point for the application."""
#from appRoutes import app    # For application discovery by the 'flask' command.

from dockerbuildagent.appRoutes.app_view_routes import app

app.debug = True
app.port = 5000
app.run(host= '0.0.0.0')
