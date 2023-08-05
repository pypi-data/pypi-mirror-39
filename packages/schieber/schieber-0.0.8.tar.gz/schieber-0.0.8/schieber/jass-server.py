import asyncio
import logging
import sys

import jsonpickle
import websockets
from threading import Thread

from schieber.player.external_player import ExternalPlayer
from schieber.team import Team
from schieber.game import Game
from schieber.player.random_player import RandomPlayer

logger = logging.getLogger(__name__)


class JassServer():

    def __init__(self, game):
        self.game = game
        self.hostname = "localhost"
        self.port = 9000
        # start the server in a new thread
        new_loop = asyncio.new_event_loop()
        thread = Thread(target=self.start_server, args=(new_loop,))
        thread.start()

    def start_server(self, event_loop):
        asyncio.set_event_loop(event_loop)
        start_server = websockets.serve(self.wait_for_client, self.hostname, self.port)
        event_loop.run_until_complete(start_server)
        event_loop.run_forever()

    async def wait_for_client(self, websocket, path):
        message = await websocket.recv()
        if message == "start":
            self.start()
        if message == "reset":
            if self.game is not None:
                self.reset()

    def start(self):
        players = [RandomPlayer(name='Tick', ), RandomPlayer(name='Trick'),
                   RandomPlayer(name='Track'), RandomPlayer(name='Dagobert')]

        team_1 = Team(players=[players[0], players[2]])
        team_2 = Team(players=[players[1], players[3]])
        teams = [team_1, team_2]

        self.game = Game(teams, point_limit=1000, use_counting_factor=False, seed=1)
        self.game.play()

    def reset(self):
        self.game.reset_points()
        self.game.play()
