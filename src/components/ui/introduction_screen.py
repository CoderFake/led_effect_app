import flet as ft
import asyncio
from typing import Callable, Optional


class LoadingDots(ft.Container):
    def __init__(self):
        super().__init__()
        self.dots = [
            ft.Container(width=10, height=10, border_radius=10, bgcolor=ft.Colors.BLUE_600, opacity=0.9,
                         scale=ft.Scale(0.7), animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT)),
            ft.Container(width=10, height=10, border_radius=10, bgcolor=ft.Colors.PURPLE_600, opacity=0.9,
                         scale=ft.Scale(0.7), animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT)),
            ft.Container(width=10, height=10, border_radius=10, bgcolor=ft.Colors.PINK_600, opacity=0.9,
                         scale=ft.Scale(0.7), animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT)),
        ]
        self.content = ft.Row(self.dots, spacing=8, alignment=ft.MainAxisAlignment.CENTER)
        self.opacity = 0.0
        self.animate_opacity = ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)

    async def pulse(self, page: ft.Page, cycles: int = 6, interval: float = 0.18):
        for _ in range(cycles):
            for i, d in enumerate(self.dots):
                d.scale = ft.Scale(1.0)
                page.update()
                await asyncio.sleep(interval)
                d.scale = ft.Scale(0.7)
                page.update()


class IntroductionScreen(ft.Container):
    def __init__(self, page: ft.Page, on_complete: Optional[Callable] = None):
        super().__init__()
        self.page = page
        self.on_complete = on_complete

        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.alignment = ft.alignment.center

        self.logo_container = None
        self.title_wrapper = None
        self.title_text = None
        self.loading_dots = None

        self.content = self.build_content()

    def build_content(self):
        self.logo_container = ft.Container(
            content=ft.Image(
                src="/assets/yamaha.png",
                width=400,
                height=300,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                error_content=ft.Container(
                    content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=100, color=ft.Colors.GREY_400),
                    alignment=ft.alignment.center,
                    width=400,
                    height=300,
                ),
            ),
            opacity=1.0,
            animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
            alignment=ft.alignment.center,
        )

        self.title_text = ft.ShaderMask(
            content=ft.Text(
                "LIGHT PATTERN DESIGNER",
                size=56,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.WHITE,
            ),
            shader=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_600, ft.Colors.PURPLE_600, ft.Colors.PINK_600, ft.Colors.ORANGE_600],
                stops=[0.0, 0.3, 0.7, 1.0],
            ),
            blend_mode=ft.BlendMode.SRC_IN,
        )

        self.title_wrapper = ft.Container(
            content=self.title_text,
            opacity=0.0,
            animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(350, ft.AnimationCurve.EASE_OUT),
        )

        self.loading_dots = LoadingDots()

        return ft.Column(
            [
                ft.Container(expand=True),
                self.logo_container,
                ft.Container(height=40),
                ft.Row(
                    [
                        ft.Container(expand=True),
                        self.title_wrapper,
                        ft.Container(width=16),
                        self.loading_dots,
                        ft.Container(expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

    async def start_animation_sequence(self):
        await asyncio.sleep(0.5)
        await self._fade_out_logo()
        await self._fade_in_title()
        await self._nudge_title_left()
        await self._show_loading()
        await self._complete_intro()

    async def _fade_out_logo(self):
        self.logo_container.opacity = 0.0
        self.page.update()
        await asyncio.sleep(1.0)

    async def _fade_in_title(self):
        await asyncio.sleep(0.1)
        self.title_wrapper.opacity = 1.0
        self.page.update()
        await asyncio.sleep(0.8)

    async def _nudge_title_left(self):
        self.title_wrapper.offset = ft.Offset(-0.03, 0)  
        self.page.update()
        await asyncio.sleep(0.35)

    async def _show_loading(self):
        self.loading_dots.opacity = 1.0
        self.page.update()
        await self.loading_dots.pulse(self.page, cycles=6, interval=0.18)

    async def _complete_intro(self):
        self.title_wrapper.opacity = 0.0
        self.loading_dots.opacity = 0.0
        self.page.update()
        await asyncio.sleep(0.4)

        if self.on_complete:
            self.on_complete()

    def set_custom_gradient_colors(self, colors: list, stops: list = None):
        if stops is None:
            stops = [i / (len(colors) - 1) for i in range(len(colors))]
        self.title_text.shader = ft.LinearGradient(
            begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=colors, stops=stops
        )
        self.page.update()

    def set_logo_frame_size(self, width: int, height: int):
        self.logo_container.content.width = width
        self.logo_container.content.height = height
        self.page.update()

    def set_logo_fit_mode(self, fit_mode: ft.ImageFit):
        self.logo_container.content.fit = fit_mode
        self.page.update()


class IntroductionManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.intro_screen = None
        self.main_app = None

    async def show_introduction(self, main_app_factory):
        self.intro_screen = IntroductionScreen(
            self.page, on_complete=lambda: self._transition_to_main_app(main_app_factory)
        )
        self.page.controls.clear()
        self.page.add(self.intro_screen)
        self.page.update()
        await self.intro_screen.start_animation_sequence()

    def _transition_to_main_app(self, main_app_factory):
        async def _do_transition():
            self.main_app = main_app_factory()

            self.intro_screen.animate_opacity = ft.Animation(500, ft.AnimationCurve.EASE_OUT)
            self.intro_screen.opacity = 0.0
            self.page.update()
            await asyncio.sleep(0.5)

            self.page.controls.clear()
            self.page.add(self.main_app)

            self.main_app.opacity = 0.0
            self.main_app.animate_opacity = ft.Animation(500, ft.AnimationCurve.EASE_IN)
            self.page.update()

            await asyncio.sleep(0.1)
            self.main_app.opacity = 1.0
            self.page.update()

        self.page.run_task(_do_transition)
