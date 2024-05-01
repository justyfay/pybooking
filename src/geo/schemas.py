from typing import List, Optional

from pydantic import BaseModel, Field, RootModel


class GeoSchema(BaseModel):
    """Схема получения информации по локациям."""

    name: str
    type: str


class Locations(RootModel):
    """Схема получения списка локаций."""

    root: List[GeoSchema]


class Geometry(BaseModel):
    """Вложенная схема - геометрия гео-объекта."""

    type: str
    coordinates: List[float]


class Properties(BaseModel):
    """Вложенная схема - данные гео-объекта."""

    balloon_content: str = Field(alias="balloonContent")
    cluster_caption: str = Field(alias="clusterCaption")
    hint_content: str = Field(alias="hintContent")
    icon_content: Optional[str] = Field(default=..., alias="iconContent")
    icon_caption: Optional[str] = Field(default=..., alias="iconCaption")


class Options(BaseModel):
    """Вложенная схема - опции гео-объекта и его составных частей."""

    icon_color: Optional[str] = Field(default=..., alias="iconColor")
    preset: Optional[str] = None
    cursor: Optional[str] = None
    hide_icon_on_balloon_open: Optional[bool] = Field(
        default=..., alias="hideIconOnBalloonOpen"
    )
    open_balloon_on_click: Optional[bool] = Field(
        default=..., alias="openBalloonOnClick"
    )


class Feature(BaseModel):
    """Вложенная схема - информация о гео-объекте."""

    type: str
    id: int
    geometry: Geometry
    properties: Properties
    options: Options


class MapSchema(BaseModel):
    """Схема отображения гео-объектов на карте."""

    type: str
    features: List[Feature]
