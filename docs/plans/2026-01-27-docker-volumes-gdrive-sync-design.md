# Docker Volumes Google Drive Sync Documentation

**Date:** 2026-01-27
**Status:** Implemented

## Overview

Document the process for syncing the `$HOME/docker_volumes` directory with Google Drive Desktop to provide automatic backup and cross-machine restore capabilities.

## Context

The project uses Docker containers managed through Portainer stacks. Persistent data is stored in `$HOME/docker_volumes` (gitignored). Users need a way to back up this data and sync it across machines.

## Solution

Add a "Docker Volumes Backup" section to the README that provides step-by-step instructions for configuring Google Drive Desktop to sync the docker_volumes directory.

## Design Decisions

1. **Placement**: Added after "Service Stacks" and before "Setting up authentication" - infrastructure-related but not part of initial setup
2. **Tone**: Match existing README style - concise, numbered steps, assumes user familiarity with Google Drive Desktop UI
3. **Scope**: Basic setup steps only, no warnings or advanced configuration
4. **Path**: Use `$HOME/docker_volumes` to be explicit about location

## Implementation

Added new section with:
- Brief explanation of what docker_volumes contains
- 5-step setup process
- Note about benefits (backup and cross-machine restore)

## Benefits

- Users can easily back up container data
- Enables restore across different machines
- Automatic sync with Google Drive Desktop
- Simple setup process documented in one place
