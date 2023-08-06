from abc import ABC, abstractmethod
from caddy.shared.point import Point


class BaseTool(ABC):

    def tool_cursor(self, context):
        context.clear()
        context.set_tool(context.default_tool)

    def tool_move(self, context):
        context.clear()
        context.set_tool(context.move_tool)

    def tool_remove(self, context):
        context.clear()
        context.set_tool(context.eraser_tool)

    def tool_add_line(self, context):
        context.clear()
        context.set_tool(context.line_tool)

    def tool_add_rectangle(self, context):
        context.clear()
        context.set_tool(context.rectangle_tool)

    def tool_add_circle(self, context):
        context.clear()
        context.set_tool(context.circle_tool)

    @abstractmethod
    def canvas_click(self, context, point: Point):
        raise NotImplementedError
