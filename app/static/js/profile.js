/**
 * JavaScript for handling the psychological profile visualizations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fetch profile data from the server
    fetchProfileData().then(profileData => {
        if (profileData) {
            // Create visualizations
            createPersonalityRadarChart(profileData);
            highlightDominantTraits(profileData);
            createBehavioralBarChart(profileData);
            createSleepPreferencesChart(profileData);
        }
    });
});

/**
 * Fetch profile data from the server
 */
async function fetchProfileData() {
    try {
        const response = await fetch('/profile/data');
        if (!response.ok) {
            throw new Error('Failed to fetch profile data');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching profile data:', error);
        // Display error message to user
        document.getElementById('profileError').innerHTML = 
            `<div class="alert alert-danger" role="alert">
                Error loading profile data. Please try again or restart the assessment.
            </div>`;
        return null;
    }
}

/**
 * Create a radar chart for personality traits
 */
function createPersonalityRadarChart(profileData) {
    const personalityTraits = profileData.personality_traits;
    const chartElement = document.getElementById('personalityChart');
    
    if (!chartElement) return;
    
    // Extract data
    const traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism'];
    const values = [
        personalityTraits.openness || 0, 
        personalityTraits.conscientiousness || 0, 
        personalityTraits.extraversion || 0, 
        personalityTraits.agreeableness || 0, 
        personalityTraits.neuroticism || 0
    ];
    
    // Create radar chart
    const data = [{
        type: 'scatterpolar',
        r: values,
        theta: traits,
        fill: 'toself',
        fillcolor: 'rgba(54, 162, 235, 0.2)',
        line: {
            color: 'rgb(54, 162, 235)'
        }
    }];
    
    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 100]
            }
        },
        showlegend: false,
        margin: {
            l: 40,
            r: 40,
            b: 40,
            t: 10,
        }
    };
    
    Plotly.newPlot(chartElement, data, layout, {responsive: true});
}

/**
 * Highlight dominant personality traits
 */
function highlightDominantTraits(profileData) {
    const dominantTraitsElement = document.getElementById('dominantTraits');
    if (!dominantTraitsElement) return;
    
    const dominantTraits = profileData.personality_traits.dominant_traits || [];
    
    if (dominantTraits.length === 0) {
        dominantTraitsElement.innerHTML = '<p class="text-muted">No dominant traits identified</p>';
        return;
    }
    
    // Create list of dominant traits
    let html = '<ul class="list-group">';
    for (const trait of dominantTraits) {
        const score = profileData.personality_traits[trait];
        html += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                ${capitalize(trait)}
                <span class="badge bg-primary rounded-pill">${score}%</span>
            </li>
        `;
    }
    html += '</ul>';
    
    dominantTraitsElement.innerHTML = html;
}

/**
 * Create a bar chart for behavioral patterns
 */
function createBehavioralBarChart(profileData) {
    const behavioralChartElement = document.getElementById('behavioralChart');
    if (!behavioralChartElement) return;
    
    const patterns = profileData.behavioral_patterns;
    
    // Extract data
    const labels = [
        'Routine Consistency', 
        'Exercise Frequency', 
        'Social Preference', 
        'Screen Time (min)'
    ];
    
    const values = [
        patterns.routine_consistency || 0,
        patterns.exercise_frequency || 0,
        patterns.social_activity_preference || 0,
        patterns.screen_time_before_bed || 0
    ];
    
    // Normalize screen time for display (0-100 scale)
    if (values[3] > 0) {
        // 120 minutes max -> 100%
        values[3] = Math.min(100, Math.round((values[3] / 120) * 100));
    }
    
    // Create bar chart colors based on values
    const colors = values.map((value, index) => {
        // Different coloring logic for each metric
        if (index === 0) { // Routine consistency - higher is blue
            return `rgba(54, 162, 235, ${0.5 + (value/20)})`; 
        } else if (index === 1) { // Exercise - higher is green
            return `rgba(75, 192, 192, ${0.5 + (value/14)})`;
        } else if (index === 2) { // Social - neutral color
            return `rgba(153, 102, 255, ${0.5 + (value/20)})`;
        } else { // Screen time - higher is red (bad)
            return `rgba(255, 99, 132, ${0.5 + (value/200)})`;
        }
    });
    
    // Create the chart
    const data = [{
        type: 'bar',
        x: labels,
        y: values,
        marker: {
            color: colors
        }
    }];
    
    const layout = {
        title: {
            text: 'Behavioral Patterns',
            font: {
                size: 16
            }
        },
        yaxis: {
            range: [0, 100],
            title: 'Score'
        },
        margin: {
            l: 50,
            r: 20,
            b: 80,
            t: 50,
        }
    };
    
    // Only create this chart if the element exists on the page
    // This allows flexibility in the template
    if (behavioralChartElement) {
        Plotly.newPlot(behavioralChartElement, data, layout, {responsive: true});
    }
}

/**
 * Create a visualization for sleep preferences
 */
function createSleepPreferencesChart(profileData) {
    const sleepChartElement = document.getElementById('sleepChart');
    if (!sleepChartElement) return;
    
    const sleepPreferences = profileData.sleep_preferences;
    
    // Create a donut chart for chronotype
    let chronotypeValue = 25; // Default
    let chronotypeLabel = 'Unknown';
    let chronotypeColor = 'rgb(169, 169, 169)';
    
    if (sleepPreferences.chronotype === 'morning_person') {
        chronotypeValue = 20;
        chronotypeLabel = 'Morning Person';
        chronotypeColor = 'rgb(255, 159, 64)'; // Orange
    } else if (sleepPreferences.chronotype === 'evening_person') {
        chronotypeValue = 80;
        chronotypeLabel = 'Evening Person';
        chronotypeColor = 'rgb(54, 162, 235)'; // Blue
    } else if (sleepPreferences.chronotype === 'intermediate') {
        chronotypeValue = 50;
        chronotypeLabel = 'Intermediate';
        chronotypeColor = 'rgb(75, 192, 192)'; // Teal
    } else if (sleepPreferences.chronotype === 'variable') {
        chronotypeValue = 50;
        chronotypeLabel = 'Variable';
        chronotypeColor = 'rgb(153, 102, 255)'; // Purple
    }
    
    // Only create this chart if the element exists
    if (sleepChartElement) {
        // Create a gauge chart for chronotype
        const data = [{
            type: "indicator",
            mode: "gauge+number+delta",
            value: chronotypeValue,
            title: { text: "Chronotype", font: { size: 24 } },
            gauge: {
                axis: { range: [0, 100], tickwidth: 1 },
                bar: { color: chronotypeColor },
                bgcolor: "white",
                borderwidth: 2,
                bordercolor: "gray",
                steps: [
                    { range: [0, 33], color: "rgba(255, 159, 64, 0.2)" },
                    { range: [33, 66], color: "rgba(75, 192, 192, 0.2)" },
                    { range: [66, 100], color: "rgba(54, 162, 235, 0.2)" }
                ],
                threshold: {
                    line: { color: "red", width: 4 },
                    thickness: 0.75,
                    value: chronotypeValue
                }
            }
        }];

        const layout = {
            width: 400,
            height: 250,
            margin: { t: 25, r: 25, l: 25, b: 25 },
            annotations: [{
                text: chronotypeLabel,
                x: 0.5,
                y: 0.85,
                font: { size: 20 },
                showarrow: false
            }]
        };

        Plotly.newPlot(sleepChartElement, data, layout);
    }
}

/**
 * Capitalize the first letter of a string
 */
function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}