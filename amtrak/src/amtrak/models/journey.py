
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JourneyResponse:
    data: JourneyData


@dataclass
class JourneyData:
    journey_solution_option: JourneySolutionOption


@dataclass
class JourneySolutionOption:
    journey_legs: list[JourneyLeg]


@dataclass
class JourneyLeg:
    journey_leg_options: list[JourneyLegOption]


@dataclass
class JourneyLegOption:
    origin: StationAndTime
    destination: StationAndTime
    travel_legs: list[TravelLeg]
    reservable_accommodations: list[ReservableAccomodation]


@dataclass
class StationAndTime:
    code: str
    name: str
    schedule: StationTime


@dataclass
class StationTime:
    arrivalDateTime: str | None  # parse directly into Date?
    departureDateTime: str | None


@dataclass
class TravelLeg:
    origin: StationAndTime
    destination: StationAndTime
    elapsedSeconds: int


@dataclass
class ReservableAccomodation:
    travel_class: str  # "Coach" "Coach" "Business"
    fare_family: str  # "VLU" "FLX" "NA"
    # accommodation_fare: AccomodationFare
    travel_leg_accommodations: list[TravelLegAccommodations]


@dataclass
class TravelLegAccommodations:
    travel_leg_fare: AccomodationFare


@dataclass
class AccomodationFare:
    dollars_amount: DollarsAmount


@dataclass
class DollarsAmount:
    total: str  # validate/convert to float (or decimal?)
