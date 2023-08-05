class CORSMiddleware(object):
    def before(self, ctx):
        if ctx.request.method == 'OPTIONS':
            pass

    def after(self, ctx):
        resp = ctx.response
        resp.set_header(
            'Access-Control-Allow-Origin', '*')
        resp.set_header(
            'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Keep-Alive,User-Agent,X-Requested-With,Cache-Control,'
            'Content-Type,Authorization,App-ID,App-Secret')
        resp.set_header(
            'Access-Control-Expose-Headers',
            'Keep-Alive,User-Agent,X-Requested-With,Cache-Control,'
            'Content-Type,Authorization,App-ID,App-Secret')

    def exception(self, ctx, exc):
        resp = ctx.response
        resp.set_header(
            'Access-Control-Allow-Origin', '*')
        resp.set_header(
            'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Keep-Alive,User-Agent,X-Requested-With,Cache-Control,'
            'Content-Type,Authorization,App-ID,App-Secret')
        resp.set_header(
            'Access-Control-Expose-Headers',
            'Keep-Alive,User-Agent,X-Requested-With,Cache-Control,'
            'Content-Type,Authorization,App-ID,App-Secret')
