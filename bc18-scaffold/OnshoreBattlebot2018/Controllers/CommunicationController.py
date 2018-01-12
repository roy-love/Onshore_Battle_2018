import random
import sys
import traceback

# Manages communications between Earth and Mars
# Provides public methods for reading and writing
# Messages must be as small and efficient as possible
class CommunicationController:
      def __init__(self, gameController):
            self.game_controller = gameController