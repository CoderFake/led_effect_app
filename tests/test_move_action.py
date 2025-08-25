import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from components.move.move_action import MoveActionHandler


def test_update_move_speed_accepts_string_and_validates():
    handler = MoveActionHandler(page=None)
    assert handler.update_move_speed("5")
    assert not handler.update_move_speed("-1")
    assert not handler.update_move_speed("abc")

