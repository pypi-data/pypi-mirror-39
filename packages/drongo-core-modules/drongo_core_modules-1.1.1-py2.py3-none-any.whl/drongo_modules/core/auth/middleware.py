class AuthMiddleware(object):
    def before(self, ctx):
        token = None
        if 'HTTP_AUTHORIZATION' in ctx.request.env:
            token = ctx.request.env['HTTP_AUTHORIZATION']

        if token is not None:
            self.load_user_from_token(ctx, token)

    def load_user_from_token(self, ctx, token):
        auth = ctx.modules.auth
        user_token_svc = auth.services.UserForTokenService(token=token)

        ctx.auth.token = token
        ctx.auth.user = user_token_svc.call()
