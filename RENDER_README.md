# Deriv Bot v3 - Render Backend

OAuth backend for Deriv Bot v3 auto-hedging system.

## Environment Variables (Set in Render)

- `DERIV_APP_ID` - Your Deriv OAuth App ID
- `SECRET_KEY` - Random string for session security
- `PYTHON_VERSION` - 3.11.0

## Callback URL

Set in Deriv OAuth app:
`https://your-render-url.onrender.com/callback`

## Deployment

Automatically deploys from this repo via Render.
