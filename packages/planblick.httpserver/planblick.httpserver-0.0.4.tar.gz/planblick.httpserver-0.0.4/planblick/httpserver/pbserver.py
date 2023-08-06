import os
import cherrypy

class Server:

    def start(self, flask_app):
        # Mount the application
        cherrypy.tree.graft(flask_app, "/")


        class Static(object): pass


        # Add static file serving to enable swagger GUI
        PATH = os.path.abspath(os.path.dirname(__file__))
        cherrypy.tree.mount(Static(), '/static', config={
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH + '/static',
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


