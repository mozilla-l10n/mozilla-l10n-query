'use strict';

/**
 * Map a query type and value to a pre-generated API file path.
 * @param {string} queryType - One of 'repo', 'type', 'bugzilla', 'tool', or ''.
 * @param {string} value - The query value (e.g. 'beta', 'product', 'www', 'pontoon').
 * @returns {string} Relative path to the JSON file.
 */
function buildApiUrl(queryType, value) {
    if (queryType === 'repo' && value) {
        return `api/repo/${value}.json`;
    }
    if (queryType === 'type' && value) {
        return `api/type/${value}.json`;
    }
    if (queryType === 'bugzilla' && value) {
        return `api/bugzilla/${value}.json`;
    }
    if (queryType === 'tool' && value) {
        return `api/tool/${value}.json`;
    }
    return 'api/index.json';
}

/**
 * Fetch a JSON file and display its contents in the results element.
 * @param {string} url - URL of the JSON file to fetch.
 */
async function fetchAndDisplay(url) {
    const resultsEl = document.getElementById('results');
    try {
        resultsEl.textContent = 'Loading…';
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        resultsEl.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resultsEl.textContent = `Error: ${err.message}`;
    }
}

/**
 * Read query type and value from the current URL search params.
 * @returns {{ queryType: string, value: string }}
 */
function getQueryFromLocation() {
    const params = new URLSearchParams(window.location.search);
    for (const qt of ['repo', 'type', 'bugzilla', 'tool']) {
        if (params.has(qt)) {
            return { queryType: qt, value: params.get(qt) };
        }
    }
    return { queryType: '', value: '' };
}

if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('query-form');
        const queryTypeEl = document.getElementById('query-type');
        const queryValueEl = document.getElementById('query-value');

        // Load from URL params on page load
        const { queryType, value } = getQueryFromLocation();
        if (queryType) {
            queryTypeEl.value = queryType;
            queryValueEl.value = value;
            fetchAndDisplay(buildApiUrl(queryType, value));
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const qt = queryTypeEl.value;
            const v = queryValueEl.value.trim();
            const url = buildApiUrl(qt, v);
            const params = new URLSearchParams();
            if (qt && v) {
                params.set(qt, v);
            }
            history.replaceState(
                null,
                '',
                params.toString() ? `?${params}` : window.location.pathname
            );
            fetchAndDisplay(url);
        });
    });
}

if (typeof module !== 'undefined') module.exports = { buildApiUrl };
