"""
Webhooks Resource & Security Verification Helpers
"""

import hmac
import hashlib
from typing import Optional, Dict, Any, Union


class WebhooksResource:
    def __init__(self, client):
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all registered webhook endpoints."""
        return self._client._request("GET", "/webhooks")

    def create(
        self,
        name: str,
        webhook_url: str,
        secret: Optional[str] = None,
        platform: str = "all",
        send_auto: bool = True
    ) -> Dict[str, Any]:
        """
        Register a new webhook endpoint.
        
        Args:
            name: Friendly label (e.g. 'Production CRM Pipeline')
            webhook_url: Target destination URL
            secret: Optional HMAC secret for payload signature verification
            platform: 'all', 'maps', or 'website'
            send_auto: Automatically dispatch on job completion
        """
        payload = {
            "name": name,
            "webhook_url": webhook_url,
            "platform": platform,
            "send_auto": send_auto
        }
        if secret:
            payload["secret"] = secret
        return self._client._request("POST", "/webhooks", json=payload)

    def update(self, webhook_id: str, **kwargs) -> Dict[str, Any]:
        """Update an existing webhook configuration."""
        return self._client._request("PUT", f"/webhooks/{webhook_id}", json=kwargs)

    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Remove a webhook endpoint."""
        return self._client._request("DELETE", f"/webhooks/{webhook_id}")

    @staticmethod
    def verify_signature(
        raw_body: Union[str, bytes],
        signature_header: str,
        secret: str
    ) -> bool:
        """
        Verify incoming webhook HMAC SHA-256 signature from the X-Bolt-Signature header.
        
        Args:
            raw_body: Exact raw request body as bytes or string
            signature_header: Value of the 'X-Bolt-Signature' HTTP header (e.g. 'sha256=abcdef...')
            secret: Your configured webhook secret key
            
        Returns:
            True if the signature is valid, False otherwise.
        """
        if not signature_header or not secret or raw_body is None:
            return False

        if isinstance(raw_body, str):
            raw_body = raw_body.encode("utf-8")

        expected_sig = signature_header[7:] if signature_header.startswith("sha256=") else signature_header
        computed_sig = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig.strip(), computed_sig.strip())
