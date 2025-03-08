import sys
import os
from pathlib import Path
print(sys.argv)
if len(sys.argv) > 2:
    binding_dir = Path(sys.argv[-2]).resolve()
    os.environ["MAAFW_BINARY_PATH"] = str(binding_dir)

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

from action.Fishing import Fishing
from action.ScreenShot import ScreenShot
from action.ShotSelf import ShotSelf
from action.ShotTarget import ShotTarget
from action.StoryRogue import StoryRogue

def main():
    Toolkit.init_option("./")
    if len(sys.argv) >1:
        socket_id = sys.argv[-1]
    else:
        socket_id = "MAA_AGENT_SOCKET"
    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()

if __name__ == "__main__":
    main()
