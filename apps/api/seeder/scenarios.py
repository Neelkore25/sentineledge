from datetime import datetime, timezone, timedelta

SCENARIO_TEMPLATES = {
    "brute_force": {
        "id": "scenario_brute_force",
        "name": "Too Many Doors",
        "category": "Credential Access",
        "description": "Rapid succession of 15 failed authentication attempts against the Admin Auth Portal followed by a suspicious login.",
        "target_asset_id": "ASSET_AUTH_PORTAL",
        "target_user_id": "usr_finance_admin",
        "source_ip": "194.26.29.114",
        "location": "Bucharest, RO",
        "events": [
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Unknown-Device-Linux",
                "bytes_transferred": 512,
                "event_metadata": {"reason": "Invalid password", "attempt_index": i}
            } for i in range(1, 13)
        ] + [
            {
                "event_type": "LOGIN_SUCCESS",
                "action": "LOGIN",
                "status": "SUCCESS",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Unknown-Device-Linux",
                "bytes_transferred": 2048,
                "event_metadata": {"mfa_prompted": False, "session_created": True}
            },
            {
                "event_type": "ADMIN_ACCESS",
                "action": "LIST_ACCOUNTS",
                "status": "SUCCESS",
                "endpoint": "/api/v1/admin/users",
                "source": "auth_service",
                "device_id": "Unknown-Device-Linux",
                "bytes_transferred": 14200,
                "event_metadata": {"query": "SELECT * FROM users"}
            }
        ]
    },
    "suspicious_login": {
        "id": "scenario_suspicious_login",
        "name": "Unexpected Visitor",
        "category": "Initial Access",
        "description": "Off-hours login (03:15 AM) from a new foreign IP address and unmanaged device bypassing standard geofencing.",
        "target_asset_id": "ASSET_ERP_PORTAL",
        "target_user_id": "usr_ops_lead",
        "source_ip": "185.220.101.5",
        "location": "Frankfurt, DE",
        "events": [
            {
                "event_type": "LOGIN_SUCCESS",
                "action": "LOGIN",
                "status": "SUCCESS",
                "endpoint": "/portal/sso",
                "source": "vpn_gateway",
                "device_id": "Win10-Unmanaged-BYOD",
                "bytes_transferred": 4096,
                "event_metadata": {"country": "DE", "is_tor_exit_node": True}
            },
            {
                "event_type": "FILE_DOWNLOAD",
                "action": "DOWNLOAD",
                "status": "SUCCESS",
                "endpoint": "/portal/invoices/q3_summary.pdf",
                "source": "erp_portal",
                "device_id": "Win10-Unmanaged-BYOD",
                "bytes_transferred": 15_000_000,
                "event_metadata": {"filename": "q3_summary.pdf"}
            }
        ]
    },
    "privilege_jump": {
        "id": "scenario_privilege_jump",
        "name": "The Privilege Jump",
        "category": "Privilege Escalation",
        "description": "Standard engineering account abruptly assigned Super-Admin permissions without an associated change ticket.",
        "target_asset_id": "ASSET_ACTIVE_DIR",
        "target_user_id": "usr_dev_intern",
        "source_ip": "10.0.4.55",
        "location": "Mumbai, IN",
        "events": [
            {
                "event_type": "API_REQUEST",
                "action": "QUERY_ROLES",
                "status": "SUCCESS",
                "endpoint": "/api/v1/iam/roles",
                "source": "iam_service",
                "device_id": "Laptop-Corporate-DEV09",
                "bytes_transferred": 8192,
                "event_metadata": {"role_queried": "DomainAdmin"}
            },
            {
                "event_type": "PRIVILEGE_CHANGE",
                "action": "GRANT_ROLE",
                "status": "SUCCESS",
                "endpoint": "/api/v1/iam/assign",
                "source": "iam_service",
                "device_id": "Laptop-Corporate-DEV09",
                "bytes_transferred": 1024,
                "event_metadata": {"granted_role": "SuperAdministrator", "ticket_id": None}
            }
        ]
    },
    "data_exfiltration": {
        "id": "scenario_data_exfiltration",
        "name": "The Large Download",
        "category": "Exfiltration",
        "description": "High-volume compressed SQL database dump transfer (2.8 GB) initiated during non-working hours.",
        "target_asset_id": "ASSET_CUSTOMER_DB",
        "target_user_id": "usr_finance_admin",
        "source_ip": "10.0.2.14",
        "location": "Mumbai, IN",
        "events": [
            {
                "event_type": "DB_QUERY",
                "action": "EXECUTE_EXPORT",
                "status": "SUCCESS",
                "endpoint": "/db/export/customers_full.sql.gz",
                "source": "database_server",
                "device_id": "Laptop-Corporate-FIN01",
                "bytes_transferred": 50_000,
                "event_metadata": {"table": "customers_financial_pii", "rows": 450000}
            },
            {
                "event_type": "FILE_DOWNLOAD",
                "action": "EGRESS_TRANSFER",
                "status": "SUCCESS",
                "endpoint": "/external/cloud_upload",
                "source": "network_egress",
                "device_id": "Laptop-Corporate-FIN01",
                "bytes_transferred": 2_800_000_000,
                "event_metadata": {"destination": "https://transfer.sh/drop", "duration_sec": 140}
            }
        ]
    },
    "multi_stage": {
        "id": "scenario_multi_stage",
        "name": "The Long Night",
        "category": "Multi-Stage Compromise",
        "description": "Full-spectrum kill chain: Reconnaissance sweep -> Brute force -> Privilege grant -> Bulk exfiltration.",
        "target_asset_id": "ASSET_CUSTOMER_DB",
        "target_user_id": "usr_finance_admin",
        "source_ip": "194.26.29.200",
        "location": "Bucharest, RO",
        "events": [
            {
                "event_type": "PORT_SCAN",
                "action": "PROBE",
                "status": "BLOCKED",
                "endpoint": "/port/8080",
                "source": "edge_firewall",
                "device_id": "Scanner-Node",
                "bytes_transferred": 256,
                "event_metadata": {"ports": [22, 80, 443, 3306, 5432, 8080]}
            },
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 512,
                "event_metadata": {"attempt": 1}
            },
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 512,
                "event_metadata": {"attempt": 2}
            },
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 512,
                "event_metadata": {"attempt": 3}
            },
            {
                "event_type": "LOGIN_SUCCESS",
                "action": "LOGIN",
                "status": "SUCCESS",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 2048,
                "event_metadata": {"compromised_credential": True}
            },
            {
                "event_type": "PRIVILEGE_CHANGE",
                "action": "GRANT_ROLE",
                "status": "SUCCESS",
                "endpoint": "/api/v1/iam/assign",
                "source": "iam_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 1024,
                "event_metadata": {"granted": "FullAdmin"}
            },
            {
                "event_type": "FILE_DOWNLOAD",
                "action": "EGRESS_TRANSFER",
                "status": "SUCCESS",
                "endpoint": "/external/cloud_upload",
                "source": "network_egress",
                "device_id": "Scanner-Node",
                "bytes_transferred": 1_900_000_000,
                "event_metadata": {"file": "production_backup.tar.gz"}
            }
        ]
    },
    "recon_sweep": {
        "id": "scenario_recon_sweep",
        "name": "Recon in the Dark",
        "category": "Reconnaissance",
        "description": "Broad port and service enumeration probing edge endpoints from an external scanner.",
        "target_asset_id": "ASSET_AUTH_PORTAL",
        "target_user_id": None,
        "source_ip": "45.154.255.88",
        "location": "Sofia, BG",
        "events": [
            {
                "event_type": "PORT_SCAN",
                "action": "SYN_SCAN",
                "status": "BLOCKED",
                "endpoint": f"/probe/port_{p}",
                "source": "edge_firewall",
                "device_id": "Unknown-Scanner",
                "bytes_transferred": 128,
                "event_metadata": {"port": p}
            } for p in [21, 22, 23, 25, 80, 443, 1433, 3306, 3389, 5432, 6379, 8080, 9200]
        ]
    },
    "backup_failure": {
        "id": "scenario_backup_failure",
        "name": "Backup Severed",
        "category": "Impact",
        "description": "Automated snapshot job failed and backup integrity check flagged corrupted replica on the primary DB.",
        "target_asset_id": "ASSET_CUSTOMER_DB",
        "target_user_id": "usr_backup_svc",
        "source_ip": "10.0.1.99",
        "location": "Mumbai, IN",
        "events": [
            {
                "event_type": "BACKUP_FAILED",
                "action": "SNAPSHOT_CREATE",
                "status": "FAILURE",
                "endpoint": "/backup/v2/snapshot",
                "source": "backup_daemon",
                "device_id": "Backup-Server-01",
                "bytes_transferred": 0,
                "event_metadata": {"error": "Volume lock timeout", "asset": "Customer Financial DB"}
            },
            {
                "event_type": "BACKUP_TAMPERED",
                "action": "VERIFY_REPLICA",
                "status": "FAILURE",
                "endpoint": "/backup/v2/verify",
                "source": "backup_daemon",
                "device_id": "Backup-Server-01",
                "bytes_transferred": 4096,
                "event_metadata": {"checksum_mismatch": True}
            }
        ]
    }
}
