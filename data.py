from pydantic import BaseModel, computed_field


class RegistrationInformation(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class DemographicInformation(BaseModel):
    gender: str
    age_group: str
    primary_language: str
    relationship_status: str
    income_range: str
    occupation: str
    country_region: str
    education_level: str
    ethnicity: str


class ViewingPreferences(BaseModel):
    favorite_genres: list[str]
    genres_to_avoid: list[str]
    preferred_narrative_elements: list[str]
    preferred_themes: list[str]
    preferred_plots: list[str]
    preferred_formats: list[str]
    preferred_min_lengths: list[str]
    ratings_to_avoid: list[str]
    preferred_streaming_services: list[str]


class PersonalFavorite(BaseModel):
    title: str
    platform: str


class ViewingHistory(BaseModel):
    format: str
    title: str
    viewed_date: str
    platform: str
    liked: bool = True


class CurrentConditions(BaseModel):
    season: str | None
    holiday: str | None
    occasion: str | None
    audience: str | None
    weather: str | None


class Recommendation(BaseModel):
    title: str
    preview_keyframe: str
    streaming_platform: str
    url: str
    reason: str
    liked: bool = True


class RecommendationList(BaseModel):
    recommendations: list[Recommendation]


class ViewerProfile(BaseModel):
    registration_information: RegistrationInformation
    personalization: bool = True
    demographic_information: DemographicInformation
    viewing_preferences: ViewingPreferences
    personal_favorites: list[PersonalFavorite]
    viewing_history: list[ViewingHistory]
    current_conditions: CurrentConditions
    recommendations: list[Recommendation]
