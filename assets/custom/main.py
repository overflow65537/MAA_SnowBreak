import sys
from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

from action.Fishing import Fishing
from action.ScreenShot import ScreenShot
from action.ShotSelf import ShotSelf
from action.ShotTarget import ShotTarget
from action.StoryRogue import StoryRogue


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


def main():
    Toolkit.init_option("./")
    if len(sys.argv) > 1:
        print("使用自定义socket_id: " + sys.argv[-1])
        socket_id = sys.argv[-1]
    else:
        print("使用默认socket_id: MAA_AGENT_SOCKET")
        socket_id = "MAA_AGENT_SOCKET"
    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()
