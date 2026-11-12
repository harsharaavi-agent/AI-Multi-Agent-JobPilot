"""Search multiple configured career-site providers."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Protocol


class JobSearchProvider(Protocol):
    """Interface implemented by each career-site search adapter."""

    def search(
        self,
        query: str,
        location: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        ...


class MultiSiteJobSearchAgent:
    """Queries registered providers that implement a ``search`` method."""

    def __init__(self, providers: Mapping[str, JobSearchProvider]):
        self.providers = dict(providers)

    def search(
        self,
        query: str,
        location: Optional[str] = None,
        max_results_per_site: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return listings from each provider, tagged with their source."""
        if not query.strip():
            raise ValueError("Job search query cannot be empty.")
        if max_results_per_site < 1:
            raise ValueError("max_results_per_site must be at least 1.")
        if not self.providers:
            raise RuntimeError("No career-site search providers configured.")

        jobs: List[Dict[str, Any]] = []
        seen_urls: set[str] = set()

        for site_name, provider in self.providers.items():
            site_jobs = provider.search(
                query=query,
                location=location,
                limit=max_results_per_site,
            )

            if not isinstance(site_jobs, list):
                raise TypeError(
                    f"Provider '{site_name}' must return a list of jobs."
                )

            for job in site_jobs[:max_results_per_site]:
                if not isinstance(job, dict):
                    raise TypeError(
                        f"Provider '{site_name}' returned a non-dictionary job."
                    )

                normalized_job = dict(job)
                if not normalized_job.get("source"):
                    normalized_job["source"] = site_name
                job_url = normalized_job.get("url") or normalized_job.get(
                    "apply_url"
                )
                if job_url:
                    normalized_url = str(job_url).strip().casefold()
                    if normalized_url in seen_urls:
                        continue
                    seen_urls.add(normalized_url)
                jobs.append(normalized_job)

        return jobs
