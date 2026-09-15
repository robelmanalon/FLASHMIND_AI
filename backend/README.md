# FlashMind AI API

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Supabase configuration

Set these values in `backend/.env`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_ROLE_KEY=your-server-only-service-role-key
```

`SUPABASE_KEY` is used by normal database, auth, and storage services. The service-role key is optional and must remain server-only; it is reserved for administrative operations. Never add either real key to source control or frontend environment variables. Rotate any service-role key that has been shared outside the Supabase dashboard.

The async service layer is available under `app/services`:

- `supabase.py`: cached supabase-py connection factory
- `authentication.py`: sign-up, sign-in, and sign-out
- `database.py`: async CRUD facade for Supabase tables
- `profiles.py`, `decks.py`, `flashcards.py`, `quizzes.py`, `study_history.py`: table-specific CRUD helpers
- `files.py`, `storage.py`: file metadata and Supabase Storage operations

The API exposes JSON REST endpoints and allows requests from the Vite frontend at `http://localhost:5173`.

## REST endpoints

- `POST /auth/register`, `POST /auth/login`
- `GET /profile`
- `GET /decks`, `POST /decks`, `PUT /decks/{id}`, `DELETE /decks/{id}`
- `GET /flashcards`, `POST /flashcards`, `PUT /flashcards/{id}`, `DELETE /flashcards/{id}`
- `POST /quiz/generate`, `GET /quiz/{id}`
- `POST /study/review`

The current local implementation uses an in-memory repository so it can run without credentials. Supabase settings are already available in `.env.example`; the repository layer can be replaced with Supabase queries when persistence is enabled.