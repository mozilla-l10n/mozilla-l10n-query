'use strict';

const { test } = require('node:test');
const assert = require('node:assert');
const { buildApiUrl } = require('../../docs/app.js');

test('?repo=beta maps to api/repo/beta.json', () => {
    assert.strictEqual(buildApiUrl('repo', 'beta'), 'api/repo/beta.json');
});

test('?type=product maps to api/type/product.json', () => {
    assert.strictEqual(buildApiUrl('type', 'product'), 'api/type/product.json');
});

test('?bugzilla=www maps to api/bugzilla/www.json', () => {
    assert.strictEqual(buildApiUrl('bugzilla', 'www'), 'api/bugzilla/www.json');
});

test('?tool=pontoon maps to api/tool/pontoon.json', () => {
    assert.strictEqual(buildApiUrl('tool', 'pontoon'), 'api/tool/pontoon.json');
});

test('?tool=all maps to api/tool/all.json', () => {
    assert.strictEqual(buildApiUrl('tool', 'all'), 'api/tool/all.json');
});

test('no params maps to api/index.json', () => {
    assert.strictEqual(buildApiUrl('', ''), 'api/index.json');
});
