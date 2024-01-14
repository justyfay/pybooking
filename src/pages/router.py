import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent
from starlette.responses import FileResponse

from config import settings

router = APIRouter()


@router.get("/img/{filename}")
def get_img(filename: str):
    filepath = os.path.join(os.getcwd() + "/static/images", filename)
    return FileResponse(filepath)


@router.get("/css/{filename}")
def get_css(filename: str):
    filepath = os.path.join(os.getcwd() + "/static/css", filename)
    return FileResponse(filepath)


@router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def main2_page() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Navbar(
                    title="PyBooking", title_event=GoToEvent(url=settings.base_url)
                ),
                c.Div(
                    class_name="header_container",
                    components=[
                        c.Image(
                            class_name="header_image",
                            src=f"{settings.base_url}/img/header.jpg",
                            width="100%",
                            height="100%",
                        )
                    ],
                ),
                c.Div(
                    class_name="search_container",
                    components=[
                        c.Div(
                            class_name="search_panel location_container",
                            components=[
                                c.FormFieldSelect(
                                    name="search_input location_input",
                                    title="",
                                    options=[
                                        {"value": "hammer", "label": "Hammer"},
                                        {
                                            "value": "screwdriver",
                                            "label": "Screwdriver",
                                        },
                                    ],
                                    type="FormFieldSelect",
                                )
                            ],
                        ),
                        c.Div(
                            class_name="search_panel arrival_date_container",
                            components=[
                                c.FormFieldSelect(
                                    name="search_input arrival_date_input",
                                    title="",
                                    options=[
                                        {"value": "hammer", "label": "Hammer"},
                                        {
                                            "value": "screwdriver",
                                            "label": "Screwdriver",
                                        },
                                    ],
                                    type="FormFieldSelect",
                                )
                            ],
                        ),
                        c.Div(
                            class_name="search_panel departure_date_container",
                            components=[
                                c.FormFieldSelect(
                                    name="search_input departure_date_input",
                                    title="",
                                    options=[
                                        {"value": "hammer", "label": "Hammer"},
                                        {
                                            "value": "screwdriver",
                                            "label": "Screwdriver",
                                        },
                                    ],
                                    type="FormFieldSelect",
                                )
                            ],
                        ),
                        c.Div(
                            class_name="search_panel search_button_container",
                            components=[
                                c.Button(
                                    class_name="search_button btn btn-primary btn-lg w-100",
                                    text="Найти",
                                ),
                            ],
                        ),
                    ],
                ),
                c.Heading(
                    class_name="direction_heading",
                    text="Популярные направления",
                    level=2,
                ),
                c.Div(
                    class_name="country_cards",
                    components=[
                        c.Div(
                            class_name="card_container russia_card",
                            components=[
                                c.Image(
                                    class_name="card russia_card",
                                    width="100%",
                                    height="100%",
                                    src=f"{settings.base_url}/img/russia_card.jpg",
                                ),
                                c.Heading(
                                    class_name="direction_russia",
                                    text="Россия",
                                    level=5,
                                ),
                            ],
                        ),
                        c.Div(
                            class_name="card_container turkey_card",
                            components=[
                                c.Image(
                                    class_name="card turkey_card",
                                    width="100%",
                                    height="100%",
                                    src=f"{settings.base_url}/img/istanbul_card.jpg",
                                ),
                                c.Heading(
                                    class_name="direction_istanbul",
                                    text="Турция",
                                    level=5,
                                ),
                            ],
                        ),
                        c.Div(
                            class_name="card_container egipet_card",
                            components=[
                                c.Image(
                                    class_name="card egipet_card",
                                    width="100%",
                                    height="100%",
                                    src=f"{settings.base_url}/img/egipet_card.jpg",
                                ),
                                c.Heading(
                                    class_name="direction_russia",
                                    text="Египет",
                                    level=5,
                                ),
                            ],
                        ),
                        c.Div(
                            class_name="card_container emieates_card",
                            components=[
                                c.Image(
                                    class_name="card emieates_card",
                                    width="100%",
                                    height="100%",
                                    src=f"{settings.base_url}/img/emieates_card.jpg",
                                ),
                                c.Heading(
                                    class_name="direction_russia",
                                    text="ОАЭ",
                                    level=5,
                                ),
                            ],
                        ),
                    ],
                ),
                c.Footer(
                    links=[
                        c.Link(
                            components=[c.Text(text="Github")],
                            on_click=GoToEvent(
                                url="https://github.com/justyfay/pybooking"
                            ),
                        )
                    ]
                ),
            ],
        )
    ]


_PREBUILT_VERSION = "0.0.15"
_PREBUILT_CDN_URL = f"https://cdn.jsdelivr.net/npm/@pydantic/fastui-prebuilt@{_PREBUILT_VERSION}/dist/assets"


def prebuilt_html(title: str = ""):
    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <script type="module" crossorigin src="{_PREBUILT_CDN_URL}/index.js"></script>
    <link rel="stylesheet" crossorigin href="{_PREBUILT_CDN_URL}/index.css">
    <link rel="stylesheet" href="{settings.base_url}/css/style.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""


@router.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    print(f"{settings.base_url}/css/style.css")

    return HTMLResponse(prebuilt_html(title="Бронирование отелей - PyBooking"))
