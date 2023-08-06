from caddy.model.model import Model, ModelObserver
from caddy.presenter.tool_context import ToolContext
from caddy.presenter.visitor.drawing_visitor import DrawingVisitor
from caddy.shared.point import Point
from caddy.view.buttons import ButtonFrame


class Presenter(ModelObserver):
    def __init__(self, model: Model, app) -> None:
        # TODO: Interfaces for views instead of Application instance
        super().__init__()
        self.context: ToolContext = ToolContext(model)
        self.model: Model = model
        self.app = app
        self.drawing_visitor = DrawingVisitor(app)

        # Register as a model observer
        model.attach_observer(self)

        # Register itself to button events
        btn_event_handlers = {
            ButtonFrame.ButtonEvents.CURSOR: lambda: self.context.tool_cursor(),
            ButtonFrame.ButtonEvents.MOVE: lambda: self.context.tool_move(),
            ButtonFrame.ButtonEvents.REMOVE: lambda: self.context.tool_remove(),
            ButtonFrame.ButtonEvents.POLYLINE: lambda: self.context.tool_add_line(),
            ButtonFrame.ButtonEvents.RECTANGLE: lambda: self.context.tool_add_rectangle(),
            ButtonFrame.ButtonEvents.CIRCLE: lambda: self.context.tool_add_circle()
        }
        for event, function in btn_event_handlers.items():
            app.button_menu.register_button_handler(event, function)

        # Register itself to canvas click events
        app.canvas.register_canvas_click_handler(lambda coord: self.context.canvas_click(Point(coord[0], coord[1])))

    def on_model_changed(self):
        self.app.canvas.canvas_clear()
        self.model.accept_visitor(self.drawing_visitor)
