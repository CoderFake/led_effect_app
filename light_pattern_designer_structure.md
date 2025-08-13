"""
Light Pattern Designer - Cấu trúc dự án

led_effect_app/
├── src/
│   ├── __init__.py
│   ├── main.py                     # Entry point
│   ├── app/
│   │   ├── __init__.py
│   │   ├── light_pattern_app.py    # Main application class
│   │   └── config.py               # App configuration
│   ├── components/
│   │   ├── __init__.py
│   │   ├── menu_bar.py             # File menu component
│   │   ├── scene_effect_panel.py   # Scene/Effect controls
│   │   ├── color_palette.py        # Color palette component
│   │   ├── region_settings.py      # Region settings panel
│   │   └── segment_edit.py         # Segment editing panel
│   ├── models/
│   │   ├── __init__.py
│   │   ├── scene.py                # Scene data model
│   │   ├── effect.py               # Effect data model
│   │   ├── segment.py              # Segment data model
│   │   ├── color_palette.py        # Color palette data model
│   │   └── region.py               # Region data model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_service.py         # File I/O operations
│   │   ├── osc_service.py          # OSC communication
│   │   └── data_service.py         # Data management
│   └── utils/
│       ├── __init__.py
│       ├── constants.py            # Application constants
│       └── helpers.py              # Helper functions
├── assets/
│   └── icons/                      # Application icons
├── tests/
│   ├── __init__.py
│   ├── test_components/
│   ├── test_models/
│   └── test_services/
├── requirements.txt
├── README.md
└── setup.py

=== MÔ TẢ CÁC MODULE ===

1. main.py
   - Entry point của ứng dụng
   - Khởi tạo Flet app và gọi LightPatternApp

2. app/light_pattern_app.py
   - Main application class
   - Quản lý layout tổng thể
   - Điều phối các component

3. components/
   - menu_bar.py: File menu (Open, Save, Save as)
   - scene_effect_panel.py: Scene ID, Effect ID controls
   - color_palette.py: Color palette management
   - region_settings.py: Region configuration
   - segment_edit.py: Segment editing interface

4. models/
   - Các data class cho Scene, Effect, Segment, etc.
   - Validation và business logic

5. services/
   - file_service.py: JSON file operations
   - osc_service.py: OSC communication với lighting system
   - data_service.py: Data synchronization

=== THIẾT KẾ RESPONSIVE ===

- Sử dụng ft.ResponsiveRow và ft.Column với expand
- Layout chính: Row với 2 cột (Scene/Effect bên trái, Segment Edit bên phải)
- Các panel có thể thu gọn/mở rộng
- Breakpoints cho mobile/tablet/desktop

=== KIẾN TRÚC COMPONENT ===

Mỗi component kế thừa từ ft.UserControl:
- Tự quản lý state
- Event handling riêng biệt
- Có thể reuse
- Responsive design
"""