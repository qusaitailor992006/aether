import uuid
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.aether_models import CloudBillingRecord

class BillingIngestionService:
    def normalize_and_ingest_records(self, db: Session, raw_records: List[Dict[str, Any]]) -> int:
        """
        Normalizes multi-cloud billing exports (GCP, AWS CUR, Azure Cost Management)
        into the unified AETHER standard billing schema.
        """
        records_to_insert = []
        for raw in raw_records:
            # Map heterogeneous cloud field aliases to canonical schema
            provider = raw.get("provider") or raw.get("cloud_provider") or "GCP"
            service = raw.get("service_name") or raw.get("service") or raw.get("line_item_product_code") or "Compute Engine"
            category = self._categorize_service(service, raw.get("service_category"))
            cost = float(raw.get("cost_usd") or raw.get("cost") or raw.get("unblended_cost") or 0.0)
            dept = raw.get("department") or raw.get("cost_center") or "Engineering"
            env = raw.get("environment") or raw.get("env") or "Production"
            
            timestamp_val = raw.get("timestamp")
            if isinstance(timestamp_val, str):
                try:
                    ts = datetime.fromisoformat(timestamp_val.replace("Z", "+00:00"))
                except Exception:
                    ts = datetime.utcnow()
            elif isinstance(timestamp_val, datetime):
                ts = timestamp_val
            else:
                ts = datetime.utcnow()

            record = CloudBillingRecord(
                id=str(uuid.uuid4()),
                record_id=raw.get("record_id") or f"REC-{uuid.uuid4().hex[:8].upper()}",
                provider=provider.upper(),
                service_name=service,
                service_category=category,
                resource_id=raw.get("resource_id") or f"res-{uuid.uuid4().hex[:6]}",
                department=dept,
                project_id=raw.get("project_id") or "enterprise-core-prod",
                environment=env,
                cost_usd=round(cost, 4),
                usage_amount=float(raw.get("usage_amount") or 1.0),
                usage_unit=raw.get("usage_unit") or "hours",
                timestamp=ts
            )
            records_to_insert.append(record)

        if records_to_insert:
            db.bulk_save_objects(records_to_insert)
            db.commit()
            
        return len(records_to_insert)

    def _categorize_service(self, service_name: str, explicit_category: str = None) -> str:
        if explicit_category:
            return explicit_category.capitalize()
            
        name_lower = service_name.lower()
        if any(k in name_lower for k in ["compute", "ec2", "vm", "cloud run", "kubernetes", "gke", "eks", "lambda"]):
            return "Compute"
        elif any(k in name_lower for k in ["s3", "storage", "gcs", "blob", "ebs", "disk"]):
            return "Storage"
        elif any(k in name_lower for k in ["sql", "bigquery", "rds", "dynamo", "database", "spanner", "firestore"]):
            return "Database"
        elif any(k in name_lower for k in ["network", "vpc", "load balancer", "nat", "route53", "cdn", "dns"]):
            return "Networking"
        elif any(k in name_lower for k in ["egress", "transfer", "bandwidth"]):
            return "Egress"
        else:
            return "Other"

billing_ingestion_service = BillingIngestionService()
