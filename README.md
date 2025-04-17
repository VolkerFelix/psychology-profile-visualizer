# Psychology Profile Visualizer

A Flask web application that guides users through a psychological assessment questionnaire and visualizes their personality profile, sleep preferences, and behavioral patterns.

## Features

- **Interactive Questionnaire Flow**: Multi-step questionnaire covering personality traits, sleep preferences, and behavioral patterns
- **Dynamic Visualizations**: Radar charts, bar graphs, and other visualizations to represent psychological profiles
- **Personalized Insights**: Custom insights and observations based on assessment results
- **Responsive Design**: Works on desktop and mobile devices
- **API Integration**: Connects to the psychology-service backend for questionnaire data and profile generation

## Screenshots

![Landing Page](screenshots/landing-page.png)
![Questionnaire](screenshots/questionnaire.png)
![Profile Visualization](screenshots/profile-visualization.png)

## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Visualization**: Plotly.js
- **Styling**: Custom CSS with Bootstrap components
- **API Integration**: Requests library for communicating with the psychology-service

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/psychology-profile-visualizer.git
   cd psychology-profile-visualizer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following content:
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_APP=run.py
   FLASK_ENV=development
   PSYCHOLOGY_API_BASE_URL=http://localhost:8001/api
   ```

## Running the Application

1. Start the Flask development server:
   ```
   flask run
   ```
   or
   ```
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

## Testing the API Connection

You can test the connection to the psychology-service API using the provided test script:

```
python -m app.utils.test_api
```

This will verify that the application can successfully connect to the API and retrieve questionnaire data.

## Project Structure

```
psychology-profile-visualizer/
├── app/                          # Application package
│   ├── __init__.py               # Flask app initialization
│   ├── static/                   # Static files (CSS, JS, images)
│   ├── templates/                # HTML templates
│   ├── models/                   # Data models
│   ├── utils/                    # Utility functions
│   │   ├── api_client.py         # API client for psychology-service
│   │   └── test_api.py           # API connection test script
│   └── routes/                   # Flask route definitions
├── config.py                     # Configuration settings
├── requirements.txt              # Project dependencies
├── run.py                        # Application entry point
└── README.md                     # This file
```

## How It Works

1. **Onboarding Flow**: Users complete a series of questionnaires covering personality traits (based on the Big Five model), sleep preferences, and behavioral patterns.

2. **API Integration**: The application fetches questionnaire data from the psychology-service API and submits responses for processing.

3. **Data Processing**: The application scores and processes the responses using psychological assessment algorithms, either from the API or locally if the API is unavailable.

4. **Profile Generation**: A comprehensive psychological profile is created with insights into the user's dominant traits, strengths, challenges.

5. **Visualization**: Interactive charts and graphics display the profile results in an intuitive and engaging format.

## Psychological Assessment Basis

The assessment is based on established psychological frameworks:

- **Personality Traits**: Based on the Big Five personality model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- **Sleep Assessment**: Evaluates chronotype, environment preferences, and sleep anxiety
- **Behavioral Patterns**: Examines routine consistency, exercise habits, social preferences, and digital behaviors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- Built with inspiration from the Psychology Profiling Microservice architecture
- Personality assessment based on established psychological research
- Visualization techniques designed to make complex psychological data understandable