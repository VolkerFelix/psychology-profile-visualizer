"""
Questionnaire model with predefined questions based on the Psychology Profiling Microservice.
"""

# Define the sections of the questionnaire
SECTIONS = ['personality', 'sleep', 'behavioral']

def get_all_sections():
    """Get all questionnaire sections."""
    return SECTIONS

def get_questionnaire_by_section(section):
    """
    Get questions for a specific section of the questionnaire.
    
    Args:
        section (str): The section name ('personality', 'sleep', or 'behavioral')
        
    Returns:
        dict: A dictionary with section info and questions
    """
    sections = {
        'personality': {
            'title': 'Personality Traits',
            'description': 'These questions help us understand your core personality traits.',
            'questions': [
                {
                    'id': 'openness_1',
                    'text': 'I enjoy trying new experiences and activities',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'openness'
                },
                {
                    'id': 'openness_2',
                    'text': 'I am curious about many different things',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'openness'
                },
                {
                    'id': 'conscientiousness_1',
                    'text': 'I am organized and keep things neat',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'conscientiousness'
                },
                {
                    'id': 'conscientiousness_2',
                    'text': 'I plan ahead and follow through with my plans',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'conscientiousness'
                },
                {
                    'id': 'extraversion_1',
                    'text': 'I enjoy being around people and socializing',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'extraversion'
                },
                {
                    'id': 'extraversion_2',
                    'text': 'I am talkative and express my opinions freely',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'extraversion'
                },
                {
                    'id': 'agreeableness_1',
                    'text': 'I am considerate and kind to almost everyone',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'agreeableness'
                },
                {
                    'id': 'agreeableness_2',
                    'text': 'I like to cooperate with others',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'agreeableness'
                },
                {
                    'id': 'neuroticism_1',
                    'text': 'I worry about things frequently',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'neuroticism'
                },
                {
                    'id': 'neuroticism_2',
                    'text': 'I am easily stressed or anxious',
                    'description': 'Rate how much you agree with this statement',
                    'type': 'likert_5',
                    'dimension': 'neuroticism'
                }
            ]
        },
        'sleep': {
            'title': 'Sleep Preferences',
            'description': 'These questions help us understand your sleep patterns and preferences.',
            'questions': [
                {
                    'id': 'chronotype',
                    'text': 'When do you naturally prefer to go to sleep?',
                    'description': 'Select the time that best matches your preference, not when you actually go to bed',
                    'type': 'multiple_choice',
                    'dimension': 'chronotype',
                    'options': [
                        {'id': 'early', 'text': 'Early (before 10 PM)', 'value': 'morning_person'},
                        {'id': 'medium', 'text': 'Medium (10 PM - midnight)', 'value': 'intermediate'},
                        {'id': 'late', 'text': 'Late (after midnight)', 'value': 'evening_person'},
                        {'id': 'variable', 'text': 'It varies significantly day to day', 'value': 'variable'}
                    ]
                },
                {
                    'id': 'sleep_environment',
                    'text': 'What is your preferred sleep environment?',
                    'description': 'Select the environment that helps you sleep best',
                    'type': 'multiple_choice',
                    'dimension': 'sleep_environment',
                    'options': [
                        {'id': 'dark_quiet', 'text': 'Completely dark and quiet', 'value': 'dark_quiet'},
                        {'id': 'some_light', 'text': 'Some light (night light, dim lamp)', 'value': 'some_light'},
                        {'id': 'some_noise', 'text': 'Some noise (fan, white noise)', 'value': 'some_noise'},
                        {'id': 'noise_light', 'text': 'Both some noise and light', 'value': 'noise_and_light'}
                    ]
                },
                {
                    'id': 'sleep_anxiety',
                    'text': 'How often do you worry about not getting enough sleep?',
                    'description': 'Rate on a scale from 0 (never) to 10 (constantly)',
                    'type': 'slider',
                    'dimension': 'sleep_anxiety',
                    'min': 0,
                    'max': 10,
                    'step': 1
                },
                {
                    'id': 'ideal_bedtime',
                    'text': 'What is your ideal bedtime?',
                    'description': 'Select the time you would go to bed if you had complete control of your schedule',
                    'type': 'time',
                    'dimension': 'ideal_bedtime'
                },
                {
                    'id': 'relaxation_techniques',
                    'text': 'What relaxation techniques help you fall asleep?',
                    'description': 'Select all that apply',
                    'type': 'checkbox',
                    'dimension': 'relaxation_techniques',
                    'options': [
                        {'id': 'reading', 'text': 'Reading', 'value': 'reading'},
                        {'id': 'meditation', 'text': 'Meditation or breathing exercises', 'value': 'meditation'},
                        {'id': 'music', 'text': 'Listening to calming music or sounds', 'value': 'music'},
                        {'id': 'stretching', 'text': 'Stretching or gentle yoga', 'value': 'stretching'},
                        {'id': 'bath', 'text': 'Taking a warm bath or shower', 'value': 'bath'},
                        {'id': 'none', 'text': 'None of these', 'value': 'none'}
                    ]
                }
            ]
        },
        'behavioral': {
            'title': 'Behavioral Patterns',
            'description': 'These questions help us understand your daily habits and behavioral patterns.',
            'questions': [
                {
                    'id': 'stress_response',
                    'text': 'How do you typically respond to stress?',
                    'description': 'Select the option that best describes your usual response',
                    'type': 'multiple_choice',
                    'dimension': 'stress_response',
                    'options': [
                        {'id': 'problem', 'text': 'I try to solve the problem directly', 'value': 'problem_focused'},
                        {'id': 'emotion', 'text': 'I focus on managing my emotions', 'value': 'emotion_focused'},
                        {'id': 'social', 'text': 'I seek support from others', 'value': 'social_support'},
                        {'id': 'avoidant', 'text': 'I try to avoid thinking about it', 'value': 'avoidant'},
                        {'id': 'mixed', 'text': 'A mix of several approaches', 'value': 'mixed'}
                    ]
                },
                {
                    'id': 'routine_consistency',
                    'text': 'How consistent is your daily routine?',
                    'description': 'Rate on a scale from 0 (completely variable) to 10 (highly consistent)',
                    'type': 'slider',
                    'dimension': 'routine_consistency',
                    'min': 0,
                    'max': 10,
                    'step': 1
                },
                {
                    'id': 'exercise_frequency',
                    'text': 'How many days per week do you typically exercise?',
                    'description': 'Select the number that best represents your usual habits',
                    'type': 'slider',
                    'dimension': 'exercise_frequency',
                    'min': 0,
                    'max': 7,
                    'step': 1
                },
                {
                    'id': 'social_activity',
                    'text': 'How much do you prefer social activities before bedtime?',
                    'description': 'Rate on a scale from 0 (prefer solitude) to 10 (prefer socializing)',
                    'type': 'slider',
                    'dimension': 'social_activity_preference',
                    'min': 0,
                    'max': 10,
                    'step': 1
                },
                {
                    'id': 'screen_time',
                    'text': 'How many minutes do you typically spend on screens right before bed?',
                    'description': 'Enter approximate time in minutes',
                    'type': 'slider',
                    'dimension': 'screen_time_before_bed',
                    'min': 0,
                    'max': 120,
                    'step': 5
                }
            ]
        }
    }
    
    return sections.get(section, {'title': 'Unknown Section', 'description': '', 'questions': []})