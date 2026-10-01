# Novin Social

Novin Social is a multi-project social sales and opportunity-hunting platform.

## Pilot
The first pilot is YazdRail, but the core is project-agnostic and can later support real estate, education, services, products, and other campaigns.

## V1 scope
- Multi-organization / multi-project architecture
- Social source ingestion foundation
- Opportunity Hunter foundation
- Pattern Miner data model
- Iran relevance scoring fields
- Lead scoring fields
- Lead deduplication foundation
- Conversion tracking foundation
- Admin API foundation

## Stack
- FastAPI
- PostgreSQL
- Redis
- Docker
- Windmill (planned orchestration layer)

## Local development

1. Copy the environment template:

   cp .env.example .env

2. Start the stack:

   docker compose up --build

3. Initialize the database:

   docker compose exec api python -m app.init_db

4. Check the API:

   GET http://localhost:8000/health

## Core data model
- organizations
- projects
- campaigns
- leads
- lead_signals
- patterns

## Architecture principle
No YazdRail-specific business logic is hard-coded into the platform core. Project-specific targeting, scoring, knowledge, sales scripts, and conversion rules will be configuration-driven.
