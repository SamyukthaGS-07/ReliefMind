We'll follow this sequence:

PHASE 1
Project setup
    ↓
PHASE 2
Database + models
    ↓
PHASE 3
Report ingestion
    ↓
PHASE 4
AI extraction
    ↓
PHASE 5
Dedup + reliability + freshness
    ↓
PHASE 6
Needs + priority engine
    ↓
PHASE 7
Resources + matching
    ↓
PHASE 8
Relief plan generation
    ↓
PHASE 9
Human approval
    ↓
PHASE 10
Replanning + what-changed diff
    ↓
PHASE 11
Next.js dashboard
    ↓
PHASE 12
Scenario injector + demo polish
First milestone

We'll get this working first:

POST /reports
       ↓
Report stored
       ↓
AI extracts:
location
time
need
urgency
people affected
       ↓
Incident created/linked
       ↓
Need created
       ↓
Priority calculated
       ↓
GET /incidents

Once that works, we have the first actual slice of ReliefMind.

Step 1 — Repository Structure

I'd start with a monorepo:

reliefmind/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   └── routes/
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │
│   │   ├── engines/
│   │   │   ├── extraction.py
│   │   │   ├── deduplication.py
│   │   │   ├── reliability.py
│   │   │   ├── prioritization.py
│   │   │   └── planning.py
│   │   │
│   │   └── db/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── ...
│
├── data/
│   ├── scenarios/
│   └── seed/
│
├── docker-compose.yml
├── README.md
└── .gitignore
Why this structure?

The important distinction is:

services/

handles application/business operations,

while:

engines/

contains the actual intelligence/decision logic.

So we don't end up with one gigantic main.py.

Step 2 — Backend Stack

Let's lock this:

Python 3.12
FastAPI
Pydantic v2
SQLAlchemy 2
PostgreSQL
PostGIS
Alembic
httpx
sentence-transformers
LLM API

For development, Docker Compose can run PostgreSQL.

Step 3 — First Database Slice

We'll initially implement:

Source
Report
Incident
IncidentReport
Need

Then test:

Citizen report
      ↓
POST /reports
      ↓
DB
      ↓
Extraction
      ↓
Incident
      ↓
Need

We shouldn't build resources, routing, optimization, approval, etc. yet.

Get one vertical slice working first.

Step 4 — Our First API

The first endpoint:

POST /api/v1/reports

Request:

{
  "source_type": "citizen",
  "content": "Flood water has entered around 40 houses near Central School. Around 80 people are affected and elderly residents need medical help."
}

Eventually the response becomes something like:

{
  "report_id": "REP-001",
  "incident_id": "INC-001",
  "extraction": {
    "event_type": "flood",
    "location": "Central School",
    "people_affected": 80,
    "needs": [
      {
        "type": "medical",
        "urgency": "high"
      }
    ]
  },
  "reliability": 0.67,
  "freshness": 1.0,
  "priority": {
    "score": 86,
    "level": "CRITICAL"
  }
}

That single endpoint will eventually demonstrate a surprisingly large portion of the project.

One important rule before we code

We should not start by making the frontend.

The temptation will be to make the dashboard because it's visually exciting.

Don't.

First make this work:

messy report → structured evidence → incident → need → priority

Then:

need → resource → route → plan

Then:

plan → human approval → dispatch → replan

Finally, build the UI around those APIs.

That way the frontend is displaying a real system, rather than simulating one.