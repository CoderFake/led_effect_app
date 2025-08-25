import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from components.panel.segment_edit_action import SegmentEditActionHandler
from services.color_service import color_service
from services.data_cache import data_cache


class StubSegmentComponent:
    def __init__(self, segment_id: str):
        self._segment_id = segment_id

    def get_selected_segment(self):
        return self._segment_id


def test_segment_updates_persist_across_switch():
    handler = SegmentEditActionHandler(page=None)

    # Reset to initial scene with default segment
    data_cache.set_current_scene(0)
    color_service.sync_with_cache_palette()
    color_service.set_current_segment_id("0")

    # Ensure second segment exists
    data_cache.create_new_segment(custom_id=1)

    # Update values for segment 0
    handler.update_segment_color_slot("0", 0, 3)
    handler.update_transparency_from_slider(0, 0.5, StubSegmentComponent("0"))
    handler.update_length_parameter(0, "20", StubSegmentComponent("0"))

    # Switch to another segment then back
    color_service.set_current_segment_id("1")
    color_service.set_current_segment_id("0")

    seg0 = data_cache.get_segment("0")
    assert seg0.color[0] == 3
    assert seg0.transparency[0] == 0.5
    assert seg0.length[0] == 20
