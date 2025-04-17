from maa.agent.agent_server import AgentServer

from action.Fishing import Fishing
from action.ScreenShot import ScreenShot
from action.ShotSelf import ShotSelf
from action.ShotTarget import ShotTarget
from action.StoryRogue import StoryRogue
from action.Count import Count
from action.Puzzle_Clculate import PuzzleClculate


@AgentServer.custom_action("Puzzle_Clculate")
class Agent_Puzzle_Clculate(PuzzleClculate):
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