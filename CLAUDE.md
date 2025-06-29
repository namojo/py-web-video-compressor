# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project focused on observability and monitoring capabilities. The project uses OpenTelemetry for distributed tracing and metrics collection, with Prometheus as the metrics backend.

## Common Commands

### Environment Setup
- **Create virtual environment**: `python -m venv venv`
- **Activate environment** (macOS/Linux): `source venv/bin/activate`
- **Activate environment** (Windows): `venv\Scripts\activate`
- **Install dependencies**: `pip install -r requirements.txt`

### Development
- **Run Python files**: `python <filename>.py`
- **Install new dependencies**: `pip install <package>` then `pip freeze > requirements.txt`

## Architecture Overview

### Technology Stack
- **Python**: Primary development language
- **OpenTelemetry**: Distributed tracing and observability framework
  - `opentelemetry-api`: Core API for instrumentation
  - `opentelemetry-sdk`: SDK implementation for telemetry data
  - `opentelemetry-exporter-prometheus`: Prometheus metrics exporter
- **Prometheus**: Metrics collection and monitoring system
- **Requests**: HTTP client library for external API calls

### Project Structure
This project is currently in initial setup phase with dependency specifications defined. The architecture suggests building applications with:
- HTTP request capabilities for external service integration
- Comprehensive observability through OpenTelemetry instrumentation
- Metrics export to Prometheus for monitoring and alerting