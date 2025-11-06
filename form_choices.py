class FormChoices:
    def __init__(self):
        pass

    @property
    def GENDERS(self):
        return [
            "Unspecified",
            "Male",
            "Female",
            "Other",
        ]

    @property
    def AGE_RANGES(self) -> list[str]:
        return [
            "Unspecified",
            "Under 18",
            "18-24",
            "25-34",
            "35-44",
            "45-54",
            "55-64",
            "65 and over",
        ]

    @property
    def LANGUAGES(self):
        return [
            "Unspecified",
            "Bengali",
            "English",
            "French",
            "German",
            "Hindi",
            "Indonesian",
            "Japanese",
            "Mandarin Chinese",
            "Portuguese",
            "Russian",
            "Spanish",
            "Standard Arabic",
            "Other",
        ]

    @property
    def RELATIONSHIP_STATUSES(self):
        return [
            "Unspecified",
            "Single",
            "In a Relationship",
            "Married",
            "Divorced",
            "Widowed",
        ]

    @property
    def INCOME_RANGES(self):
        return [
            "Unspecified",
            "No Income",
            "Under $25,000",
            "$25,000 - $49,999",
            "$50,000 - $74,999",
            "$75,000 - $99,999",
            "$100,000 - $149,999",
            "$150,000 - $199,999",
            "$200,000 and above",
        ]

    @property
    def OCCUPATIONS(self):
        return [
            "Unspecified",
            "Business & Finance",
            "Creative & Media",
            "Education",
            "Engineering",
            "Healthcare",
            "Legal",
            "Professional",
            "Retired",
            "Sales & Marketing",
            "Service & Retail",
            "Skilled Trades",
            "Student",
            "Technology",
            "Unemployed",
            "Other",
        ]

    @property
    def COUNTRIES(self):
        return [
            "Unspecified",
            "Argentina",
            "Australia",
            "Belgium",
            "Brazil",
            "Canada",
            "China",
            "France",
            "Germany",
            "India",
            "Indonesia",
            "Ireland",
            "Italy",
            "Japan",
            "Mexico",
            "Netherlands",
            "Poland",
            "Russia",
            "Saudi Arabia",
            "South Korea",
            "Spain",
            "Sweden",
            "Switzerland",
            "Taiwan",
            "Thailand",
            "Turkey",
            "United Kingdom",
            "United States",
            "Other",
        ]

    @property
    def EDUCATION_LEVELS(self):
        return [
            "Unspecified",
            "No Formal Education",
            "High School Diploma",
            "Some College",
            "Associate's Degree",
            "Bachelor's Degree",
            "Master's Degree",
            "Doctorate",
            "Postdoctoral",
            "Vocational Training",
            "Other",
        ]

    @property
    def ETHNICITIES(self):
        return [
            "Unspecified",
            "Asian",
            "Black or African",
            "White or European",
            "Hispanic or Latino",
            "Native American or Indigenous",
            "Pacific Islander",
            "Middle Eastern",
            "Mixed or Multiple ethnicities",
            "Other",
        ]

    @property
    def GENRES(self):
        return [
            "Action",
            "Adventure",
            "Animation",
            "Biographical/Biopic",
            "Comedy",
            "Crime/Mystery",
            "Dark Humor",
            "Disaster",
            "Documentary",
            "Drama",
            "Erotic",
            "Experimental",
            "Family",
            "Fantasy",
            "Historical",
            "Holiday",
            "Horror",
            "Martial Arts",
            "Musical",
            "Mystery",
            "Noir",
            "Psychological",
            "Religious/Spiritual",
            "Romance-Comedy (Rom-Com)",
            "Romance",
            "Satire",
            "Sci-Fi/Fantasy",
            "Sports",
            "Superhero",
            "Suspense",
            "Teen/Young Adult",
            "Thriller",
            "War",
            "Western",
            "Zombie",
        ]

    @property
    def NARRATIVE_ELEMENTS(self):
        return [
            "Allegory",
            "Character-Driven",
            "Cliffhanger Endings",
            "Dark & Gritty",
            "Descriptive Atmosphere",
            "Emotional & Heartfelt",
            "Epiphanies",
            "First-Person or Multiple Viewpoints",
            "Flashbacks and Flash-Forwards",
            "Foreshadowing",
            "Frame Stories (Story Within a Story)",
            "Inner Monologue",
            "Inspiring & Uplifting",
            "Irony",
            "Lighthearted & Fun",
            "Metafiction",
            "Multiple Story Arcs",
            "Nonlinear Timelines",
            "Nostalgic & Reflective",
            "Plot Twists",
            "Red Herrings",
            "Relaxing & Escapist",
            "Shifting Perspectives",
            "Stream of Consciousness",
            "Surprise Reveals",
            "Surreal & Abstract",
            "Suspenseful & Thrilling",
            "Symbolism",
            "Thought-Provoking & Dramatic",
            "Unreliable Narrator",
            "Use of coincidence and fate",
            "Whimsical & Quirky",
        ]

    @property
    def THEMES(self):
        return [
            "Adventure & Exploration",
            "Betrayal",
            "Class & Social Status",
            "Courage & Heroism",
            "Destiny & Fate",
            "Family Bonds",
            "Freedom & Oppression",
            "Friendship",
            "Guilt & Redemption",
            "Happiness",
            "Hard Work",
            "Health & Illness",
            "Heartbreak",
            "Humor & Satire",
            "Identity & Self-Discovery",
            "Immigration & Displacement",
            "Immortality",
            "Imperialism",
            "Impossibility",
            "Individuality",
            "Justice",
            "Legal Injustice",
            "Life",
            "Loneliness & Isolation",
            "Loss & Grief",
            "Loss of Humanity Through Technology",
            "Love & Romance",
            "Loyalty",
            "Madness",
            "Magic & Supernatural Forces",
            "Man vs. Nature",
            "Man vs. Self",
            "Man vs. Society",
            "Manipulation",
            "Mystery & Suspense",
            "Personal Growth & Transformation",
            "Political Intrigue",
            "Power & Corruption",
            "Pursuit of Love",
            "Redemption",
            "Religion & Spirituality",
            "Revenge",
            "Sacrificial Love",
            "Social Commentary",
            "Survival",
            "Technology & the Digital Age",
            "The American Dream",
            "The Environment",
            "War & Peace",
        ]

    @property
    def PLOT_ELEMENTS(self):
        return [
            "Atmosphere/Tone",
            "Beautiful Cinematography",
            "Character Development",
            "Climax",
            "Complex Characters",
            "Conflict",
            "Crisis Moment",
            "Dialogue",
            "Exposition",
            "Falling Action",
            "Fast-Paced Plot",
            "Flashbacks",
            "Foreshadowing",
            "Humor",
            "Inciting Incident",
            "Narrative Arc",
            "Obstacles/Increased Stakes",
            "Pacing",
            "Point of View",
            "Progressive Complications",
            "Resolution/Denouement",
            "Rising Action",
            "Satisfying Ending",
            "Setting",
            "Strong Emotional Impact",
            "Subplots",
            "Symbolism",
            "Theme",
            "Thought-Provoking Story",
            "Turning Point",
        ]

    @property
    def CONTENT_FORMAT(self):
        return [
            "Animated film",
            "Anthology series",
            "Behind-the-scenes",
            "Commentary track",
            "Documentary",
            "Dramedy",
            "Episodic series",
            "Fan edit",
            "Feature film",
            "Game show",
            "Let's Play",
            "Livestream",
            "Machinima",
            "Miniseries",
            "Music video",
            "Parody",
            "Podcast",
            "Reaction video",
            "Reality show",
            "Review",
            "Short film",
            "Sitcom",
            "Sketch comedy",
            "Soap opera",
            "Talk show",
            "Teaser",
            "Trailer",
            "Tutorial",
            "TV special",
            "Unboxing",
            "Vlog",
            "Web series",
        ]

    @property
    def DURATIONS(self):
        return [
            "Under 5 minutes",
            "10-15 minutes",
            "30 minutes",
            "60 minutes",
            "90 minutes",
            "Over 90 minutes",
        ]

    @property
    def RATINGS(self):
        return [
            "G - General Audiences",
            "PG - Parental Guidance",
            "PG-13 - Parents Strongly Cautioned",
            "R - Restricted",
            "NC-17 - Adults Only",
        ]

    @property
    def STREAMING_SERVICES(self):
        return [
            "Unspecified/Unknown",
            "Amazon Prime Video",
            "Apple TV+",
            "Crunchyroll",
            "Dailymotion",
            "Disney+",
            "Facebook Watch",
            "FuboTV",
            "Hulu",
            "Instagram",
            "HBO Max",
            "Netflix",
            "Paramount+",
            "Peacock",
            "Pluto TV",
            "Sling TV",
            "TikTok",
            "Tubi",
            "Twitch",
            "Vimeo",
            "YouTube",
        ]

    @property
    def HOLIDAY(self):
        return [
            "Unspecified",
            "Christmas",
            "New Year's Day",
            "Thanksgiving",
            "Halloween",
            "Valentine's Day",
            "July 4th",
            "Memorial Day",
            "Easter",
            "Hanukkah",
        ]

    @property
    def SEASONS(self):
        return [
            "Unspecified",
            "Spring",
            "Summer",
            "Fall",
            "Winter",
        ]

    @property
    def OCCASION(self):
        return [
            "Unspecified",
            "Birthday",
            "Anniversary",
            "Graduation",
            "Promotion",
            "Retirement",
        ]

    @property
    def AUDIENCE(self):
        return [
            "Unspecified",
            "Kids",
            "Teens",
            "Adults",
            "Family",
            "Friends",
            "Couples",
            "Date Night",
            "Solo",
        ]

    @property
    def WEATHER(self):
        return [
            "Unspecified",
            "Sunny",
            "Rainy",
            "Snowy",
            "Cloudy",
        ]
