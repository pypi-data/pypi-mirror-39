from flask import request, current_app, _app_ctx_stack, g
from datetime import datetime
from open_tracer import TraceRequest, trace_resource, sanitize_urlparams


class FlaskTracer(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.inject_headers)
        app.after_request(self.analyze_response)

    def inject_headers(*args, **kwargs):
        g.start_time = datetime.now()
        trace_id = request.headers.get("trace_id", None)
        request_id = request.headers.get("request_id", "")
        child_id = request.headers.get("child_id", "")

        if not trace_id:
            TraceRequest().set_trace_id(request_id, parent_id=child_id)
        else:
            TraceRequest().set_trace_id(trace_id, parent_id=child_id)

    def analyze_response(self, response):
        if "start_time" in g:
            end_time = datetime.now()
            if 400 <= response.status_code < 600:
                status = False
            else:
                status = True
            trace_resource("api-response", request.method, sanitize_urlparams(request.url), request.url, g.start_time, end_time, status)
        return response

