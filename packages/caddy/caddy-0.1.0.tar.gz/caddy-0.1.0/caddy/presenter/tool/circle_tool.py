from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class CircleTool(BaseTool):

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.set_tool(context.circle_stage_tool)


class CircleStageTool(BaseTool):

    def canvas_click(self, context, point: Point):
        center = context.points[0]
        radius = int(center.dist_from(point))
        context.model.add_circle(center, radius)

        context.clear()
        context.set_tool(context.circle_tool)
