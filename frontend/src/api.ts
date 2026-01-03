import axios from 'axios';

// In dev, we point to port 8001. In prod (Nginx), we use relative path /api/v1 which Nginx proxies.
const baseURL = import.meta.env.DEV
    ? `${window.location.protocol}//${window.location.hostname}:8001/api/v1`
    : '/api/v1';

const api = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface FileNode {
    name: string;
    type: 'directory' | 'file';
    path: string;
    size: number;
}

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

export const fetchFiles = async (path: string = ''): Promise<FileNode[]> => {
    const response = await api.get('/library/files', { params: { path } });
    return response.data;
};

export default api;
