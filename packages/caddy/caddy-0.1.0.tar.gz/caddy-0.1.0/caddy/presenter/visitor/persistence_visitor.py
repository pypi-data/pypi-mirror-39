from caddy.presenter.visitor.visitor import Visitor


class PersistenceVisitor(Visitor):

    def visit_polyline(self, line):
        raise NotImplementedError

    def visit_rectangle(self, rectangle):
        raise NotImplementedError

    def visit_circle(self, circle):
        raise NotImplementedError
