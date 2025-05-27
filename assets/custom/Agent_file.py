# Copyright (c) 2024-2025 MAA_SnowBreak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
MAA_SnowBreak
MAA_SnowBreak Agent调试启动器
作者:overflow65537
"""


from maa.agent.agent_server import AgentServer

from action.Fishing import Fishing
from action.ScreenShot import ScreenShot
from action.ShotSelf import ShotSelf
from action.ShotTarget import ShotTarget
from action.StoryRogue import StoryRogue
from action.Count import Count
from action.PuzzleClculate import PuzzleClculate


@AgentServer.custom_action("PuzzleClculate")
class Agent_PuzzleClculate(PuzzleClculate):
    pass


@AgentServer.custom_action("Count")
class Agent_Count(Count):
    pass


@AgentServer.custom_action("Fishing")
class Agent_Fishing(Fishing):
    pass


@AgentServer.custom_action("ShotSelf")
class Agent_ShotSelf(ShotSelf):
    pass


@AgentServer.custom_action("ShotTarget")
class Agent_ShotTarget(ShotTarget):
    pass


@AgentServer.custom_action("ScreenShot")
class Agent_ScreenShot(ScreenShot):
    pass


@AgentServer.custom_action("StoryRogue")
class Agent_StoryRogue(StoryRogue):
    pass
