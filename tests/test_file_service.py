import json
from services.file_service import FileService
from services.data_cache import DataCacheService


def test_save_to_path_writes_model_format(tmp_path):
    dc = DataCacheService()
    fs = FileService(dc)
    target = tmp_path / "scene_save_as.json"
    assert fs.save_to_path(str(target))
    with open(target, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == dc.export_to_dict()


def test_save_file_uses_current_path(tmp_path):
    dc = DataCacheService()
    fs = FileService(dc)
    fs.current_file_path = str(tmp_path / "scene_save.json")
    fs.mark_as_changed()
    assert fs.save_file()
    with open(fs.current_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == dc.export_to_dict()
