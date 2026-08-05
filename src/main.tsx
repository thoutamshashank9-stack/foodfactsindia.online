import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
// Self-hosted fonts — eliminates render-blocking Google Fonts network request.
// These are bundled into the CSS chunk by Vite and served from the same origin.
import '@fontsource/inter/400.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import '@fontsource/inter/800.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/600.css';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
