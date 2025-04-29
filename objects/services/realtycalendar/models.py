from typing import List, Optional, Dict
from pydantic import BaseModel


class Coordinates(BaseModel):
    lat: float
    lon: float


class PriceCommon(BaseModel):
    with_discount: Optional[float] = None
    without_discount: float
    discount_percent: int


class PriceDiscounts(BaseModel):
    long_stay: int
    promo_code: int


class PriceExtras(BaseModel):
    service_charge: int


class PayNow(BaseModel):
    with_discount: Optional[float] = None
    without_discount: float


class PayLater(BaseModel):
    with_discount: Optional[float] = None
    without_discount: float


class PriceDetails(BaseModel):
    amount: float
    discounts: PriceDiscounts
    extras: PriceExtras
    pay_now: PayNow
    pay_later: PayLater


class Price(BaseModel):
    common: PriceCommon
    details: PriceDetails


class Photo(BaseModel):
    url: str


class MetroStation(BaseModel):
    id: int
    title: str


class City(BaseModel):
    id: int
    title: str


class Apartment(BaseModel):
    id: int
    address: str
    rooms: int
    sleeps: str
    desc: str
    floor: int
    title: str
    area: float
    coordinates: Coordinates
    price: Price
    photos: List[Photo]
    metro_stations: List[MetroStation]
    city: City
    services: List[str]
    capacity: int
    max_children_count: int

    class Config:
        json_encoders = {
            str: lambda v: v.encode('unicode_escape').decode('utf-8') if isinstance(v, str) else v
        }

    @classmethod
    def filter_by_price(
            cls,
            apartments: list['Apartment'],
            price_min: Optional[float] = None,
            price_max: Optional[float] = None
    ) -> list['Apartment']:
        """
        Фильтрует список квартир по заданному диапазону цен.

        :param apartments: Список объектов Apartment для фильтрации
        :param price_min: Минимальная цена (опционально)
        :param price_max: Максимальная цена (опционально)
        :return: Отфильтрованный список квартир
        """
        filtered = []

        for apartment in apartments:
            current_price = apartment.price.common.without_discount

            # Проверяем попадание в диапазон
            if ((price_min is None or current_price >= price_min) and
                    (price_max is None or current_price <= price_max)):
                filtered.append(apartment)

        return filtered
