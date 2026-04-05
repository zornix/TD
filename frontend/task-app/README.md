# TaskFlow Frontend

This is a modern, Next.js based frontend application for the Task Management system.

## Setup & Running

This project uses Next.js 14 App Router, initialized without Tailwind to provide a flexible styling architecture with vanilla CSS.

### Starting the UI
Start the development server:

```bash
npm run dev
```

Navigate to [http://localhost:3000](http://localhost:3000)

> **Note**: Ensure the Python backend is running concurrently on port 8000. It will be queried dynamically at `http://localhost:8000/api`.

## File Structure breakdown

- `src/` 
  - `app/` 
    - `page.tsx`: The primary route point loading the Application Dashboard.
    - `layout.tsx`: Base document structure handling font-family loading and generic metadata.
    - `globals.css`: Handles all styling including grid definitions, glassmorphic panels, and thematic tokens (`--primary`, `--bg-main`).
  - `components/` 
    - `Dashboard.tsx`: Central orchestrator view. Loads current categorized metrics, task lists, and orchestrates fetching from the backend.
    - `CategorySetup.tsx`: Responsible for enabling the creation of new logical groupings (Categories) and allocating weight coefficients to them.
    - `TaskForm.tsx`: Collects all new task criteria including relative importance, effort, and scheduling.
    - `TaskList.tsx`: A grouped layout managing mapping of individual item cards.
    - `TaskItem.tsx`: Representation of an individual task, handles status toggling logic and deletion requests. Includes categorized styling for the "quadrant" status.
  - `utils/` 
    - `api.ts`: Isomorphic Javascript bindings mapping exact requests (e.g., toggleTaskDone, createTask) logically to the FastAPI HTTP paths.
    - `types.ts`: Provides local structured type safety overlapping the server schemas (Task, Category models).

## High Level Operation Logic

1. **Dashboard Loading:**
   When navigating to the page, `Dashboard.tsx` independently queries active contexts via `getCategories()` and `getTasks()`.
2. **Category Structuring:**
   Before tracking tasks, users generate custom "Categories" and weight attributes leveraging `CategorySetup`.
3. **Task Manipulation:**
   When `TaskForm` calculates a request, the `api.ts` relay submits to `POST /api/tasks`, delegating Priority mathematical resolution server-side.
   On a successful resolution, the parent layout receives a reload pulse.
4. **Task Iteration:**
   Users check-off active elements from the UI triggers `toggleTaskDone` (`PATCH /api/tasks/{int}/done`), applying a strikethrough class on completion.

## Design
UI incorporates a fluid dark theme and Glassmorphism leveraging pseudo-blurring over a complex dynamic background. No auxiliary CSS framework is attached (e.g. Tailwind), keeping overhead zero.
