# QuantumLens direct replacement bundle

This bundle addresses the urgent Supabase data mismatch and isolates embedding inference in its own container.

## Why PBT is missing

The archive's canonical source `backend/src/ingestion/mapped_metrics.json` contains 456 records, including 90 PBT source rows. The stale mirror `backend/data/generated/mapped_metrics.json` contains only 366 records and no PBT. The existing database also has 366 rows. This bundle makes the canonical source explicit and copies it to the generated mirror only after a successful database upsert.

## Apply in this order

1. Make a Git commit or copy the current project directory before overwriting files. Do not delete the existing Chroma directories.
2. Extract this bundle at the repository root and overwrite matching paths.
3. From `backend`, install/refresh dependencies if needed:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Inspect the planned load first (does not write to Supabase):

   ```powershell
   python -m warehouse.data_loader
   ```

5. Apply the load (automatically backs up the existing metrics table to `backend/data/backups/` before writing):

   ```powershell
   python -m warehouse.data_loader --apply
   ```

   The loader uses `on_conflict=metric_id,sheet_name,row_number`, so existing source records are updated and new source records inserted. The current source contains 456 unique keys versus 366 existing records; expect 90 new records if the live database matches the reported baseline. Existing overlapping values are updated to match the canonical mapped source, and the prior database snapshot is retained as JSON.

6. Run tests:

   ```powershell
   python -m pytest -q
   ```

7. Run health checks:

   ```powershell
   python scripts/project_health_check.py
   ```

8. To build the isolated embedding service and API:

   ```powershell
   docker compose up --build -d
   docker compose ps
   ```

   First model download may take time. The embedding service intentionally uses `sentence-transformers/all-MiniLM-L6-v2`, matching the existing local embedding generator's model. Do not switch the service model to BGE without rebuilding all existing Chroma vectors with that same model.

## Oracle removal

The replacement files remove active Oracle configuration from settings, Compose, repository, and SQL retriever paths. After verifying no remaining imports, delete the obsolete `backend/warehouse/create_schema.py`, `backend/warehouse/load_to_oracle.py`, and `backend/warehouse/oracle_client.py`. `backend/src/rag/sql_retriever.py` is now Supabase-backed. Keep any old database backups until final validation.

## Notes

- The bundle does not include `.env` or any credentials.
- The bundle does not execute a live database write by itself; the `--apply` flag is required.
- Existing Chroma databases are preserved. The embedding model is kept consistent to avoid mixing vectors from different embedding spaces.
