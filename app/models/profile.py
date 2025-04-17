"""
Profile model representing a user's psychological profile.
"""

class PsychologicalProfile:
    """Class representing a user's psychological profile."""
    
    def __init__(self, personality_traits=None, sleep_preferences=None, behavioral_patterns=None):
        """
        Initialize a new psychological profile.
        
        Args:
            personality_traits (dict): Dictionary of personality trait scores
            sleep_preferences (dict): Dictionary of sleep preferences
            behavioral_patterns (dict): Dictionary of behavioral patterns
        """
        self.personality_traits = personality_traits or {
            'openness': 0,
            'conscientiousness': 0,
            'extraversion': 0,
            'agreeableness': 0,
            'neuroticism': 0,
            'dominant_traits': []
        }
        
        self.sleep_preferences = sleep_preferences or {
            'chronotype': None,
            'ideal_bedtime': None,
            'environment_preference': None,
            'sleep_anxiety_level': 0,
            'relaxation_techniques': []
        }
        
        self.behavioral_patterns = behavioral_patterns or {
            'stress_response': None,
            'routine_consistency': 0,
            'exercise_frequency': 0,
            'social_activity_preference': 0,
            'screen_time_before_bed': 0
        }
        
        self.overall_profile = {}
        self._generate_overall_profile()
    
    def _generate_overall_profile(self):
        """Generate an overall profile with key insights."""
        # Initialize overall profile
        self.overall_profile = {
            'insights': [],
            'strengths': [],
            'challenges': [],
        }
        
        # Add personality insights
        self._add_personality_insights()
        
        # Add sleep insights
        self._add_sleep_insights()
        
        # Add behavioral insights
        self._add_behavioral_insights()
        
        # Add cross-dimensional insights
        self._add_cross_dimensional_insights()
    
    def _add_personality_insights(self):
        """Add insights based on personality traits."""
        # Find dominant traits (traits with scores >= 70)
        dominant_traits = []
        for trait, score in self.personality_traits.items():
            if trait != 'dominant_traits' and score >= 70:
                dominant_traits.append(trait)
        
        # Store dominant traits
        self.personality_traits['dominant_traits'] = dominant_traits
        
        # Add insights based on high trait scores
        if 'openness' in dominant_traits:
            self.overall_profile['strengths'].append('Open to new experiences and ideas')
            
        if 'conscientiousness' in dominant_traits:
            self.overall_profile['strengths'].append('Well-organized and disciplined')
            
        if 'extraversion' in dominant_traits:
            self.overall_profile['strengths'].append('Socially engaged and energetic')
            self.overall_profile['challenges'].append('May find it difficult to wind down before sleep')
            
        if 'agreeableness' in dominant_traits:
            self.overall_profile['strengths'].append('Cooperative and considerate of others')
            
        if 'neuroticism' in dominant_traits:
            self.overall_profile['challenges'].append('Tendency toward anxiety that may affect sleep')
    
    def _add_sleep_insights(self):
        """Add insights based on sleep preferences."""
        # Chronotype insights
        chronotype = self.sleep_preferences.get('chronotype')
        if chronotype == 'morning_person':
            self.overall_profile['insights'].append('Morning chronotype (early bird)')
        elif chronotype == 'evening_person':
            self.overall_profile['insights'].append('Evening chronotype (night owl)')
        elif chronotype == 'intermediate':
            self.overall_profile['insights'].append('Intermediate chronotype with balanced day/night preferences')
        
        # Sleep anxiety
        anxiety_level = self.sleep_preferences.get('sleep_anxiety_level', 0)
        if anxiety_level >= 7:
            self.overall_profile['challenges'].append('High sleep anxiety that may impact sleep quality')
        
        # Environment preference
        env_pref = self.sleep_preferences.get('environment_preference')
        if env_pref in ['some_noise', 'noise_and_light']:
            self.overall_profile['insights'].append('Comfortable with some ambient noise during sleep')
    
    def _add_behavioral_insights(self):
        """Add insights based on behavioral patterns."""
        # Stress response
        stress_response = self.behavioral_patterns.get('stress_response')
        if stress_response == 'problem_focused':
            self.overall_profile['strengths'].append('Practical approach to handling stress')
        elif stress_response == 'avoidant':
            self.overall_profile['challenges'].append('Tendency to avoid addressing stressors directly')
        
        # Routine consistency
        consistency = self.behavioral_patterns.get('routine_consistency', 0)
        if consistency >= 8:
            self.overall_profile['strengths'].append('Maintains consistent daily routines')
            self.overall_profile['insights'].append('Likely benefits from regular sleep schedule')
        elif consistency <= 3:
            self.overall_profile['challenges'].append('Variable daily routines may impact sleep regularity')
        
        # Screen time
        screen_time = self.behavioral_patterns.get('screen_time_before_bed', 0)
        if screen_time >= 60:
            self.overall_profile['challenges'].append('High screen time before bed may affect melatonin production')
        
        # Exercise frequency
        exercise = self.behavioral_patterns.get('exercise_frequency', 0)
        if exercise >= 4:
            self.overall_profile['strengths'].append('Regular exercise can contribute to better sleep quality')
        
        # Social activity preference
        social = self.behavioral_patterns.get('social_activity_preference', 0)
        if social >= 7:
            self.overall_profile['insights'].append('Prefers social activities in evening hours')
    
    def _add_cross_dimensional_insights(self):
        """Add insights that combine multiple dimensions."""
        # High neuroticism + high sleep anxiety
        if (self.personality_traits.get('neuroticism', 0) >= 70 and 
            self.sleep_preferences.get('sleep_anxiety_level', 0) >= 7):
            self.overall_profile['challenges'].append('Anxiety affects both daily life and sleep quality')
        
        # High conscientiousness + low routine consistency
        if (self.personality_traits.get('conscientiousness', 0) >= 70 and 
            self.behavioral_patterns.get('routine_consistency', 0) <= 3):
            self.overall_profile['insights'].append('Despite organizing tendencies, daily routines are variable')
        
        # Morning person + high screen time
        if (self.sleep_preferences.get('chronotype') == 'morning_person' and 
            self.behavioral_patterns.get('screen_time_before_bed', 0) >= 60):
            self.overall_profile['insights'].append('Morning person with high screen time before bed')
        
        # High extraversion + high social activity preference
        if (self.personality_traits.get('extraversion', 0) >= 70 and 
            self.behavioral_patterns.get('social_activity_preference', 0) >= 7):
            self.overall_profile['insights'].append('Strong social orientation in both personality and evening habits')
        
    def to_dict(self):
        """Convert profile to dictionary for JSON serialization."""
        return {
            'personality_traits': self.personality_traits,
            'sleep_preferences': self.sleep_preferences,
            'behavioral_patterns': self.behavioral_patterns,
            'overall_profile': self.overall_profile
        }