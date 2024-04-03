const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

async function fetchApi(endpoint: string, options = {}) {
    const url = `${apiBaseUrl}${endpoint}`;

    const headers = options.body instanceof FormData ? {} : {'Content-Type': 'application/json'};
    const response = await fetch(url, {
        ...options,
        headers: {...headers, ...options.headers},
    });
    
    if (response.status === 204) return null;

    const data = await response.json()
    if (!response.ok) {
        throw new Error(`${data.message}`);
    }

    return data;
}

export const api = {
    uploadFile(formData: any) {
        return fetchApi('upload/', {
            method: 'POST',
            body: formData,
        });
    },
    createSighting(sightingData: any) {
        return fetchApi('sightings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sightingData),
        });
    },
    deleteAsteroid(asteroidId: string) {
        return fetchApi(`asteroids/${asteroidId}/`, {method: 'DELETE'});
    },
    searchSightings(searchTerm: string) {
        return fetchApi(`sightings/?search=${searchTerm}`);
    },
};
