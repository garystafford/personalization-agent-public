import json
import logging
import random
import sys
from typing import List

import gradio as gr
from pydantic import ValidationError

import agent
from data import (
    CurrentConditions,
    DemographicInformation,
    PersonalFavorite,
    Recommendation,
    RecommendationList,
    RegistrationInformation,
    ViewerProfile,
    ViewingPreferences,
)

# Basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

personalization_agent = agent.create_agent()

viewer_profiles: List[ViewerProfile] = []


def check_agent_health() -> str:
    config_info = f""" 
- __Model Host__: Bedrock
- __Model__: {personalization_agent.model.config['model_id']}
- __Includes Tool Result Status__: {personalization_agent.model.config['include_tool_result_status']}
- __Temperature__: {personalization_agent.model.config['temperature']}
- __Cache Prompt__: {personalization_agent.model.config['cache_prompt']}
- __Cache Tools__: {personalization_agent.model.config['cache_tools']}
- __Streaming__: {personalization_agent.model.config['streaming']}
"""  # type: ignore

    try:
        prompt_health = "Just return the word 'Healthy'. No additional text, preamble, explanation, tools, formatting, reasoning, or reflection."
        response = personalization_agent(prompt_health)
        response_health = response.message.get("content", "No response received.")[
            0
        ].get("text", "No response received.")
        response_latency = response.metrics.accumulated_metrics.get(
            "latencyMs", "No response received."
        )
        total_tokens = response.metrics.accumulated_usage.get(
            "totalTokens", "No response received."
        )
        logger.debug(f"Agent health check response: {response}")
        config_info += f"\n- __Agent Health Check Status__:\n{response_health}"
        config_info += f"\n- __Accumulated Latency__:\n{response_latency}ms"
        config_info += f"\n- __Accumulated Tokens__:\n{total_tokens}"
    except Exception as e:
        logger.error(f"Agent health check failed: {e}")
        config_info += f"\n- __Agent Health Check Error__:\n{e}"
    return config_info


def fetch_viewer_profiles(file_path: str) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)
    try:
        global viewer_profiles
        viewer_profiles = [ViewerProfile.model_validate(user) for user in data]
        logger.info(f"Fetched viewer profiles: {len(viewer_profiles)} profiles loaded.")
    except ValidationError as e:
        logger.error(f"Error loading viewer profiles: {e}")


fetch_viewer_profiles("viewer_profiles.json")


def fetch_generic_recommendations(file_path: str) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    try:
        global generic_recommendations
        generic_recommendations = [Recommendation.model_validate(rec) for rec in data]
        logger.info(
            f"Fetched generic recommendations: {len(generic_recommendations)} recommendations loaded."
        )
    except ValidationError as e:
        logger.error(f"Error loading generic recommendations: {e}")


fetch_generic_recommendations("generic_recommendations.json")


def retrieve_generic_recommendations() -> str:
    # recommendations = generic_recommendations.model_dump_json(indent=4)
    recommendations = random.sample(generic_recommendations, 8)

    return json.dumps(
        [recommendation.model_dump() for recommendation in recommendations], indent=4
    )


def save_viewer_profile(viewer_profile: ViewerProfile):
    """Load viewer profiles from the JSON file and replace or add the given viewer profile.

    Args:
        viewer_profile (UserProfile): The viewer profile to save.
    """

    with open(file="viewer_profiles.json", mode="r", encoding="utf-8") as f:
        viewer_profiles = json.load(f)
        viewer_profiles = [
            ViewerProfile.model_validate(profile) for profile in viewer_profiles
        ]

    for idx, profile in enumerate(viewer_profiles):
        if (
            profile.registration_information.username
            == viewer_profile.registration_information.username
        ):
            viewer_profiles[idx] = viewer_profile
            logger.info(
                f"Viewer profile updated: {viewer_profile.registration_information.username}"
            )
            break
    else:
        viewer_profiles.append(viewer_profile)
        logger.info(
            f"New viewer profile created: {viewer_profile.registration_information.username}"
        )

    with open(file="viewer_profiles.json", mode="w", encoding="utf-8") as f:
        json.dump([profile.model_dump() for profile in viewer_profiles], f, indent=4)

    logger.info(
        f"Viewer profile saved: {viewer_profile.registration_information.username}"
    )


def create_viewer_profile(
    first_name,
    last_name,
    username,
    password,
    email,
    personalization_choice,
    gender,
    age_group,
    primary_language,
    relationship_status,
    income_range,
    occupation,
    country_region,
    education_level,
    ethnicity,
    favorite_genres,
    genres_to_avoid,
    preferred_narrative_elements,
    preferred_themes,
    preferred_plots,
    preferred_formats,
    preferred_min_lengths,
    ratings_to_avoid,
    preferred_streaming_services,
    favorite_one_title,
    favorite_one_platform,
    favorite_two_title,
    favorite_two_platform,
    favorite_three_title,
    favorite_three_platform,
    favorite_four_title,
    favorite_four_platform,
    favorite_five_title,
    favorite_five_platform,
    season_input,
    holiday_input,
    occasion_input,
    audience_input,
    weather_input,
) -> str:
    """
    Processes user input and returns a JSON object.

    Args:
        first_name (str): The first name provided by the user.
        last_name (str): The last name provided by the user.
        username (str): The username provided by the user.
        password (str): The password provided by the user.
        email (str): The email provided by the user.
        personalization_choice (bool): The personalization choice provided by the user.
        gender (str): The gender provided by the user.
        age_group (str): The age group provided by the user.
        primary_language (str): The primary language provided by the user.
        relationship_status (str): The relationship status provided by the user.
        income_range (str): The income range provided by the user.
        occupation (str): The occupation provided by the user.
        country_region (str): The country or region provided by the user.
        education_level (str): The education level provided by the user.
        ethnicity (str): The ethnicity provided by the user.
        favorite_genres (list): List of favorite genres.
        genres_to_avoid (list): List of genres to avoid.
        preferred_narrative_elements (list): List of preferred narrative elements.
        preferred_themes (list): List of preferred themes.
        preferred_plots (list): List of preferred plots.
        preferred_formats (list): List of preferred formats.
        preferred_min_lengths (list): List of preferred minimum lengths.
        ratings_to_avoid (list): List of ratings to avoid.
        favorite_platforms (list): List of favorite viewing platforms.
        favorite_one_title (str): Title of the first favorite content.
        favorite_one_platform (str): Platform of the first favorite content.
        favorite_two_title (str): Title of the second favorite content.
        favorite_two_platform (str): Platform of the second favorite content.
        favorite_three_title (str): Title of the third favorite content.
        favorite_three_platform (str): Platform of the third favorite content.
        favorite_four_title (str): Title of the fourth favorite content.
        favorite_four_platform (str): Platform of the fourth favorite content.
        favorite_five_title (str): Title of the fifth favorite content.
        favorite_five_platform (str): Platform of the fifth favorite content.
        season_input (str): The current season.
        holiday_input (str): The current holiday.
        occasion_input (str): The current occasion.
        audience_input (str): The target audience.
        weather_input (str): The current weather.

    Returns:
        str: A JSON string representation of the user profile.
    """

    if not all([first_name, last_name, username, password]):
        return json.dumps(
            {"error": "First name, last name, username, and password are required."}
        )

    registration = RegistrationInformation(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email,
    )
    demographic = DemographicInformation(
        gender=gender,
        age_group=age_group,
        primary_language=primary_language,
        relationship_status=relationship_status,
        income_range=income_range,
        occupation=occupation,
        country_region=country_region,
        education_level=education_level,
        ethnicity=ethnicity,
    )
    viewing = ViewingPreferences(
        favorite_genres=favorite_genres,
        genres_to_avoid=genres_to_avoid,
        preferred_narrative_elements=preferred_narrative_elements,
        preferred_themes=preferred_themes,
        preferred_plots=preferred_plots,
        preferred_formats=preferred_formats,
        preferred_min_lengths=preferred_min_lengths,
        ratings_to_avoid=ratings_to_avoid,
        preferred_streaming_services=preferred_streaming_services,
    )
    personal_favorites = []
    if favorite_one_title and favorite_one_platform:
        personal_favorites.append(
            PersonalFavorite(title=favorite_one_title, platform=favorite_one_platform)
        )
    if favorite_two_title and favorite_two_platform:
        personal_favorites.append(
            PersonalFavorite(title=favorite_two_title, platform=favorite_two_platform)
        )
    if favorite_three_title and favorite_three_platform:
        personal_favorites.append(
            PersonalFavorite(
                title=favorite_three_title, platform=favorite_three_platform
            )
        )
    if favorite_four_title and favorite_four_platform:
        personal_favorites.append(
            PersonalFavorite(title=favorite_four_title, platform=favorite_four_platform)
        )
    if favorite_five_title and favorite_five_platform:
        personal_favorites.append(
            PersonalFavorite(title=favorite_five_title, platform=favorite_five_platform)
        )

    current_conditions = CurrentConditions(
        season=season_input,
        holiday=holiday_input,
        occasion=occasion_input,
        audience=audience_input,
        weather=weather_input,
    )

    # get the viewing history section from the existing profile if it exists, otherwise create an empty list
    viewing_history = []
    for profile in viewer_profiles:
        if profile.registration_information.username == username:
            viewing_history = profile.viewing_history
            break

    # get the recommendations section from the existing profile if it exists, otherwise create an empty list
    recommendations = []
    for profile in viewer_profiles:
        if profile.registration_information.username == username:
            recommendations = profile.recommendations
            break

    viewer_profile = ViewerProfile(
        registration_information=registration,
        personalization=personalization_choice,
        demographic_information=demographic,
        viewing_preferences=viewing,
        viewing_history=viewing_history,
        personal_favorites=personal_favorites,
        current_conditions=current_conditions,
        recommendations=recommendations,
    )

    save_viewer_profile(viewer_profile)
    return viewer_profile.model_dump_json(indent=4)


def generate_viewer_description(
    viewer_profile: ViewerProfile, viewer_information_to_include: list[str]
) -> tuple[str, str]:

    personalization_data = {}
    for info in viewer_information_to_include:
        if info == "Demographics":
            personalization_data["demographic_information"] = (
                viewer_profile.demographic_information.model_dump_json()
            )
        elif info == "Viewing Preferences":
            personalization_data["viewing_preferences"] = (
                viewer_profile.viewing_preferences.model_dump_json()
            )
        elif info == "Personal Favorites":
            personalization_data["personal_favorites"] = [
                favorite.model_dump_json()
                for favorite in viewer_profile.personal_favorites
            ]
        elif info == "Current Conditions":
            personalization_data["current_conditions"] = (
                viewer_profile.current_conditions.model_dump_json()
            )
        elif info == "Viewing History":
            personalization_data["viewing_history"] = [
                history.model_dump_json() for history in viewer_profile.viewing_history
            ]

    viewer_description_prompt_template = f"""Based directly on the following information about the streaming media viewer information below and th guide to the sections of the viewer information, write a description of this viewer. The goal is to use the description to make personalized content recommendations for this viewer. The description should focus on the viewer's preferences, interests, and demographic information. The description should be written in a way that is easy to understand and captures the essence of the viewer's personality and viewing habits.
    # Important Notes:
    - Only return the description with no additional text, preamble, explanation, thinking, or reflection on the viewer's information.
    - Don't focus on which streaming platforms the viewer watched content previously, but rather the type of content they prefer to watch.
    - Include personal favorites as part of the description to help inform the recommendations.

    # Section Guide
    Guide to possible sections in the viewer_information data object:
    1. demographic_information: Information about the viewer's background, such as age, gender, and location.
    2. viewing_preferences: Information about the viewer's content preferences, such as favorite genres and themes.
    3. personal_favorites: Information about the viewer's favorite content.
    4. current_conditions: Information about the current context, such as season, holiday, or weather.
    5. viewing_history: Information about the viewer's past viewing behavior.

    # Viewer Information:
    {personalization_data}
"""

    logger.info(
        f"Viewer Description Prompt Template: {json.dumps(viewer_description_prompt_template)}"
    )
    viewer_description = personalization_agent(viewer_description_prompt_template)
    return personalization_data, str(viewer_description)


def generate_recommendations(
    viewer_description: str, recommendation_count: int
) -> list[Recommendation]:
    recommendations_prompt_template = f"""Based directly on the following description of the viewer in the <viewer_description> tags below, make {recommendation_count} personalized recommendation(s) for recent content on any of the popular streaming media platforms (e.g., Netflix, Hulu, Amazon Prime Video, YouTube, etc.):

    <viewer_description>
    {viewer_description}
    </viewer_description>

    Using the structured format provided, return a list of recommendations. Include the title, streaming platform on which the content can be viewed, URL of content, and brief description of the reason why you are recommending it to me.
    
    Important Notes:
    - Get the current date and time using the current_time tool before making recommendations.
    - Only return the recommendations in the structured format with no additional text, preamble, or explanation.
    - Search the Internet for relevant content and validate that the URLs actually work.
    - Always refer to the viewer in first person: "you," "your," and "yours."
    """
    logger.debug(f"Recommendations Prompt Template: {recommendations_prompt_template}")

    personalized_recommendations = personalization_agent(
        recommendations_prompt_template
    )
    logger.debug(f"Raw Recommendations from Agent: {personalized_recommendations}")

    personalized_recommendations = personalization_agent.structured_output(
        RecommendationList, str(personalized_recommendations)
    )
    logger.debug(
        f"Structured Recommendations: {personalized_recommendations.model_dump_json(indent=4)}"
    )

    return personalized_recommendations


def retrieve_viewer_description(
    viewer_profile_index: int,
    viewer_information_to_include: list[str],
) -> tuple[str, str]:
    viewer_profile = viewer_profiles[viewer_profile_index]
    logger.debug(f"Viewer Profile: {viewer_profile.model_dump_json(indent=4)}")

    logger.info(f"Personalization Level: {viewer_information_to_include}")
    personalization_data, viewer_description = generate_viewer_description(
        viewer_profile, viewer_information_to_include
    )
    logger.debug(f"Viewer Description: {viewer_description}")

    return (
        personalization_data,
        viewer_description,
    )


def retrieve_recommendations(
    viewer_description: str, recommendation_count: int = 4
) -> str:
    if not viewer_description or "error" in viewer_description.lower():
        return "No valid viewer description available for recommendations."

    recommendations = generate_recommendations(viewer_description, recommendation_count)
    logger.debug(f"Recommendations: {recommendations.model_dump_json(indent=4)}")
    formatted_recommendations = ""
    for recommendation in recommendations.recommendations:
        formatted_recommendations += (
            f"![Coming Soon!](/gradio_api/file=assets/coming_soon.jpg)\n"
            f"## {recommendation.title}\n\n"
            f"**Available on:** {recommendation.streaming_platform}  \n"
            f"**Link:** [Watch here]({recommendation.url})  \n"
            f"**Why Recommended:** {recommendation.reason}  \n\n"
            f"---\n\n"
        )
    return formatted_recommendations


def retrieve_recommendations_to_grid(
    viewer_description: str, recommendation_count: int = 4
) -> str:
    if not viewer_description or "error" in viewer_description.lower():
        return "No valid viewer description available for recommendations."
    recommendations = generate_recommendations(viewer_description, recommendation_count)
    recommendations = json.dumps(
        [
            recommendation.model_dump()
            for recommendation in recommendations.recommendations
        ],
        indent=4,
    )

    logger.debug(f"Recommendations as JSON: {recommendations}")

    return recommendations


def retrieve_viewer_profile(username: str) -> tuple[str, str]:
    # search for the user in viewer_profiles
    logger.info(f"Username: {username}")
    if username:
        for profile in viewer_profiles:
            if profile.registration_information.username == username:
                return (
                    profile.model_dump_json(),
                    profile.registration_information.first_name,
                )
    return "{}", ""


def chat_with_agent(
    history: list, recommendation_count: int = 2
) -> list[Recommendation]:
    if not history:
        return list[Recommendation]()

    for event in history:
        event.pop("metadata", None)
        event.pop("options", None)

    recommendations_prompt_template = f"""Based directly on chat history in the <chat_history> tags below, make {recommendation_count} personalized recommendation(s) for recent content on any of the popular streaming media platforms (e.g., Netflix, Hulu, Amazon Prime Video, YouTube, etc.):

<chat_history>
{json.dumps(history, indent=4)}
</chat_history>

Using the structured format provided, return a list of recommendations. Include the title, streaming platform on which the content can be viewed, URL of content, and brief description of the content.

Important Notes:
- Get the current date and time using the current_time tool before making recommendations.
- Only return the answer with no additional text, preamble, or explanation.
- Search the Internet for relevant content and validate that the URLs actually work.
    """

    logger.info(f"Recommendations Prompt Template: {recommendations_prompt_template}")
    personalized_recommendations = personalization_agent(
        recommendations_prompt_template
    )
    try:
        personalized_recommendations = personalization_agent.structured_output(
            RecommendationList, str(personalized_recommendations)
        )

        formatted_recommendations = ""
        for recommendation in personalized_recommendations.recommendations:
            formatted_recommendations += (
                f"## {recommendation.title}\n\n"
                f"**Available on:** {recommendation.streaming_platform}  \n"
                f"**Link:** [Watch here]({recommendation.url})  \n"
                f"**Description:** {recommendation.reason}  \n\n"
            )
        return formatted_recommendations
    except ValidationError as e:
        logger.error(f"Error parsing recommendations from agent response: {e}")
        return personalized_recommendations.message.get(
            "content", "No recommendations received."
        )


def generate_welcome_message(request: gr.Request):
    # search for the user in viewer_profiles
    for idx, profile in enumerate(viewer_profiles):
        if profile.registration_information.username == request.username:
            return (
                f"Welcome, {profile.registration_information.first_name}",
                idx,
                profile.registration_information.first_name,
                profile.registration_information.last_name,
                profile.registration_information.username,
                profile.registration_information.password,
                profile.registration_information.email,
                profile.personalization,
                profile.demographic_information.gender,
                profile.demographic_information.age_group,
                profile.demographic_information.primary_language,
                profile.demographic_information.relationship_status,
                profile.demographic_information.income_range,
                profile.demographic_information.occupation,
                profile.demographic_information.country_region,
                profile.demographic_information.education_level,
                profile.demographic_information.ethnicity,
                profile.viewing_preferences.favorite_genres,
                profile.viewing_preferences.genres_to_avoid,
                profile.viewing_preferences.preferred_narrative_elements,
                profile.viewing_preferences.preferred_themes,
                profile.viewing_preferences.preferred_plots,
                profile.viewing_preferences.preferred_formats,
                profile.viewing_preferences.preferred_min_lengths,
                profile.viewing_preferences.ratings_to_avoid,
                profile.viewing_preferences.preferred_streaming_services,
                (
                    profile.personal_favorites[0].title
                    if len(profile.personal_favorites) > 0
                    else None
                ),
                (
                    profile.personal_favorites[0].platform
                    if len(profile.personal_favorites) > 0
                    else None
                ),
                (
                    profile.personal_favorites[1].title
                    if len(profile.personal_favorites) > 1
                    else None
                ),
                (
                    profile.personal_favorites[1].platform
                    if len(profile.personal_favorites) > 1
                    else None
                ),
                (
                    profile.personal_favorites[2].title
                    if len(profile.personal_favorites) > 2
                    else None
                ),
                (
                    profile.personal_favorites[2].platform
                    if len(profile.personal_favorites) > 2
                    else None
                ),
                (
                    profile.personal_favorites[3].title
                    if len(profile.personal_favorites) > 3
                    else None
                ),
                (
                    profile.personal_favorites[3].platform
                    if len(profile.personal_favorites) > 3
                    else None
                ),
                (
                    profile.personal_favorites[4].title
                    if len(profile.personal_favorites) > 4
                    else None
                ),
                (
                    profile.personal_favorites[4].platform
                    if len(profile.personal_favorites) > 4
                    else None
                ),
                profile.current_conditions.season,
                profile.current_conditions.holiday,
                profile.current_conditions.occasion,
                profile.current_conditions.audience,
                profile.current_conditions.weather,
                (
                    f"{profile.viewing_history[0].viewed_date} | {profile.viewing_history[0].format} | {profile.viewing_history[0].title} | {profile.viewing_history[0].platform} | {'👍' if profile.viewing_history[0].liked else '👎'}"
                    if len(profile.viewing_history) > 0
                    else None
                ),
                (
                    f"{profile.viewing_history[1].viewed_date} | {profile.viewing_history[1].format} | {profile.viewing_history[1].title} | {profile.viewing_history[1].platform} | {'👍' if profile.viewing_history[1].liked else '👎'}"
                    if len(profile.viewing_history) > 1
                    else None
                ),
                (
                    f"{profile.viewing_history[2].viewed_date} | {profile.viewing_history[2].format} | {profile.viewing_history[2].title} | {profile.viewing_history[2].platform} | {'👍' if profile.viewing_history[2].liked else '👎'}"
                    if len(profile.viewing_history) > 2
                    else None
                ),
                (
                    f"{profile.viewing_history[3].viewed_date} | {profile.viewing_history[3].format} | {profile.viewing_history[3].title} | {profile.viewing_history[3].platform} | {'👍' if profile.viewing_history[3].liked else '👎'}"
                    if len(profile.viewing_history) > 3
                    else None
                ),
                (
                    f"{profile.viewing_history[4].viewed_date} | {profile.viewing_history[4].format} | {profile.viewing_history[4].title} | {profile.viewing_history[4].platform} | {'👍' if profile.viewing_history[4].liked else '👎'}"
                    if len(profile.viewing_history) > 4
                    else None
                ),
                retrieve_generic_recommendations(),
            )
    return "User not found."


def authenticate_user(username, password):
    # if the username and password match from viewer_profiles then allow in
    for profile in viewer_profiles:
        if (
            profile.registration_information.username == username
            and profile.registration_information.password == password
        ):
            return True
    return False
