import axios from 'axios';

// Create an Axios instance pointing to the FastAPI backend
// In dev, Vite proxies /api, or we point directly if we set CORS.
// Let's assume dev server is separate for now, so we point to localhost:8000
// Dynamically determine the API URL based on the current hostname
// This allows the app to work whether accessed via localhost, IP, or domain.
const API_PORT = '8001';
const baseURL = `${window.location.protocol}//${window.location.hostname}:${API_PORT}/api/v1`;

const api = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const searchDownload = async (query: string, songLimit?: number) => {
    return api.post('/downloads/search', { query, song_limit: songLimit });
};

export const artistDownload = async (artistUrl: string, artistName: string, limit?: number, songLimit?: number, maxAlbumLength?: number) => {
    return api.post('/downloads/artist', {
        artist_url: artistUrl,
        artist_name: artistName,
        limit,
        song_limit: songLimit,
        max_album_length: maxAlbumLength
    });
};

export const scanLibrary = async () => {
    return api.post('/library/scan');
};

export default api;
