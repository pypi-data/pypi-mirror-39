from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class RectangleTool(BaseTool):

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.set_tool(context.rectangle_stage_tool)


class RectangleStageTool(BaseTool):

    def canvas_click(self, context, point2: Point):
        point1 = context.points[0]
        context.model.add_rectangle(point1, point2)

        context.clear()
        context.set_tool(context.rectangle_tool)
