# Auth Template with Google OAuth

A modern authentication template using FastAPI, React, MongoDB, and Google OAuth.

## Features

- 🔐 Google OAuth Authentication
- 📱 Responsive Design with Tailwind CSS
- 🚀 FastAPI Backend
- 🗄️ MongoDB Database
- 🔒 JWT Token Authentication
- 🎨 Modern UI/UX

## Tech Stack

### Frontend

- React with TypeScript
- Tailwind CSS
- React Router DOM
- Google OAuth
- Vite

### Backend

- FastAPI
- MongoDB
- Google OAuth Verification

## Setup Instructions

### Prerequisites

- Node.js
- Python
- MongoDB

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/hsd2514/auth_template_2.git
   cd auth_template_2/backend
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file:

   ```env
   SECRET_KEY="your-secret-key"
   GOOGLE_CLIENT_ID="your-google-client-id"
   ```

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create .env file:

   ```env
   VITE_GOOGLE_CLIENT_ID="your-google-client-id"
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

### Tailwind CSS Setup

1. Install Tailwind CSS:

   ```bash
   npm install -D tailwindcss postcss autoprefixer
   ```

2. Initialize Tailwind CSS:

   ```bash
   npx tailwindcss init -p
   ```

3. Configure your template paths in `tailwind.config.js`:

   ```js
   module.exports = {
     content: ["./src/**/*.{js,jsx,ts,tsx}"],
     theme: {
       extend: {},
     },
     plugins: [],
   };
   ```

4. Add Tailwind directives to `src/index.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

### Google OAuth Setup

1. Go to Google Cloud Console
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized origins:
   - http://localhost:5173
   - http://127.0.0.1:5173
6. Add authorized redirect URIs:
   - http://localhost:5173
   - http://localhost:5173/login

## Project Structure
