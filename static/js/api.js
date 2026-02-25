const API_BASE = ''; // same origin

async function apiCall(endpoint, method = 'GET', body = null, requiresAuth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (requiresAuth) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = '/login-page';
            throw new Error('No token');
        }
        headers['Authorization'] = `Bearer ${token}`;
    }
    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);
    
    const response = await fetch(API_BASE + endpoint, options);
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/login-page';
        throw new Error('Unauthorized');
    }
    const data = await response.json();
    if (!response.ok) throw data;
    return data;
}