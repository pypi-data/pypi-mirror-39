from typing import List

from caddy.model.model import Model
from caddy.presenter.tool.base_tool import BaseTool
from caddy.presenter.tool.circle_tool import CircleTool, CircleStageTool
from caddy.presenter.tool.default_tool import DefaultTool
from caddy.presenter.tool.eraser_tool import EraserTool
from caddy.presenter.tool.line_tool import LineTool, LineStageTool
from caddy.presenter.tool.move_tool import MoveTool, MoveStageTool
from caddy.presenter.tool.rectangle_tool import RectangleTool, RectangleStageTool
from caddy.shared.point import Point


class ToolContext:
    # Class attributes containing instances of all possible states/tool
    default_tool = DefaultTool()
    line_tool = LineTool()
    line_stage_tool = LineStageTool()
    rectangle_tool = RectangleTool()
    rectangle_stage_tool = RectangleStageTool()
    circle_tool = CircleTool()
    circle_stage_tool = CircleStageTool()
    move_tool = MoveTool()
    move_stage_tool = MoveStageTool()
    eraser_tool = EraserTool()

    def __init__(self, model: Model):
        self._current_tool: BaseTool = self.default_tool
        self.points: List[Point] = []
        self.recent_object_id: int = -1
        self.model: Model = model

    def set_tool(self, state: BaseTool):
        self._current_tool = state

    def clear(self):
        self.recent_object_id = -1
        self.points.clear()

    def canvas_click(self, point: Point):
        self._current_tool.canvas_click(self, point)

    def tool_cursor(self):
        self._current_tool.tool_cursor(self)

    def tool_move(self):
        self._current_tool.tool_move(self)

    def tool_remove(self):
        self._current_tool.tool_remove(self)

    def tool_add_line(self):
        self._current_tool.tool_add_line(self)

    def tool_add_rectangle(self):
        self._current_tool.tool_add_rectangle(self)

    def tool_add_circle(self):
        self._current_tool.tool_add_circle(self)
