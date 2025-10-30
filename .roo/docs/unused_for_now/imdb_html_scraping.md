# IMDb HTML Scraping (Archived)

This document archives deprecated IMDb HTML scraping functions, preserved for historical reference. The application is migrating to API-only (RapidAPI) access per the provider simplification plan.

## Archived functions

### _extract_rating_from_obj

```python
def _extract_rating_from_obj(obj) -> Optional[float]:
    """
    Extract rating from a JSON-LD object if present.
    Looks for aggregateRating.ratingValue.
    """
    try:
        if not isinstance(obj, dict):
            return None
        ar = obj.get('aggregateRating') or obj.get('AggregateRating') or {}
        if isinstance(ar, dict):
            rv = ar.get('ratingValue') or ar.get('rating') or ar.get('value')
            if rv is not None:
                try:
                    return float(rv)
                except (TypeError, ValueError):
                    return None
        ir = obj.get('itemReviewed') or {}
        if isinstance(ir, dict):
            ar = ir.get('aggregateRating') or {}
            if isinstance(ar, dict):
                rv = ar.get('ratingValue')
                if rv is not None:
                    try:
                        return float(rv)
                    except (TypeError, ValueError):
                        return None
    except Exception:
        return None
    return None
```

### imdb_rating_scrape

```python
def imdb_rating_scrape(imdb_id_or_url: str, timeout: Optional[float] = None) -> Optional[float]:
    """
    Fetch and scrape the IMDb rating for a given IMDb title id or URL.

    Args:
        imdb_id_or_url: IMDb title id like 'tt0903747' or a full IMDb URL containing the id.
        timeout: Optional request timeout in seconds (default: 8).

    Returns:
        float rating value (eg, 8.7) if found, otherwise None.
    """
    imdb_id = imdb_id_normalize(imdb_id_or_url)
    if not imdb_id:
        return None

    url = f'https://www.imdb.com/title/{imdb_id}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

    try:
        resp = requests.get(url, headers=headers, timeout=timeout or 8)
        resp.raise_for_status()
        html = resp.text
    except requests.RequestException:
        return None

    # 1) Preferred: JSON-LD script tag(s)
    try:
        for m in re.finditer(r'<script type="application/ld\+json">(.+?)</script>', html, re.DOTALL | re.IGNORECASE):
            payload = m.group(1)
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if isinstance(data, list):
                for obj in data:
                    val = _extract_rating_from_obj(obj)
                    if val is not None:
                        return val
            else:
                val = _extract_rating_from_obj(data)
                if val is not None:
                    return val
    except Exception:
        pass

    # 2) Fallback: search for aggregateRating JSON fragment
    try:
        m = re.search(r'"aggregateRating"\s*:\s*{[^}]*"ratingValue"\s*:\s*"?(?P<val>\d+(\.\d+)?)', html, re.IGNORECASE | re.DOTALL)
        if m:
            return float(m.group('val'))
    except Exception:
        pass

    try:
        m = re.search(r'"ratingValue"\s*:\s*"?(?P<val>\d+(\.\d+)?)', html)
        if m:
            return float(m.group('val'))
    except Exception:
        pass

    # 3) UI-based fallback (fragile; may change)
    try:
        m = re.search(r'data-testid="hero-rating-bar__aggregate-rating__score"[^>]*>\s*<span[^>]*>\s*(\d+(\.\d+)?)\s*</span>', html, re.IGNORECASE)
        if m:
            return float(m.group(1))
    except Exception:
        pass

    return None
```

---

Subsequent tasks in the plan will remove these functions from the runtime Python modules and refactor call sites to API-only flows. This file preserves the original implementations for historical reference and debugging.