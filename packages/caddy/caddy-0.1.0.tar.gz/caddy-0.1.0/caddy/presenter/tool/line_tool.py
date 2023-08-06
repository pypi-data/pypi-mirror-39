import copy

from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class LineTool(BaseTool):

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.set_tool(context.line_stage_tool)


class LineStageTool(BaseTool):

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.model.remove_by_id(context.recent_object_id)
        context.recent_object_id = context.model.add_polyline(copy.deepcopy(context.points))
 