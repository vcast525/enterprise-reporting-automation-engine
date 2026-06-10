# Raw Data

This folder contains the original source files used by the Enterprise Reporting Automation Engine.

## Purpose

The files stored in this folder represent the initial input datasets that are ingested by the application.

Examples include:

- Control Inventory
- Issues Report
- Assessment Results
- Application Inventory

## Guidelines

- Source files should remain unchanged.
- Files in this folder serve as the system of record for ingestion.
- Data transformations should not occur within this folder.
- All processing should occur within the application pipeline.

## Data Flow

Raw Data → Validation → Transformation → Reporting