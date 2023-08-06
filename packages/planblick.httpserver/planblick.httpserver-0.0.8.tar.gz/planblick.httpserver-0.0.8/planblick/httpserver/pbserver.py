import os
import cherrypy
from inspect import getframeinfo, stack


class Server:

    def start(self, flask_app, static_dir=None, static_path=None):
        # Mount the application
        cherrypy.tree.graft(flask_app, "/")

        class Static(object):
            pass

        if static_dir is not None and static_path is None:
            static_path = static_dir
        if static_dir is not None and static_path is not None:
            # Add static file serving to enable swagger GUI
            caller = getframeinfo(stack()[1][0])
            PATH = os.path.abspath(os.path.dirname(caller.filename))
            cherrypy.tree.mount(Static(), static_path, config={
                '/': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': PATH + static_dir,
                    'tools.staticdir.index': 'index.html',
                }
            })

        # Unsubscribe the default server
        cherrypy.server.unsubscribe()

        # Instantiate a new server object
        server = cherrypy._cpserver.Server()

        # Configure the server object
        server.socket_host = "0.0.0.0"
        server.socket_port = 8000
        server.thread_pool = 30

        # Subscribe this server
        server.subscribe()

        # Start the server engine (Option 1 *and* 2)
        cherrypy.engine.start()
        cherrypy.engine.block()


if __name__ == '__main__':
    server = Server()
    server.start()
