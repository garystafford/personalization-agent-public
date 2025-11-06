import json
import logging
import sys

import gradio as gr
from gradio.themes import Base, GoogleFont

import utilities
from data import Recommendation
from form_choices import FormChoices

# Basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

form_choices = FormChoices()

with open(file="custom.css", mode="r", encoding="utf-8") as f:
    custom_css = f.read()

# Create the Gradio UI
with gr.Blocks(
    title="Personalized Recommendations Agent",
    css=custom_css,
    theme=Base(font=[GoogleFont("Inter"), "Arial", "sans-serif"], primary_hue="blue"),
    fill_width=True,
) as demo:
    welcome_message = gr.Markdown()
    username_hidden = gr.Textbox(visible=False)

    gr.HTML(
        """<div class="form title">
                <div class="image">
                    <img src="/gradio_api/file=assets/personalization.png" width='75px' height='auto' style="padding-right: 12px;">
                </div>
                <div>
                    <h1>Personalized Recommendations Agent</h1>
                </div>
            </div>
            <div class="subtitle form">
                Discover personalized recommendations perfectly matched to your tastes using advanced AI and your unique viewing profile. Simply provide your preferences and favorites, and get smart suggestions for content you’ll love, on all your favorite streaming platforms.
            </div>"""
    )
    with gr.Tab("Start Watching", id="currently_trending"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## Start Watching", elem_classes="blue-text")
                gr.Markdown(
                    "View some of the hottest content currently trending on major streaming platforms."
                )
                currently_trending_output = gr.Markdown(
                    label="Recommendations",
                    visible=False,
                )

                @gr.render(inputs=[currently_trending_output])
                def current_trending(recommendations_json_string):
                    if not recommendations_json_string:
                        return "<p style='color: gray;'>No current recommendations available.</p>"
                    logger.debug(
                        f"Received recommendations JSON string: {recommendations_json_string}"
                    )
                    recommendations = json.loads(recommendations_json_string)
                    recommendations = [
                        Recommendation.model_validate(rec) for rec in recommendations
                    ]
                    logger.debug(f"Validated recommendations data: {recommendations}")
                    cards_html = ""
                    for recommendation in recommendations:
                        cards_html += f"""<div class="card">
                            <img class="main-img" src="gradio_api/file=assets/coming_soon.jpg" alt="{recommendation.title}">
                            <div class="title">{recommendation.title}</div>
                            <div class="platform">{recommendation.streaming_platform}</div>
                            <div class="reason">{recommendation.reason}</div>
                            <div class="card-footer">
                                <div><a class="link" href="{recommendation.url}" target="_blank">Watch Now</a></div>
                            </div>
                        </div>"""

                    start_html = """<div class="recommendations-container"><div class="grid" id="recommendationsGrid">"""
                    end_html = """</div></div>"""
                    html = f"{start_html}{cards_html}{end_html}"
                    gr.HTML(html)

    with gr.Tab("Viewer Profile", id="viewer_information", elem_classes="form"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## Viewer Profile", elem_classes="blue-text")
                gr.Markdown(
                    "To get personalized content recommendations, complete each section of the form with information about your preferences, background, and favorites. The more detail you share, the more accurate and relevant your recommendations will be.",
                    min_height="85px",
                )
                with gr.Tab("1. Registration", id="registration_information"):
                    gr.Markdown(
                        "Enter your basic information such as first name, last name, username, password, and email address. This helps create your user profile and ensures security and communication."
                    )
                    first_name_input = gr.Textbox(
                        label="First Name",
                        type="text",
                        placeholder="Required",
                    )
                    last_name_input = gr.Textbox(
                        label="Last Name",
                        type="text",
                        placeholder="Required",
                    )
                    username_input = gr.Textbox(
                        label="Username",
                        type="text",
                        placeholder="Required",
                    )
                    password_input = gr.Textbox(
                        label="Password",
                        type="password",
                        lines=1,
                        max_lines=1,
                        placeholder="Required",
                    )
                    email_input = gr.Textbox(
                        label="Email",
                        type="email",
                        lines=1,
                        max_lines=1,
                        placeholder="Required",
                    )
                    personalization_choice = gr.Checkbox(
                        label="Personalization?",
                    )
                with gr.Tab("2. Demographics", id="demographic_information"):
                    gr.Markdown(
                        "Select details like your gender, age range, primary language, relationship status, income range, occupation, country or region, education level, and ethnicity. These fields help tailor recommendations to your background and preferences."
                    )
                    gender_input = gr.Dropdown(
                        label="Gender",
                        choices=form_choices.GENDERS,
                        # info="Select your gender",
                        multiselect=False,
                    )
                    age_input = gr.Dropdown(
                        label="Age Range",
                        choices=form_choices.AGE_RANGES,
                        # info="Select your age group",
                        multiselect=False,
                    )
                    primary_language_input = gr.Dropdown(
                        label="Preferred Language",
                        choices=form_choices.LANGUAGES,
                        # info="Select your preferred language",
                        multiselect=False,
                    )
                    relationship_status_input = gr.Dropdown(
                        label="Relationship Status",
                        choices=form_choices.RELATIONSHIP_STATUSES,
                        # info="Select your relationship status",
                        multiselect=False,
                    )
                    income_input = gr.Dropdown(
                        label="Income Range",
                        choices=form_choices.INCOME_RANGES,
                        # info="Select your income range",
                        multiselect=False,
                    )
                    occupation_input = gr.Dropdown(
                        label="Occupation",
                        choices=form_choices.OCCUPATIONS,
                        # info="Select your occupation",
                        multiselect=False,
                    )
                    country_input = gr.Dropdown(
                        label="Country/Region",
                        choices=form_choices.COUNTRIES,
                        # info="Select your country or region",
                        multiselect=False,
                    )
                    education_level_input = gr.Dropdown(
                        label="Education Level",
                        choices=form_choices.EDUCATION_LEVELS,
                        # info="Select your education level",
                        multiselect=False,
                    )
                    ethnicity_input = gr.Dropdown(
                        label="Ethnicity/Race",
                        choices=form_choices.ETHNICITIES,
                        # info="Select your ethnic/racial category",
                        multiselect=False,
                    )
                with gr.Tab("3. Viewing Preferences", id="viewing_preferences"):
                    gr.Markdown(
                        "Choose your favorite genres, genres to avoid, preferred narrative elements, themes, plot elements, content formats, content durations, ratings to avoid, and favorite streaming services. The more preferences you share, the better the system can match you with relevant content."
                    )
                    favorite_genres_input = gr.Dropdown(
                        label="Favorite Genres",
                        choices=form_choices.GENRES,
                        info="Choose up to 3 of your favorite genres",
                        multiselect=True,
                        max_choices=3,
                    )
                    genres_to_avoid_input = gr.Dropdown(
                        label="Genres to Avoid",
                        choices=form_choices.GENRES,
                        info="Choose up to 2 genres you want to avoid",
                        multiselect=True,
                        max_choices=2,
                    )
                    narrative_elements_input = gr.Dropdown(
                        label="Preferred Narrative Elements",
                        choices=form_choices.NARRATIVE_ELEMENTS,
                        info="Choose up to 2 narrative elements you enjoy",
                        multiselect=True,
                        max_choices=2,
                    )
                    preferred_themes_input = gr.Dropdown(
                        label="Preferred Themes",
                        choices=form_choices.THEMES,
                        info="Choose up to 2 themes you enjoy",
                        multiselect=True,
                        max_choices=2,
                    )
                    preferred_plots_input = gr.Dropdown(
                        label="Preferred Plot Elements",
                        choices=form_choices.PLOT_ELEMENTS,
                        info="Choose up to 2 plot elements you enjoy",
                        multiselect=True,
                        max_choices=2,
                    )
                    preferred_formats_input = gr.Dropdown(
                        label="Preferred Content Formats",
                        choices=form_choices.CONTENT_FORMAT,
                        info="Choose up to 5 content formats you enjoy",
                        multiselect=True,
                        max_choices=5,
                    )
                    preferred_min_lengths_input = gr.Dropdown(
                        label="Preferred Durations",
                        choices=form_choices.DURATIONS,
                        info="Choose up to 3 content lengths you enjoy",
                        multiselect=True,
                        max_choices=3,
                    )
                    avoid_ratings_input = gr.Dropdown(
                        label="Ratings to Avoid",
                        choices=form_choices.RATINGS,
                        # info="Choose up to 2 ratings to avoid",
                        multiselect=True,
                        max_choices=2,
                    )
                    preferred_streaming_services_input = gr.Dropdown(
                        label="Favorite Streaming Services",
                        choices=form_choices.STREAMING_SERVICES,
                        info="Choose up to 5 of your favorite streaming services",
                        multiselect=True,
                        max_choices=5,
                    )
                with gr.Tab("4. Personal Favorites", id="personal_favorites"):
                    gr.Markdown(
                        "List up to five favorite movies, shows, or other media titles. Sharing your top picks helps the system understand your tastes and improves the accuracy of your recommendations."
                    )
                    favorite_one_title_input = gr.Textbox(
                        label="Favorite #1",
                        type="text",
                        placeholder="e.g. Marry Poppins",
                    )
                    favorite_one_platform_input = gr.Dropdown(
                        label="Favorite #1 Platform",
                        choices=form_choices.STREAMING_SERVICES,
                        # info="Select the streaming service for your favorite title",
                        multiselect=False,
                        show_label=False,
                    )
                    gr.Markdown("---")
                    favorite_two_title_input = gr.Textbox(
                        label="Favorite #2",
                        type="text",
                        placeholder="e.g. The Godfather",
                    )
                    favorite_two_platform_input = gr.Dropdown(
                        label="Favorite #2 Platform",
                        choices=form_choices.STREAMING_SERVICES,
                        # info="Select the streaming service for your favorite title",
                        multiselect=False,
                        show_label=False,
                    )
                    gr.Markdown("---")
                    favorite_three_title_input = gr.Textbox(
                        label="Favorite #3",
                        type="text",
                        placeholder="e.g. Friends",
                    )
                    favorite_three_platform_input = gr.Dropdown(
                        label="Favorite #3 Platform",
                        choices=form_choices.STREAMING_SERVICES,
                        # info="Select the streaming service for your favorite title",
                        multiselect=False,
                        show_label=False,
                    )
                    gr.Markdown("---")
                    favorite_four_title_input = gr.Textbox(
                        label="Favorite #4",
                        type="text",
                        placeholder="e.g. The Sopranos",
                    )
                    favorite_four_platform_input = gr.Dropdown(
                        label="Favorite #4 Platform",
                        choices=form_choices.STREAMING_SERVICES,
                        # info="Select the streaming service for your favorite title",
                        multiselect=False,
                        show_label=False,
                    )
                    gr.Markdown("---")
                    favorite_five_title_input = gr.Textbox(
                        label="Favorite #5",
                        type="text",
                        placeholder="e.g. The Office",
                    )
                    favorite_five_platform_input = gr.Dropdown(
                        label="Favorite #5 Platform",
                        choices=form_choices.STREAMING_SERVICES,
                        # info="Select the streaming service for your favorite title",
                        multiselect=False,
                        show_label=False,
                    )
                with gr.Tab("5. Current Conditions", id="real_time_conditions"):
                    gr.Markdown(
                        "Provide information about your current viewing context. This helps the system tailor recommendations based on your immediate environment."
                    )
                    season_input = gr.Dropdown(
                        label="Season",
                        choices=form_choices.SEASONS,
                    )
                    holiday_input = gr.Dropdown(
                        label="Holiday",
                        choices=form_choices.HOLIDAY,
                    )
                    occasion_name_input = gr.Dropdown(
                        label="Occasion",
                        choices=form_choices.OCCASION,
                    )
                    audience_input = gr.Dropdown(
                        label="Audience",
                        choices=form_choices.AUDIENCE,
                    )
                    weather_input = gr.Dropdown(
                        label="Weather",
                        choices=form_choices.WEATHER,
                    )
                with gr.Tab("6. Viewing History", id="viewing_history"):
                    gr.Markdown(
                        "Your most recent viewing history. This helps the system understand your past preferences and improve future recommendations."
                    )
                    viewing_history_input_1 = gr.Textbox(
                        label="Viewing History #1",
                        show_label=False,
                        placeholder="List your past watched titles...",
                        interactive=False,
                    )
                    viewing_history_input_2 = gr.Textbox(
                        label="Viewing History #2",
                        show_label=False,
                        placeholder="List your past watched titles...",
                        interactive=False,
                    )
                    viewing_history_input_3 = gr.Textbox(
                        label="Viewing History #3",
                        show_label=False,
                        placeholder="List your past watched titles...",
                        interactive=False,
                    )
                    viewing_history_input_4 = gr.Textbox(
                        label="Viewing History #4",
                        show_label=False,
                        placeholder="List your past watched titles...",
                        interactive=False,
                    )
                    viewing_history_input_5 = gr.Textbox(
                        label="Viewing History #5",
                        show_label=False,
                        placeholder="List your past watched titles...",
                        interactive=False,
                    )
        with gr.Row(elem_classes="form"):
            with gr.Column(
                scale=1,
            ):
                save_viewer_profile_button = gr.Button(
                    "Save Viewer Profile", variant="primary"
                )
                output_text = gr.Textbox(
                    label="Preview",
                    lines=10,
                    max_lines=20,
                    interactive=False,
                    show_copy_button=True,
                    value="Your viewer profile information will appear here after saving.",
                )
    with gr.Tab("Recommendations", id="recommendations"):
        with gr.Row():
            with gr.Column(scale=1, elem_classes="form"):
                gr.Markdown("## Recommendations", elem_classes="blue-text")
                gr.Markdown(
                    "Generate a unique viewer description, summarizing your interests, habits, and background. This provides a clear snapshot of who you are as a viewer, helping guide the recommendation process. Based on your viewer description, personalized recommendations are tailored to your unique tastes and preferences, making it easier for you to discover new content you'll love.",
                )
                viewer_profile_names = [
                    (
                        user.registration_information.full_name,
                        idx,
                    )
                    for idx, user in enumerate(utilities.viewer_profiles)
                ]
                logger.debug(f"Viewer profiles loaded: {viewer_profile_names}")

                with gr.Accordion("1. Configure Personalization", open=True):
                    viewer_profile_section = gr.Dropdown(
                        label="Viewer",
                        choices=viewer_profile_names,
                        value=viewer_profile_names[1][1],
                        multiselect=False,
                        interactive=True,
                    )
                    viewer_information_to_include = gr.CheckboxGroup(
                        [
                            "Demographics",
                            "Viewing Preferences",
                            "Personal Favorites",
                            "Current Conditions",
                            "Viewing History",
                        ],
                        value=[
                            "Demographics",
                            "Viewing Preferences",
                            "Personal Favorites",
                            "Current Conditions",
                            "Viewing History",
                        ],
                        label="Viewer Information to Include",
                        info="Select viewer profile information to include when making recommendations",
                    )
                with gr.Accordion("2. Generate Viewer Description", open=True):
                    demo_personalization_data_output = gr.Textbox(
                        visible=False,
                    )
                    demo_viewer_description_button = gr.Button(
                        "Generate Viewer Description", variant="primary"
                    )

                    demo_viewer_description_output = gr.Textbox(
                        label="Viewer Description",
                        show_label=False,
                        show_copy_button=True,
                        lines=5,
                        max_lines=20,
                        value="Viewer description will appear here...",
                    )
        with gr.Row():
            with gr.Column(scale=1, elem_classes="form", show_progress=True):
                with gr.Accordion("3. Generate Recommendations", open=True):
                    recommendation_count_value = gr.Slider(
                        label="Number of Recommendations",
                        minimum=1,
                        maximum=8,
                        value=4,
                        step=1,
                    )
                    demo_recommendations_button = gr.Button(
                        "Generate Recommendations", variant="primary"
                    )
                    demo_recommendations_output = gr.Markdown(
                        label="Recommendations",
                        visible=False,
                    )

        @gr.render(inputs=[demo_recommendations_output])
        def dynamic_display(recommendations_json_string):
            if not recommendations_json_string:
                html = "<p style='color: gray;'>Your personalized recommendations will appear here...</p>"
            else:
                recommendations = json.loads(recommendations_json_string)
                logger.debug(f"Recommendations JSON data loaded: {recommendations}")
                recommendations = [
                    Recommendation.model_validate(rec) for rec in recommendations
                ]

                logger.debug(f"Validated recommendations data: {recommendations}")
                cards_html = ""
                for recommendation in recommendations:
                    cards_html += f"""<div class="card">
                        <img class="main-img" src="gradio_api/file=assets/coming_soon.jpg" alt="{recommendation.title}">
                        <div class="title">{recommendation.title}</div>
                        <div class="platform">{recommendation.streaming_platform}</div>
                        <div class="reason">{recommendation.reason}</div>
                        <div class="card-footer">
                            <div><a class="link" href="{recommendation.url}" target="_blank">Watch Now</a></div>
                        </div>
                    </div>"""
                start_html = """<div class="recommendations-container"><h1 class="recommendations-title">Your Recommendations</h1><div class="grid" id="recommendationsGrid">"""
                end_html = """</div></div>"""
                html = f"{start_html}{cards_html}{end_html}"
            gr.HTML(html)

    with gr.Tab(label="Content Concierge", id="chatbot", elem_classes="form"):
        gr.Markdown("## Content Concierge", elem_classes="blue-text")
        gr.Markdown(
            "Interact with the Personalized Recommendations Agent through a conversational chatbot interface. Ask for viewing recommendations.",
        )
        with gr.Row():
            with gr.Column(scale=1, elem_classes="form", show_progress=True):
                chatbot = gr.Chatbot(
                    type="messages",
                    min_height=300,
                    max_height=900,
                    elem_id="chatbot",
                    # avatar_images=["user.png", "bot.png"],
                    resizable=True,
                    # feedback_options=["Like", "Dislike"],
                    # feedback_value=["Like", "Dislike"],
                    layout="bubble",
                )
                chat_msg = gr.Textbox(
                    label="User Message",
                    show_label=False,
                    placeholder="Ask for recommendations (e.g., 'What should I watch tonight?')",
                    interactive=True,
                    submit_btn=True,
                    elem_classes="message-input",
                )

            def user(user_message, history: list):
                return "", history + [{"role": "user", "content": user_message}]

            def bot(history: list):
                history.append(
                    {
                        "role": "assistant",
                        "content": str(utilities.chat_with_agent(history)),
                    }
                )
                logger.debug(f"Chat history updated: {history}")
                return history

    with gr.Tab("System Status", id="system-overview", elem_classes="form"):
        gr.Markdown("## System Status", elem_classes="blue-text")
        with gr.Row():
            with gr.Column(scale=1):
                model_status_output = gr.Markdown(
                    value=utilities.check_agent_health(),
                    elem_id="config-info",
                )
                refresh_status_button = gr.Button("Refresh Status", variant="primary")
        refresh_status_button.click(
            fn=utilities.check_agent_health,
            inputs=None,
            outputs=model_status_output,
        )
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("[Log out](/logout)")

    # ----- Button Handlers -----
    chat_msg.submit(
        fn=user, inputs=[chat_msg, chatbot], outputs=[chat_msg, chatbot], queue=False
    ).then(fn=bot, inputs=[chatbot], outputs=chatbot)

    demo_viewer_description_button.click(
        fn=utilities.retrieve_viewer_description,
        inputs=[
            viewer_profile_section,
            viewer_information_to_include,
        ],
        outputs=[
            demo_personalization_data_output,
            demo_viewer_description_output,
        ],
    )

    demo_recommendations_button.click(
        fn=utilities.retrieve_recommendations_to_grid,
        inputs=[demo_viewer_description_output, recommendation_count_value],
        outputs=[
            demo_recommendations_output,
        ],
        show_progress="full",
    )

    save_viewer_profile_button.click(
        fn=utilities.create_viewer_profile,
        inputs=[
            first_name_input,
            last_name_input,
            username_input,
            password_input,
            email_input,
            personalization_choice,
            gender_input,
            age_input,
            primary_language_input,
            relationship_status_input,
            income_input,
            occupation_input,
            country_input,
            education_level_input,
            ethnicity_input,
            favorite_genres_input,
            genres_to_avoid_input,
            narrative_elements_input,
            preferred_themes_input,
            preferred_plots_input,
            preferred_formats_input,
            preferred_min_lengths_input,
            avoid_ratings_input,
            preferred_streaming_services_input,
            favorite_one_title_input,
            favorite_one_platform_input,
            favorite_two_title_input,
            favorite_two_platform_input,
            favorite_three_title_input,
            favorite_three_platform_input,
            favorite_four_title_input,
            favorite_four_platform_input,
            favorite_five_title_input,
            favorite_five_platform_input,
            season_input,
            holiday_input,
            occasion_name_input,
            audience_input,
            weather_input,
        ],
        outputs=[output_text],
    )

    demo.load(
        utilities.generate_welcome_message,
        None,
        [
            welcome_message,
            viewer_profile_section,
            first_name_input,
            last_name_input,
            username_input,
            password_input,
            email_input,
            personalization_choice,
            gender_input,
            age_input,
            primary_language_input,
            relationship_status_input,
            income_input,
            occupation_input,
            country_input,
            education_level_input,
            ethnicity_input,
            favorite_genres_input,
            genres_to_avoid_input,
            narrative_elements_input,
            preferred_themes_input,
            preferred_plots_input,
            preferred_formats_input,
            preferred_min_lengths_input,
            avoid_ratings_input,
            preferred_streaming_services_input,
            favorite_one_title_input,
            favorite_one_platform_input,
            favorite_two_title_input,
            favorite_two_platform_input,
            favorite_three_title_input,
            favorite_three_platform_input,
            favorite_four_title_input,
            favorite_four_platform_input,
            favorite_five_title_input,
            favorite_five_platform_input,
            season_input,
            holiday_input,
            occasion_name_input,
            audience_input,
            weather_input,
            viewing_history_input_1,
            viewing_history_input_2,
            viewing_history_input_3,
            viewing_history_input_4,
            viewing_history_input_5,
            currently_trending_output,
        ],
    )

demo.queue()
demo.launch(
    allowed_paths=["./", "./images/"],
    auth=utilities.authenticate_user,
    auth_message="Please log in to access the Personalized Recommendations Agent.",
    favicon_path="favicon.ico",
)
