# Dashboard Showing GNSS-RFI (jamming) impact on civil aviation.

## Build and run

```sh
docker build -f Dockerfile -t jamming_dashboard .
docker run -p 8050:8050 -v "$(pwd)"/app:/app --rm jamming_dashboard
```

## Access the page

Go to `http://localhost:8050` in browser.

