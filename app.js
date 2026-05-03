// Weather API Helper
const WeatherAPI = {
    async getCoordinates(cityName) {
        const url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(cityName)}&count=1&language=en&format=json`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            if (data.results && data.results.length > 0) {
                return data.results[0];
            }
            return null;
        } catch (error) {
            console.error("Error fetching coordinates:", error);
            return null;
        }
    },

    async getForecast(lat, lon) {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=temperature_2m,precipitation_probability,precipitation,weather_code&timezone=auto`;
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error("Error fetching forecast:", error);
            return null;
        }
    },

    getWeatherDescription(code) {
        const mapping = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm"
        };
        return mapping[code] || "Unknown";
    }
};

// Recommendation Engine
const RecommendationEngine = {
    generate(weatherData, durationHours) {
        const hourly = weatherData.hourly;
        const temps = hourly.temperature_2m.slice(0, durationHours);
        const precipProb = hourly.precipitation_probability.slice(0, durationHours);
        const precipAmount = hourly.precipitation.slice(0, durationHours);
        const codes = hourly.weather_code.slice(0, durationHours);

        const avgTemp = temps.reduce((a, b) => a + b, 0) / temps.length;
        const maxPrecipProb = Math.max(...precipProb);
        const totalPrecip = precipAmount.reduce((a, b) => a + b, 0);

        const suggestions = [];

        // Temperature
        if (avgTemp < 10) {
            suggestions.push("It's quite cold. Wear a heavy jacket, gloves, and a scarf.");
        } else if (avgTemp < 18) {
            suggestions.push("Mildly cold. A light jacket or sweater would be perfect.");
        } else if (avgTemp < 25) {
            suggestions.push("Comfortable weather. Light cotton clothes are recommended.");
        } else {
            suggestions.push("It's hot! Wear loose, breathable cotton clothes and stay hydrated.");
        }

        // Rain
        if (maxPrecipProb > 50 || totalPrecip > 0.5) {
            suggestions.push("High chance of rain. Definitely carry an umbrella or wear a raincoat.");
        } else if (maxPrecipProb > 20) {
            suggestions.push("Slight chance of rain. You might want to carry a compact umbrella just in case.");
        }

        // Sun
        const isSunny = codes.some(c => [0, 1].includes(c));
        if (isSunny && avgTemp > 20) {
            suggestions.push("It might be sunny. Don't forget your sunglasses and a cap.");
        }

        return suggestions;
    }
};

// App Main
document.addEventListener('DOMContentLoaded', () => {
    // UI Controller
    const UI = {
        elements: {
            cityInput: document.getElementById('city-input'),
            durationSelect: document.getElementById('duration-select'),
            getBtn: document.getElementById('get-recommendation-btn'),
            resultsSection: document.getElementById('results-section'),
            currentTemp: document.getElementById('current-temp'),
            locationName: document.getElementById('location-name'),
            weatherDesc: document.getElementById('weather-desc'),
            recommendationContent: document.getElementById('recommendation-content'),
            loader: document.getElementById('loading-overlay')
        },

        showLoader(show) {
            if (this.elements.loader) {
                this.elements.loader.classList.toggle('hidden', !show);
            }
        },

        updateResults(location, weather, suggestions) {
            if (!this.elements.currentTemp) return;
            
            this.elements.currentTemp.textContent = Math.round(weather.current_weather.temperature);
            this.elements.locationName.textContent = `${location.name}, ${location.country || ''}`;
            this.elements.weatherDesc.textContent = WeatherAPI.getWeatherDescription(weather.current_weather.weathercode);

            this.elements.recommendationContent.innerHTML = suggestions
                .map(s => `<div class="suggestion-item">${s}</div>`)
                .join('');

            this.elements.resultsSection.classList.remove('hidden');
            this.elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    };

    if (UI.elements.getBtn) {
        UI.elements.getBtn.addEventListener('click', async () => {
            const city = UI.elements.cityInput.value.trim();
            const duration = parseInt(UI.elements.durationSelect.value);

            if (!city) {
                alert("Please enter a city name!");
                return;
            }

            UI.showLoader(true);

            try {
                const location = await WeatherAPI.getCoordinates(city);
                if (!location) {
                    throw new Error("Could not find that city. Please check the spelling.");
                }

                const weather = await WeatherAPI.getForecast(location.latitude, location.longitude);
                if (!weather) {
                    throw new Error("Weather service is unavailable. Please check your internet connection.");
                }

                const suggestions = RecommendationEngine.generate(weather, duration);
                UI.updateResults(location, weather, suggestions);
            } catch (err) {
                console.error("OOTDBuddy Error:", err);
                alert(err.message || "An unexpected error occurred. Please try again.");
            } finally {
                UI.showLoader(false);
            }
        });
    }

    if (UI.elements.cityInput) {
        UI.elements.cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') UI.elements.getBtn.click();
        });
    }
});
